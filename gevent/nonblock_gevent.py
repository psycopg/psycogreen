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
        logger.info("fetch %d start", i)
        cur.execute("select pg_sleep(%s)", (secs,))
        logger.info("fetch %d end", i)

logger.info("making jobs")
jobs = [
    gevent.spawn(download, 2, 3),
    gevent.spawn(fetch, 3, 2),
    ]

logger.info("join begin")
gevent.joinall(jobs)
logger.info("join end")

