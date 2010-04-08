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
from psycopg2 import extensions

from gevent.hub import getcurrent, get_hub
from gevent.core import read_event, write_event, EV_TIMEOUT
from gevent.hub import sleep as gevent_sleep

def make_psycopg_green():
    """Configure Psycopg to be used with gevent in non-blocking way."""
    if not hasattr(extensions, 'set_wait_callback'):
        raise ImportError(
            "support for coroutines not available in this Psycopg version (%s)"
            % psycopg2.__version__)

    extensions.set_wait_callback(gevent_wait_callback)

class Timeout(Exception):
    pass

def gevent_wait_callback(conn, timeout=-1):
    """A wait callback useful to allow gevent to work with Psycopg."""
    while 1:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        elif state == extensions.POLL_READ:
            wait_read(conn.fileno(), timeout=timeout)
        elif state == extensions.POLL_WRITE:
            wait_write(conn.fileno(), timeout=timeout)
        else:
            raise psycopg2.OperationalError(
                "Bad result from poll: %r" % state)

def _wait_helper(ev, evtype):
    current = ev.arg
    if evtype & EV_TIMEOUT:
        current.throw(Timeout())
    else:
        current.switch(ev)

def wait_read(fileno, timeout=-1):
    evt = read_event(fileno, _wait_helper, timeout, getcurrent())
    try:
        switch_result = get_hub().switch()
        assert evt is switch_result, 'Invalid switch into wait_read(): %r' % (switch_result, )
    finally:
        evt.cancel()


def wait_write(fileno, timeout=-1):
    evt = write_event(fileno, _wait_helper, timeout, getcurrent())
    try:
        switch_result = get_hub().switch()
        assert evt is switch_result, 'Invalid switch into wait_write(): %r' % (switch_result, )
    finally:
        evt.cancel()
