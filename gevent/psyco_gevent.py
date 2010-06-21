"""A wait callback to allow psycopg2 cooperation with gevent.

Use `make_psycopg_green()` to enable gevent support in Psycopg.
"""

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
# THE SOFTWARE.

import psycopg2
import psycopg2.extensions

import gevent.socket

def make_psycopg_green():
    """Configure Psycopg to be used with gevent in non-blocking way."""
    if not hasattr(psycopg2.extensions, 'set_wait_callback'):
        raise ImportError(
            "support for coroutines not available in this Psycopg version (%s)"
            % psycopg2.__version__)

    psycopg2.extensions.set_wait_callback(gevent_wait_callback)

def gevent_wait_callback(conn, timeout=None,
        # access these objects with LOAD_FAST instead of LOAD_GLOBAL lookup
        POLL_OK = psycopg2.extensions.POLL_OK,
        POLL_READ = psycopg2.extensions.POLL_READ,
        POLL_WRITE = psycopg2.extensions.POLL_WRITE,
        wait_read = gevent.socket.wait_read,
        wait_write = gevent.socket.wait_write):
    """A wait callback useful to allow gevent to work with Psycopg."""
    while 1:
        state = conn.poll()
        if state == POLL_OK:
            break
        elif state == POLL_READ:
            wait_read(conn.fileno(), timeout=timeout)
        elif state == POLL_WRITE:
            wait_write(conn.fileno(), timeout=timeout)
        else:
            raise psycopg2.OperationalError(
                "Bad result from poll: %r" % state)
