"""

HSGconv provides conversion support from/to England's highways standards local grids to OSGB36 EPSG:27700.

Website::

    https://www.brydenwood.co.uk/

Source::

    https://github.com/ccampanile/hsgconv

Bug reports::

    https://github.com/ccampanile/hsgconv/issues

Simple example
--------------

Transform a point's coordinates from local grid (A20) to national grid reference system::

    >>> import hsgconv
    >>> pt = (17573.0093, 398330.8085, 99.425508)
    >>> gp = GridParams(gridID="A20", mean_z=96.98)
    >>> to_nat = ConvertToOSBG(gp, pt[0], pt[1])
    >>> print(to_nat)
    (522569.0642059806, 227241.3842890684)

Bugs
----

Please report any bugs that you find `here <https://gitlab.com/bwtcreativetech/rempy/issues>`_.

License
-------

Released under the GNU GPL v3 license::

   Copyright (C) 2017-2018 Bryden Wood Technology
   Claudio Campanile <ccampanile@brydenwood.co.uk>


"""
#    Copyright (C) 2017-2018 by
#    Claudio Campanile <ccampanile<at>brydenwood.co.uk>
#    All rights reserved.
#    GNU GPL v3 license.
#
# Add platform dependent shared library path to sys.path
#


from .hsgconv import (GridParams, CreateParamList, ConvertToOSBG, ConvertToLocalGrid)