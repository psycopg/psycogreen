psycogreen -- integrate psycopg2 with coroutine libraries
=========================================================

Since `release 2.2`__, `Psycopg`_ offers `coroutines support`__.

Psycopg is a C extension module, so it can't be monkey-patched to be
coroutine-friendly. Instead it now exposes `a hook`__
where a coroutine library can install its wait code. Psycopg will call the
hook whenever it executes a libpq call that may block. Coroutine libraries can
implement their "wait callaback" in order to have a chance to schedule a
coroutine switch.

The psycogreen package is a contained of callbacks to make psycopg2 work with
coroutine libraries, using asynchronous calls internally but offering a
blocking interface so that regular code can run unmodified.


.. _Psycopg: http://initd.org/psycopg/
.. __: http://initd.org/psycopg/articles/2010/05/16/psycopg-220-released/
.. __: http://initd.org/psycopg/docs/advanced.html#support-to-coroutine-libraries
.. __: http://initd.org/psycopg/docs/extensions.html#psycopg2.extensions.set_wait_callback


Eventlet
--------

`Eventlet`_ support Psycopg out-of-the-box: Psycopg can be patched together
with the standard library: see `the documentation`__.

.. _Eventlet: http://eventlet.net/
.. __: http://eventlet.net/doc/patching.html#monkeypatching-the-standard-library


gevent
------

A wait callback implementation for `gevent`_ is provided here: check
`psyco_gevent.py`__ and this `test example`__.

.. _gevent: http://www.gevent.org/
.. __: https://bitbucket.org/dvarrazzo/psycogreen/src/tip/gevent/psyco_gevent.py
.. __: https://bitbucket.org/dvarrazzo/psycogreen/src/tip/gevent/test_gevent.py


uWSGI green threads
-------------------

Roberto De Ioris is writing uGreen__, a green thread implementation on top of
the `uWSGI async platform`__.

.. __: http://projects.unbit.it/uwsgi/wiki/uGreen
.. __: http://projects.unbit.it/uwsgi/

He has performed some tests using both `psycopg2 async support`__ and
`psycopg2 green support`__ and has reported no problem in their stress tests
with both the async styles.

.. __: http://projects.unbit.it/uwsgi/browser/tests/psycopg2_green.py
.. __: http://projects.unbit.it/uwsgi/browser/tests/psycogreen_green.py

