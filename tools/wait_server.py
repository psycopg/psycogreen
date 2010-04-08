#!/usr/bin/env python
"""A server to test with blocking I/O."""

# Copyright (C) 2010 Daniele Varrazzo <daniele.varrazzo@gmail.com>
# and licensed under the MIT license:
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.import time

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

def wait_app(environ, start_response):
    """An application serving blocking pages."""
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)
    try:
        secs = int(environ['PATH_INFO'].replace('/', ''))
    except:
        secs = 0

    time.sleep(secs)
    return [ str(secs) ]

httpd = make_server('', 8000, wait_app)
print "Serving on port 8000..."
httpd.serve_forever()

