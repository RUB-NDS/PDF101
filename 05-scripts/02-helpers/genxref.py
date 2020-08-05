#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# python standard library
from __future__ import print_function
import argparse, re
from binascii import unhexlify

# ----------------------------------------------------------------------

def usage():
  parser = argparse.ArgumentParser(description="Deflate zipped file.")
  parser.add_argument("filename", help="file to deflate")
  parser.add_argument("-s", "--stream", help="generate xref stream instead of table", action="store_true")
  return parser.parse_args()

# ----------------------------------------------------------------------

def gen_table(doc):
  pass

# ----------------------------------------------------------------------

def gen_stream(doc):
  pass

# ----------------------------------------------------------------------

def main():
  args = usage()
  s = open(args.filename, "rb").read()
  objs = [m.start() for m in re.finditer('\d+ \d+ obj', s)]
  objstms = [m.start() for m in re.finditer('\d+ \d+ obj\s+.*/ObjStm', s)]
  num = str(len(objs)+1)
  last = len(objs)
  xref = re.search('xref', s)
  xref = str(xref.start()) if xref else '0'
  if args.stream: xref = str(objs[-1]) if objs else '0'
  # note: we cannot handle object streams
  if args.stream:
    print(str(last) + " 0 obj")
    print("  << /Type /XRef")
    print("     /W [1 2 1]")
    print("     /Root 1 0 R")
    print("     /Size " + num)
    print("     /Length " + str((last+1)*4))
    print("  >>")
    print("stream")
    print(unhexlify('00000000'), end='')
    for obj in objs:
      print(unhexlify('01' + str(hex(obj)[2:]).zfill(4) + '00'), end='')
      if obj in objstms:
        print(unhexlify('02000100'), end='')
    print("endstream")
    print("endobj")
    print("")
  else:
  # note: we cannot handle unordered objects
    print("xref")
    print("0 " + num)
    print("0000000000 65535 f ")
    for obj in objs: print(str(obj).zfill(10) + " 00000 n ")
    print("trailer")
    print("  << /Root 1 0 R")
    print("     /Size " + num)
    print("  >>")
  print("startxref")
  print(xref)
  print("%%EOF", end='')

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
