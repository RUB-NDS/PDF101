#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################################################################
# stream.py: generate testcases for external streams wihtin xobjects #
######################################################################

# python standard library
import re, argparse

# local helper classes
from helper import obfuscate, rand_uuid
from config import domain

# ----------------------------------------------------------------------

# uri schemes and protocols that may be handled
uri_schemes = [
  'http://', 'https://', 'ftp://', 'file:///net/', '\\\\', '\\\\\\\\', 'mailto:stream@', 'telnet://', 'news://', 'smb://', 'afp://', 'view-source:http://', 'file://http://', ''
]

# ======================================================================

##############################################################
# testcases for external stream based backchannel techniques #
##############################################################

# external streams (Adobe-PDF 1.7, page 348)
def xobject(num, url):
  return ['''
  << /Length 47 >>
stream
  q
  100 0 0 100 100 400 cm
  /X''' + str(num).zfill(6) + ''' Do
  Q
endstream
''',
'''
  << /Type /XObject
     /Subtype /Image
     /Width 500
     /Height 500
     /BitsPerComponent 8
     /ColorSpace /DeviceRGB
     /FFilter /DCTDecode
     /F << /FS /URL
           /F (''' + url + ''')
        >>
     /Length 0 % do *not* remove this and stream/endstream
  >>
stream
endstream
'''
###################################################################
# TBD: there are some more variants like Unicode strings: /UF (…) #
# and OS depended entries: /F << /DOS <…> /Unix <…> /Mac <…> >>   #
###################################################################
]

# ----------------------------------------------------------------------

# wrap payloads into minimal pdf file
def wrap(payloads):
  # standard objects for doc structure
  structure = [
  # catalog object
  '''
  << /Type /Catalog
     /Pages 2 0 R''' + (('''
     /URI << /Base (''' + args.b + ''') /Type /URI >>''') if args.b else '') + '''
  >>\n''',
  # pages object
  '''
  << /Type /Pages
     /Kids [3 0 R]
     /Count 1
     /MediaBox [0 0 595 842]
  >>\n''',
  # page object
  '''
  << /Type /Page
     /Parent 2 0 R
     /Resources
      << /Font
          << /F1
              << /Type /Font
                 /Subtype /Type1
                 /BaseFont /Courier
              >>
          >>
         /XObject << '''+ ('\n'+21*' ').join(['/X' + str(count).zfill(6) + ' ' + str(count) + ' 0 R' for count in range(6, len(payloads) + 5, 2)]) +''' >>
      >>
     /Contents ['''+ ('\n'+16*' ').join([str(count) + ' 0 R' for count in [4] + list(range(5, len(payloads) + 5, 2))]) +''']
  >>\n''',
  # testcase object
  '''
  << /Length 67 >>
stream
  BT
    /F1 22 Tf
    30 800 Td
    (Testcase: ''' + ("'stream'").ljust(10) + ''') Tj
  ET
endstream\n''']
  # obfuscate payloads
  objects = structure + payloads
  objects = [obfuscate(obj, args) for obj in objects]
  # create minimal pdf file
  doc = '%PDF-' + args.v + '\n\n'
  obj_offset = len(doc)
  objects = [str(num+1) + ' 0 obj' + obj + 'endobj\n\n' for num, obj in enumerate(objects)]
  for obj in objects: doc += obj
  xref_offset = str(len(doc))
  doc += 'xref\n0 ' + str(len(objects)+1) + '\n0000000000 65535 f '
  for obj in objects:
    doc += '\n' + str(obj_offset).zfill(10) + ' 00000 n '
    obj_offset = obj_offset + len(obj)
  doc += '\ntrailer\n  << /Root 1 0 R\n     /Size ' + str(len(objects)+1) + '\n  >>'
  doc += '\nstartxref\n' + xref_offset + '\n%%EOF'
  print(doc)

# ----------------------------------------------------------------------

def usage():
  parser = argparse.ArgumentParser(description="Create PDF file to test for external streams")
  parser.add_argument("-v", metavar="version", default='1.7', help="PDF version used (default: 1.7)")
  parser.add_argument("-b", metavar="base", help="set a base URI for PDF document")
  parser.add_argument("-o", help="obfuscate (octal and linefeeds)", action="store_true")
  parser.add_argument("-x", help="obfuscate (hex and whitespaces)", action="store_true")
  return parser.parse_args()

# ----------------------------------------------------------------------

def main():
  global args; args = usage()

  counter = 6
  payloads_stream = []
  for scheme in uri_schemes:
    name = ''.join(re.findall("[a-zA-Z]+", scheme))
    payloads_stream += xobject(counter, scheme+rand_uuid()+'.'+name+'.stream.'+domain+'/0')
    counter = counter + 2
  wrap(payloads_stream)

# ----------------------------------------------------------------------

if __name__ == '__main__': main()
