"""A wait callback to allow psycopg2 cooperation with eventlet.
"""
# Copyright (C) 2010 Daniele Varrazzo <daniele.varrazzo@gmail.com>

import psycopg2
from psycopg2 import extensions

from eventlet.hubs import trampoline

def make_psycopg_green():
    if not hasattr(extensions, 'set_wait_callback'):
        raise ImportError(
            "Support for coroutines is available only from Psycopg 2.2.0")

    extensions.set_wait_callback(eventlet_wait_callback)

def eventlet_wait_callback(conn, timeout=-1):
    while 1:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        elif state == extensions.POLL_READ:
            trampoline(conn.fileno(), read=True)
        elif state == extensions.POLL_WRITE:
            trampoline(conn.fileno(), write=True)
        else:
            raise psycopg2.OperationalError(
                "Bad result from poll: %r" % state)
