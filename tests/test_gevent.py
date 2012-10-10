#!/usr/bin/env python
"""A test to verify Psycopg collaboration with other blocking I/O.

Please run the script ``tools/wait_server.py`` in a separate shell to make the
test work.

If the test works you should see download tasks overlapping query tasks.
"""

# Copyright (C) 2010-2012 Daniele Varrazzo <daniele.varrazzo@gmail.com>
# All rights reserved.  See COPYING file for details.


import gevent
import gevent.monkey
gevent.monkey.patch_all()

import psycogreen.gevent
psycogreen.gevent.patch_psycopg()

import urllib2  # green

import psycopg2

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger()
logger.info("testing psycopg2 with gevent")

conn = psycopg2.connect("dbname=postgres")

def download(num, secs):
    url = "http://localhost:8000/%d/" % secs
    for i in range(num):
        logger.info("download %d start", i)
        data = urllib2.urlopen(url).read()
        logger.info("download %d end", i)

def fetch(num, secs):
    cur = conn.cursor()
    for i in range(num):
        logger.info("query %d start", i)
        cur.execute("select pg_sleep(%s)", (secs,))
        logger.info("query %d end", i)

logger.info("making jobs")
jobs = [
    gevent.spawn(download, 2, 3),
    gevent.spawn(fetch, 3, 2),
    ]

logger.info("join begin")
gevent.joinall(jobs)
logger.info("join end")

