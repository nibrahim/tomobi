import datetime
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
    directory = save_dir + datetime.datetime.now().strftime("/%Y/%m/%d/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = "%s/%s.mobi"%(directory, fname)
    cmd = ["/usr/bin/ebook-convert", input_file, output_file]
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
    

class convert(object):
    def POST(self):
        i = web.input()
        web.header("Content-type", "text/json")
        url = i.get("url")
        if not url:
            return json.dumps(dict(status="bad url"))
        ip = pandoc_covert_to_epub(url) or lynx_covert_to_text(url)
        if not ip:
            print "Initial coversion failed : %s"%url
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
