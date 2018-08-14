#! /usr/bin/env python3
# MIT License
#
# Copyright (c) 2018 Joshua Watt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import logging
import sys
import math
from aaop import AAOPFile

def to_obj(args, infile, outfile):
    # Write all vertexes
    for stack in range(infile.num_stacks):
        outfile.write('# Stack {stack:d}\n'.format(stack=stack))
        for spoke in range(infile.num_spokes):
            phi = 2 * math.pi * spoke / infile.num_spokes
            rho = infile.spokes[stack][spoke]

            outfile.write('v {x:f} {y:f} {z:f}\n'.format(
                z = infile.stacks[stack],
                x = rho * math.cos(phi),
                y = rho * math.sin(phi)))

    # Write all faces. Make a rectangle for each stack that links the
    # vertex in it to the next
    for stack in range(infile.num_stacks - 1):
        outfile.write('# Stack {stack:d}\n'.format(stack=stack))
        cur_stack_idx = stack * infile.num_spokes + 1
        next_stack_idx = (stack + 1) * infile.num_spokes + 1

        for spoke in range(infile.num_spokes):
            next_spoke = (spoke + 1) % infile.num_spokes

            outfile.write('f {v1:d} {v2:d} {v3:d} {v4:d}\n'.format(
                v1=cur_stack_idx + spoke,
                v2=cur_stack_idx + next_spoke,
                v3=next_stack_idx + next_spoke,
                v4=next_stack_idx + spoke
                ))

    if args.enclose:
        outfile.write('# top cap\n')
        outfile.write('f {v}\n'.format(
            v=' '.join('%d' % (1 + d) for d in range(infile.num_spokes))))

        outfile.write('# bottom cap\n')
        outfile.write('f {v}\n'.format(
            v=' '.join('%d' % (1 + d + infile.num_spokes * (infile.num_stacks - 1)) for d in range(infile.num_spokes))))

def main():
    def handle_output(args, infile, outfile):
        if args.output == 'obj':
            to_obj(args, infile, outfile)

    parser = argparse.ArgumentParser(description="Converts an AAOP file to a OBJ model")
    parser.add_argument('--enclose', '-e', help="Enclose ends of model", action='store_true')
    parser.add_argument('infile', help='AAOP input file (.aop). "-" for stdin')
    parser.add_argument('outfile', help='Output file. "-" for stdout')
    parser.add_argument('-o', '--output', help='Output format', choices=['obj'], default='obj')

    args = parser.parse_args()

    if args.infile == '-':
        aaop = AAOPFile(sys.stdin)
    else:
        with open(args.infile, 'r') as infile:
            aaop = AAOPFile(infile)

    if args.outfile == '-':
        handle_output(args, aaop, sys.stdout)
    else:
        with open(args.outfile, 'w') as outfile:
            handle_output(args, aaop, outfile)

if __name__ == "__main__":
    main()

