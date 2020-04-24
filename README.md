# Cuenca – Python client library

## Transfers

### Create transfer

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


### Retrieve by `id`

```python
from cuenca import Client

client = Client()
transfer = client.transfers.retrieve('tr_123')
```

### Query by `idempotency_key` or an `account_number`

```python
from cuenca import Client

client = Client()
transfer = client.transfers.query(idempotency_key='unique string')[0]

transfers = client.transfers.query(account_number='646180157000000004')
```

## Api Keys

## Roll the `ApiKey`

```python
from cuenca import Client

client = Client()

# create new key and deactive old key in 60 mins
old_key, new_key = client.api_keys.roll(60)
```
