Some testing material to work with Psycopg2 with coroutine_ support.

One of upcoming Psycopg version will have coroutine support. In order to use
them a coroutine framework, such as Eventlet_ or gevent_, should implement a
"wait callback" as an hook to schedule a coroutine switch while a libpq call is
waiting for data.

In this project there are wait callback implementations for a few coroutine
libraries: they are licensed in order to allow their inclusion in the library.

.. _coroutine: http://en.wikipedia.org/wiki/Coroutine
.. _Eventlet: http://eventlet.net/
.. _gevent: http://www.gevent.org/
