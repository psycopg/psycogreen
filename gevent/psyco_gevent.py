"""A wait callback to allow psycopg2 cooperation with gevent.
"""
# Copyright (C) 2010 Daniele Varrazzo <daniele.varrazzo@gmail.com>

import psycopg2
from psycopg2 import extensions

from gevent.hub import getcurrent, get_hub
from gevent.core import read_event, write_event, EV_TIMEOUT
from gevent.hub import sleep as gevent_sleep

def make_psycopg_green():
    if not hasattr(extensions, 'set_wait_callback'):
        raise ImportError(
            "Support for coroutines is available only from Psycopg 2.2.0")

    extensions.set_wait_callback(gevent_wait_callback)

class Timeout(Exception):
    pass

def gevent_wait_callback(conn, timeout=-1):
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
