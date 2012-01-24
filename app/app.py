# This file is part of the tomobi application. 
#
# Copyright 2011 - Noufal Ibrahim <noufal@nibrahi.net.in>
#
# Licensed under the AGPL - http://www.gnu.org/licenses/agpl.html

import argparse
import datetime
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urlparse


import web
        
urls = (
    '/.*', 'convert'
)
app = web.application(urls, globals())

# def convert_to_mobi(input_file, fname, save_dir = "/home/noufal/tmp/"):
def convert_to_mobi(input_file, fname, save_dir = "/home/noufal/Downloads/kindle"):
    directory = save_dir + datetime.datetime.now().strftime("/%Y/%m/%d/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = "%s/%s.mobi"%(directory, fname)
    cmd = ["/usr/bin/ebook-convert", input_file, output_file, "--title='%s'"%fname, "--output-profile=kindle",  "--pretty-print"]
    print "Ebook conversion command : " + " ".join(cmd)
    with open("/dev/null", "w") as devnull:
        ret = subprocess.call(cmd, stdout = devnull)
    if ret != 0:
        print "Calibre Coversion failed : %s"%input_file
        return False
    else:
        return output_file


def pandoc_covert_to_epub(url):
    epub = tempfile.mktemp(".epub")
    cmd = ["/usr/bin/pandoc", "-f", "html", "-t", "epub", "-o", epub, url]
    print "Pandoc command : " + " ".join(cmd)
    ret = subprocess.call(cmd)
    if ret == 0:
        return epub
    else:
        return False

def lynx_covert_to_text(url):
    output = tempfile.mktemp(".txt")
    cmd = ["/usr/bin/lynx", "-dump", "-nolist", url]
    op = open(output, "w")
    print "Lynx command : " + " ".join(cmd)
    p = subprocess.Popen(cmd, stdout = op)
    ret = p.wait()
    op.close()
    if ret == 0:
        return output
    else:
        return False

def get_filename(url):
    parsed = urlparse.urlparse(url)
    if parsed.path:
        return parsed.path[1:].replace("/","_")
    else:
        return parsed.netloc

def process(filename):
    "This will sanitise the input based on the website and other such criteria"
    print "Processing %s"%filename
    processed_file = filename
    print "Processed file %s"%processed_file
    return filename #TODO: For now, do nothing.
    
def fetch(url):
    workarea = tempfile.mkdtemp()
    cmd = ["/usr/bin/wget", "-nv", "-nd", "-E", "-H", "-k", "-K", "-p", "-t2", url]
    print "Fetching page locally using '%s'"%(" ".join(cmd))
    null = open("/dev/null","w")
    p = subprocess.Popen(cmd, cwd = workarea)
    ret = p.wait()
    filename = glob.glob("%s/*.html"%workarea) or glob.glob("%s/*.php"%workarea)
    if not filename: # TODO: Raise exception here
        print "No parseable filename"
        return workarea, False
    filename = [x for x in filename if x.count("robots") == 0][0] # TODO: Fix this. Glob using the right pattern
    process(filename)
    print "Processed file is ",filename
    null.close()
    return workarea, filename
    

class convert(object):
    def POST(self):
        i = web.input()
        web.header("Content-type", "text/json")
        url = i.get("url")
        if not url:
            return json.dumps(dict(status="bad url"))
        workdir, local_file = fetch(url)
        if not local_file:
            print "Local fetch failed"
            shutil.rmtree(workdir)            
            return json.dumps(dict(status = "failed"))
        ip = pandoc_covert_to_epub(local_file) or lynx_covert_to_text(local_file)
        shutil.rmtree(workdir)
        if not ip:
            print "Initial coversion failed : %s"%url
            ret = False
        else:
            ret = convert_to_mobi(ip, get_filename(url))
            os.unlink(ip)
        if ret:
            print "Completion completed. File placed at %s"%ret
            return json.dumps(dict(file = ret, status = "success"))
        else:
            print "Conversion failed"
            return json.dumps(dict(status = "failed"))


    


if __name__ == "__main__":
    app.run()
