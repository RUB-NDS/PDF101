#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# python standard library
from __future__ import print_function
import argparse, zlib

# ----------------------------------------------------------------------

def usage():
  parser = argparse.ArgumentParser(description="Deflate zipped file.")
  parser.add_argument("filename", help="file to deflate")
  parser.add_argument("-x", "--extract", help="uncompress file instead of deflating", action="store_true")
  return parser.parse_args()

# ----------------------------------------------------------------------

def main():
  args = usage()
  s = open(args.filename, "rb").read()
  if args.extract:
    s = s.strip('\r\n')
    print(zlib.decompress(s), end='')
  else:
    print(zlib.compress(s), end='')

# ----------------------------------------------------------------------

# clean exit
if __name__ == '__main__':
  try:
    main()
  # catch CTRL-C
  except (KeyboardInterrupt):
    pass
  finally:
    print("")
