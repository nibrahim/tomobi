Mobify plugin for Chrome
========================

This is a chrome plugin and a tiny backend [web.py](http://webpy.org) based webapp to convert web pages into [`.mobi`](http://wiki.mobileread.com/wiki/MOBI) files that can be read on an Amazon Kindle ebook reader.

Rationale
---------

There are a few excellent plugins (e.g. [send to kindle](https://chrome.google.com/webstore/detail/ipkfnchcgalnafehpglfbommidgmalan)) out there that do this kind of thing using an online service and Amazon's conversion service.

Being a little paranoid about privacy and such things myself, I wanted a system that didn't rely on using a 3rd party service and Amazon's conversion service which keeps track of all documents converted. 

This program and the conversion service is completely on ones own computer and so is "self contained". 

Components
----------

There is a chrome plugin (extension.crx) which you can install into your Chrome browser. A little button will pop up next to your URL bar which you can click on a page to have it rendered into a `.mobi` file that you can drop onto your Kindle to read. 

There is also a "back end" server which you need to run to actually do the conversions. This is a python app that uses `web.py` so you need to install that inside a virtualenv and then start the server (refer Installation section below).

The actual work of conversion is accomplished using [pandoc](https://github.com/jgm/pandoc), [lynx](http://lynx.isc.org/), [Calibre](http://calibre-ebook.com/) and so you need these three programs installed as well.

Installation
------------

This whole thing is not tinker free and needs some time and tinkering to setup. Please fork the project and send it a pull request if you can improve it in any way. It currently "works for me". 

1. Install `pandoc`, `lynx` and `calibre`. On Debian, you can do this using 

    sudo apt-get install pandoc lynx calibre

1. Install `python` using `apt-get install python`
1. Install `virtualenv` using `apt-get install python-virtualenv`
1. Create a virtualenv using `virtualenv ~/mobify`.
1. Activate this virtualenv and install `web.py` inside it using `. ~/mobify/bin/activate` and then `pip install web.py`. 
1. Checkout the `mobify` app and edit the `app.py` file inside the `app` directory. In the line that says `def convert_to_mobi(input_file, fname, save_dir = "/home/noufal/Downloads/kindle")`, edit the `save_dir` parameter to indicate where you want the `.mobi` files to be generated.
1. Start the web server using `python app.py 9090`. You need to run this while the `virtualenv` is *activated*.
1. Load the `extension.crx` in Chrome to make it install it. 
1. Now the `.mobi` button should show up for you to use. Click on it while on some page and you should be able to see debug output on the terminal where the python app is running. 

Please report issues to me. 

Usage
-----

Once you get the setup above working, using the system is just a button click. Your files will get created in the save directory and you can put them onto your kindle when you want. 

The backend doesn't do much sanitisation so if you have a version of the page that is formatted for print, please convert that instead of the web version. You will probably get better results. 

Roadmap
-------

I plan to optimise the backend for sites that I usually need to get content from so that I get better conversions. 

License
-------

The backend app and the plugin are licensed under the [AGPL](http://www.gnu.org/licenses/agpl.html). 
