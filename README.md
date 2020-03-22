# Cuenca – Python client library

## Create transfer

```python
from cuenca import Client

client = Client()
transfer = client.transfers.create(
    clabe='646180157042875763',
    amount=12345,  # Mx$123.45
    descriptor='sending money',  # As it'll appear for the customer
    idempotency_key='unique string',
)

# To get updated status (estado)
transfer.refresh()
```


## Retrieve by `id`

```python
from cuenca import Client

client = Client()
transfer = client.transfers.retrieve('tr_123')
```

## Retrieve by `idempotency_key`

```python
from cuenca import Client

client = Client()
transfer = client.transfers.list(idempotency_key='unique string')[0]
```