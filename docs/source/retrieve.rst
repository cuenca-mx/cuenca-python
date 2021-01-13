Retrieve by id
-------------------
The way for retrieve a transfer is with the ``id``, like this:

.. code-block:: python

    import cuenca

    transfer = cuenca.Transfer.retrieve('tr_123')
