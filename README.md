# Cuenca – Python client library

## Transfers

### Create transfer

```python
import cuenca

cuenca.configure(sandbox=True)  # if using sandbox

transfer = cuenca.Transfer.create(
    account_number='646180157042875763',
    amount=12345,  # Mx$123.45
    descriptor='sending money',  # As it'll appear for the customer
    idempotency_key='unique string',
)

# To get updated status (estado)
transfer.refresh()
```


### Retrieve by `id`

```python
import cuenca

transfer = cuenca.Transfer.retrieve('tr_123')
```

### Query by `idempotency_key` or an `account_number`

```python
import cuenca

transfer = cuenca.Transfer.query(idempotency_key='unique string').one()

transfers = cuenca.Transfer.query(account_number='646180157000000004')
```

## Api Keys

### Roll the `ApiKey`

```python
import cuenca

# create new key and deactive old key in 60 mins
old_key, new_key = cuenca.ApiKey.roll(60)
```
