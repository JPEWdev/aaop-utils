# American Academy of Orthotists and Prosthetist (AAOP) File Utilities

A set of python utilities for dealing with AAOP data files.

The data file format was reverse engineered from a single data file, so there
are many parts of the format that serve an unknown purpose.

After installing, the program `aaopcnvt` can be used to convert an AAOP file
(usually with a .aop extension) to a more standard format. Currently, the
only supported destination format is Wavefront object (.obj).

