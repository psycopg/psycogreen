#!/usr/bin/env python
"""A server to test with blocking I/O."""

# Copyright (C) 2010-2012 Daniele Varrazzo <daniele.varrazzo@gmail.com>
# All rights reserved.  See COPYING file for details.

import time
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

