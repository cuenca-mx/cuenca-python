Transfers
==============

Create transfer
--------------------
In cuenca-python you can create transfers, something like this:

.. code-block:: python

    import cuenca

    cuenca.configure(sandbox=True)  # if using sandbox

    local_transfer_id = '078efdc20bab456285437309c4b75673'

    transfer = cuenca.Transfer.create(
        recipient_name='Benito Juárez',
        account_number='646180157042875763',  # CLABE or card number
        amount=12345,  # Mx$123.45
        descriptor='sending money',  # As it'll appear for the customer
        idempotency_key=local_transfer_id
    )

    # To get updated status
    transfer.refresh()


You can enable sandbox if you using this.

To create a transfer the following parameters are necessary:

===================== ==========================================
``account_number:``   CLABE
``amount:``           needs to be in centavos (not pesos)
``descriptor:``       how it'll appear for the recipient
``recipient_name:``   name of recipient
``idempotency_key:``  must be unique for each transfer to avoid duplicates
===================== ==========================================

The recommended idempotency_key scheme:

1. Create a transfer entry in your own database with the status created.


2. Call this method with the unique id from your database as the ``idempotency_key``.


3. Update your database with the status created or submitted after receiving a response from this method.
