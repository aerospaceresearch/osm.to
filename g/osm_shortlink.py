# osm_shortlink.py - MAximillian Dornseif 2013 - Public Domain
# see http://wiki.openstreetmap.org/wiki/Shortlink
# https://github.com/openstreetmap/openstreetmap-website/blob/master/lib/short_link.rb
# and makeShortCode in
# https://github.com/openstreetmap/openstreetmap-website/blob/master/app/assets/javascripts/application.js

# array of 64 chars to encode 6 bits. this is almost like base64 encoding, but
# the symbolic chars are different, as base64's + and / aren't very
# URL-friendly.

################## extension convert shortlink to geo loc
# def _decode(shortLink):
        """generate interleved code from String"""   

# def _deinterleave(codeEndcode):
        """split 64 bit integer to two 32 bit integers"""

# next steps
# deal with trailing "-" character
# 


########### end comment extension

ARRAY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_~'

import math

def short_osm(lat, lon, zoom=16):
    """Return a short link representing a location in OpenStreetmap.

    Provide coordinates and optional zoom level. e.g.:

    >>> short_osm(50.671530961990356, 6.09715461730957)
    http://osm.org/go/0GAjIv8h
    >>> short_osm(0, 0, 3)
    http://osm.org/go/wAAA--
    >>> short_osm(0, 0, 4)
    http://osm.org/go/wAAA
    """
    return 'http://osm.org/go/' + _encode(lat, lon, zoom)


def _encode(lat, lon, z):
    """given a location and zoom, return a short string representing it."""
    x = int((lon + 180.0) * 2**32 / 360.0)
    y = int((lat +  90.0) * 2**32 / 180.0)
    code = _interleave(x, y)
    str = ''
    # add eight to the zoom level, which approximates an accuracy of
    # one pixel in a tile.
    #print("code",code )

    for i in range(int(math.ceil((z + 8) / 3.0))):
        digit = (code >> (56 - 6 * i)) & 0x3f;
        print("(56 - 6 * i)", (56 - 6 * i))
        print("code shifted",(code >> (56 - 6 * i)) )
        str += ARRAY[digit]
        print("str", str)
    # append characters onto the end of the string to represent
    # partial zoom levels (characters themselves have a granularity
    # of 3 zoom levels).
    _decode(str)
    for i in range((z + 8) % 3):
        str += "-"
    return str

def _decode(shortLink):
        """generate interleved code from String"""    
        codeEndcode = 0
        for i in range(len(shortLink)):
            print(shortLink[i])
            print("array index", ARRAY.index(shortLink[i]))
            tmp = ARRAY.index(shortLink[i])
            codeEndcode = ((codeEndcode<<6) | (tmp))
            print(codeEndcode)
            return codeEndcode

def _deinterleave(codeEndcode):
        """split 64 bit integer to two 32 bit integers"""
        x = 0
        y = 0
        shift = 2^64
        for i in range(64,0,-2):
            tmp = (codeEndcode >> i) & 1
            x = ((x | tmp)  << 1)
            tmp = (codeEndcode >> (i-1)) & 1
            y = ((y | tmp)  << 1)            
           # x = x << 1
            print( ((codeEndcode ) & (2**i )))
            print("codeEndcode << i",codeEndcode << i)
            print("x",x << 1)
        return x, y




def _interleave(x, y):
    """combine 2 32 bit integers to a 64 bit integer"""
    c = 0
    for i in range(31, 0, -1):
      c = (c << 1) | ((x >> i) & 1)
      c = (c << 1) | ((y >> i) & 1)
    #   print("x",bin(x))
    #   print("y",bin(y))
    #   print("c",bin(c))
    return c


if __name__ == '__main__':
    # testing
    _deinterleave(3753759947717361664)
  #  _decode("0GAjIv8h")
    print (short_osm(50.671530961990356, 6.09715461730957))
    print (short_osm(50.671530961990356, 6.09715461730957, 10))
    print (short_osm(50.671530961990356, 6.09715461730957, 5))
    print (short_osm(50.671530961990356, 6.09715461730957, 4))
    print (short_osm(0, 0, 4))
    print (short_osm(0, 0, 3))

