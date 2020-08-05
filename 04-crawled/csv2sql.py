#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python standard library
import csv, argparse, sqlite3

# -------------------------------------------------------------------------------------------------

def usage():
  parser = argparse.ArgumentParser(description="Convert CSF file to SQLite database")
  parser.add_argument("infile", help="Input CSV file")
  parser.add_argument("outfile", help="Output database")
  return parser.parse_args()

# -------------------------------------------------------------------------------------------------

def main():
  args = usage()
  # connect to database
  con = sqlite3.connect(args.outfile, timeout=30.0)
  con.text_factory = str
  cur = con.cursor()
  # create table
  create_table(cur)
  with open(args.infile, 'r', newline='') as csvfile:
    # parse csv input
    data = csv.reader(csvfile, delimiter='|', quotechar='`')
    # insert record into table
    #for row in data: print(row)
    try:
      for row in data: cur.execute("INSERT INTO data VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [None]+row)
    except: print(row)
    # commit any changes to database
  # commit any changes to database
  con.commit()
  # close connection to database
  con.close()

# -------------------------------------------------------------------------------------------------

def create_table(cur):
  cur.execute("""CREATE TABLE data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    md5sum TEXT,
                    launch1 INTEGER,
                    thread1 INTEGER,
                    goto1 INTEGER,
                    gotoe1 INTEGER,
                    gotor1 INTEGER,
                    fdf1 INTEGER,
                    submit1 INTEGER,
                    uri1 INTEGER,
                    sound1 INTEGER,
                    movie1 INTEGER,
                    launch2 INTEGER,
                    thread2 INTEGER,
                    goto2 INTEGER,
                    gotoe2 INTEGER,
                    gotor2 INTEGER,
                    fdf2 INTEGER,
                    submit2 INTEGER,
                    uri2 INTEGER,
                    sound2 INTEGER,
                    movie2 INTEGER,
                    pdf_author TEXT,
                    pdf_creator TEXT,
                    pdf_producer TEXT,
                    pdf_created TEXT,
                    pdf_modified TEXT,
                    xmp_author TEXT,
                    xmp_creator TEXT,
                    xmp_producer TEXT,
                    xmp_created TEXT,
                    xmp_modified TEXT,
                    url TEXT
                    )""")

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
  main()
