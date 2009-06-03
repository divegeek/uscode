#!/usr/bin/env python

"""
A trivial utility to retrieve the US Code
"""

import httplib
import os
import re
import sys
import tempfile
import zipfile

def ensure_dir_exists(dirname):
    """
    Make sure dirname exists.
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def extract_title(conn, title_name, code_dir):
    """
    Download one title, unzip it, convert the WordPerfect files to
    wrapped text and write them into title_dir.
    """
    conn.request('GET', '/download/pls/Title_%s.ZIP' % (title_name))
    rsp = conn.getresponse()
    if rsp.status != 200:
        rsp.read()
        conn.request('GET', '/download/pls/%s.zip' % (title_name))
        rsp = conn.getresponse()
        assert rsp.status == 200
        

    zip_file = tempfile.TemporaryFile()
    zip_file.write(rsp.read())

    # Retrieved data should be a zip file.  Process each entry.
    zip_obj = zipfile.ZipFile(zip_file)

    for entry in zip_obj.infolist():
        # Extract entry content into destination file
        out_path = get_out_path(code_dir, entry.filename)
        print "Processing", entry.filename, "to", out_path
        out_file = open(out_path, "wt+")
        out_file.write(zip_obj.read(entry.filename))
        out_file.close()

    zip_file.close()                    # Temp file also disappears

name_map = {
    "05app.txt" : "Title_05_appendix.txt",
    "11a.txt"   : "Title_11.txt",
    "160.wtx"   : "Title_16.txt",
    "170.wtx"   : "Title_17.txt",
    "180.wtx"   : "Title_18.txt",
    "18a.txt"   : "Title_18_appendix.txt",
    "190.wtx"   : "Title_19.txt",
    "200.wtx"   : "Title_20.txt",
    "220.wtx"   : "Title_22.txt",
    "230.wtx"   : "Title_23.txt",
    "240.wtx"   : "Title_24.txt",
    "250.wtx"   : "Title_25.txt",
    "28a.txt"   : "Title_28_appendix.txt",
    "501.txt"   : "Title_50_appendix.txt"
    }

def get_out_path(code_dir, file_name):
    """
    Construct output path name
    """
    ensure_dir_exists(os.path.join(code_dir))
    if name_map.has_key(file_name):
        file_name = name_map[file_name]
    return os.path.join(code_dir, file_name)

def extract_titles(dest_dir):
    """
    Extract all titles of US Code
    """
    title_list = [ "%02d" % i for i in range(1, 51) if i != 34 ]

    conn = httplib.HTTPConnection('uscode.house.gov')
    dest_dir = os.path.join(dest_dir, 'code')
    extract_title(conn, "organiclaws", dest_dir)
    for title in title_list:
        extract_title(conn, title, dest_dir)
    conn.close()

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print "Usage: retrive_code <dest_path>"
        exit(1)

    extract_titles(sys.argv[1])
        
