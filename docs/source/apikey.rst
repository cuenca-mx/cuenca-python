Api Keys
==============

Cuenca-python allows you to create, activate and deactivate api keys.
The example below shows you how to create an api key and how to disable the old one.

.. code-block:: python

    import cuenca

    # Create new ApiKey
    new = cuenca.ApiKey.create()

    # Have to use the new key to deactivate the old key
    old_id = cuenca.session.auth[0]
    cuenca.session.configure(new.id, new.secret)
    cuenca.ApiKey.deactivate(old_id, 60)  # revoke prior API key in an hour


Nota:
deactivate an ``ApiKey`` in a certain number of minutes. If minutes is
negative, the API will treat it the same as 0. You can't deactivate
the same key with which the client is configured, since that'd risk
locking you out. The deactivated key is returned so that you have the
exact deactivated_at time.
