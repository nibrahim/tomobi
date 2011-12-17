import json
import os
import subprocess
import tempfile
import urlparse

import web
        
urls = (
    '/.*', 'convert'
)
app = web.application(urls, globals())

def convert_to_mobi(input_file, fname, save_dir = "/home/noufal/Downloads/kindle"):
    output_file = "%s/%s.mobi"%(save_dir, fname)
    cmd = ["/usr/bin/ebook-convert", input_file, output_file]
    print cmd
    ret = subprocess.call(cmd)
    if ret != 0:
        print "Calibre Coversion failed : %s"%input_file
        return False
    else:
        return output_file


def pandoc_covert_to_epub(url):
    epub = tempfile.mktemp(".epub")
    cmd = ["/usr/bin/pandoc", "-f", "html", "-t", "epub", "-o", epub, url]
    print cmd
    ret = subprocess.call(cmd)
    if ret == 0:
        return epub
    else:
        return False

def lynx_covert_to_text(url):
    output = tempfile.mktemp(".txt")
    cmd = ["/usr/bin/lynx", "-dump", "-nolist", url]
    op = open(output, "w")
    print cmd
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
    

class convert(object):
    def POST(self):
        i = web.input()
        url = i["url"]
        print "Coverting %s"%url
        ip = pandoc_covert_to_epub(url) or lynx_covert_to_text(url)
        if not ip:
            print "Initial coversion failed : %s"%url
        else:
            ret = convert_to_mobi(ip, get_filename(url))
            os.unlink(ip)
        if ret:
            return json.dumps(dict(file = ret, status = "success"))
        else:
            return json.dumps(dict(status = "failed"))

            

if __name__ == "__main__":
    app.run()
