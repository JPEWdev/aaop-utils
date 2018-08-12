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
import logging

logger = logging.getLogger('AAOP')

class InvalidFormat(Exception):
    pass

class AAOPFile(object):
    """
    AAOP file. Currently only cylindrical formats are supported.

    The file format is reverse engineered from a single data file, so there are
    several fields that are of unknown purpose.

    The cylindrical file format records a number of "stacks". Each stack
    specifies a set of points that share a Z coordinate. Each stack has a
    fixed number of "spokes". Each spoke a number that indicates the linear
    distance from center of the stack. Spokes are equally distributed around
    the stack.

    In mathematical cylindrical geometry, the stack defines the Z coordinate,
    the spoke length is rho, and phi can be calculated by evenly dividing the
    spokes over 2 pi.
    """
    def __init__(self, aaop):
        def get_line():
            while True:
                yield next(aaop).rstrip()

        def next_line():
            return next(get_line())

        self.version = next_line()
        if self.version != 'AAOP1':
            raise InvalidFormat('Unknown Version "%s"' % self.version)

        self.comments = []

        for l in get_line():
            self.comments.append(l)
            if l == 'END COMMENTS':
                break

        self.fmt = next_line()
        unknown1 = next_line()
        unknown2 = next_line()
        self.num_spokes = int(next_line())
        unknown3 = next_line()
        self.num_stacks = int(next_line())
        unknown4 = next_line()

        logger.info('format = %s', self.fmt)
        logger.info('unknown1 = %s', unknown1)
        logger.info('unknown2 = %s', unknown2)
        logger.info('number of spokes = %d', self.num_spokes)
        logger.info('unknown3 = %s', unknown3)
        logger.info('number of stacks = %d', self.num_stacks)
        logger.info('unknown4 = %s', unknown4)

        if self.fmt != 'CYLINDRICAL':
            raise InvalidFormat('Unknown format "%s"' % self.fmt)

        self.stacks = []
        for i in range(self.num_stacks):
            self.stacks.append(float(next_line()))

        self.spokes = []
        for stack in range(self.num_stacks):
            d = []
            for spoke in range(self.num_spokes):
                d.append(float(next_line()))
            self.spokes.append(d)

