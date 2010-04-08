#!/usr/bin/env python
"""A test to verify Psycopg collaboration with other blocking I/O.

Please run the script ``tools/wait_server.py`` in a separate shell to make the
test work.

If the test works you should see download tasks overlapping query tasks.
"""

# Copyright (C) 2010 Daniele Varrazzo <daniele.varrazzo@gmail.com>
#
#  This module is licensed under the MIT license:
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import psyco_gevent
psyco_gevent.make_psycopg_green()

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

