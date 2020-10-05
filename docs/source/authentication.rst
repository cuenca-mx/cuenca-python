Authentication
==============

Configure the client
--------------------

Cuenca-python has configurations values, with sensible defaults. The authentication has a configure the credentials for the
client, the way to configure is to set the :file:`CUENCA_API_KEY` and :file:`CUENCA_API_SECRET` environment variables.
The client library will automatically configure based on the values of those variables.

To configure manually:

.. code-block:: python

    import cuenca

    cuenca.configure(api_key='PKxxxx', api_secret='yyyyyy')
