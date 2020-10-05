Query by idempotency_key, account_number and status
---------------------------------------------------------------

Results are always returned in descending order of ``created_at``

the methods that  can be used:

* ``one()`` - returns a single result. Raises ``NoResultFound`` if there are no results and ``MultipleResultsFound`` if there are more than one.

* ``first()`` - returns the first result or ``None`` if there aren't any.

* ``all()`` - returns a generator of all matching results. Pagination is handled automatically as you iterate over the response.

* ``count()`` - returns an integer with the count of the matching results.


You can use like this example:

.. code-block:: python

    import cuenca
    from cuenca.types import Status

    # find the unique transfer using the idempotency key
    local_transfer_id = '078efdc20bab456285437309c4b75673'
    transfer = cuenca.Transfer.one(idempotency_key=local_transfer_id)

    # returns a generator of all succeeded transfers to the specific account
    transfers = cuenca.Transfer.all(
        account_number='646180157000000004',
        status=Status.succeeded
    )

    # the total number of succeeded transfers
    count = cuenca.Transfer.count(status=Status.succeeded)
