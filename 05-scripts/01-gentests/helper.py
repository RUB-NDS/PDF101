# -*- coding: utf-8 -*-

# python standard library
import re, uuid, random

#####################################
# generate random 8b uuid for tests #
#####################################
def rand_uuid():
  return str(uuid.uuid4()).replace('-', '')[:8]

#####################################
# oct: (\163\\n\150\145\\n\154\154) #
#####################################
def ooct(s):
  # convert string to octal list
  l = ['\\' + (oct(ord(c)).zfill(4))[2:] for c in s]
  # insert newlines at random
  s = ''.join([t + '\\\n' if (random.randint(0,2) == 0) else t for t in l])
  s = '(' + s + ')'
  return s

#####################################
# hex: <68 656c  6c 6f>             #
#####################################
def ohex(s):
  # convert string to hexdecimal
  s = s.encode('utf-8').hex()
  # insert whitespaces at random
  s = ''.join(t.ljust(random.randint(0,4)) for t in [s[i:i+2] for i in range(0,len(s),2)])
  s = '<' + s + '>'
  return s

#####################################
# str: (hello)                      #
#####################################	
def obfuscate(payload, args):
  # poor man's obfuscation (will break stuff!)
  inner = re.compile('(\(([^()]+)\))') # match parentheses
  if args.o: payload = re.sub(inner, lambda m: ooct(m.group(2)), payload)
  if args.x: payload = re.sub(inner, lambda m: ohex(m.group(2)), payload) 
  return payload

##################################################################################################
# TBD: further obfuscation techniques such as URL encoding, `A New Era of SSRF', stream encoding #
#      (/FlateDecode, ASCIIHexDecode, LZWDecode, …), Name representation (/#FF), PDF Encryption, #
#      XDP, countless ways of JS encoding (hex/eval/unescape/…)                                  #
##################################################################################################
