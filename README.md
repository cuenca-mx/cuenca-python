# Cuenca – Python client library

## Transfers

### Create transfer

```python
import cuenca

cuenca.configure(sandbox=True)  # if using sandbox

transfer = cuenca.Transfer.create(
    recipient_name='Benito Juárez',
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

### Query by `idempotency_key`, `account_number` and `status`

Results are always returned in descending order of `created_at`

The methods that can be used:
- `one()` - returns a single result. Raises `NoResultFound` if there are no
results and `MultipleResultsFound` if there are more than one
- `first()` - returns the first result or `None` if there aren't any
- `all()` - returns a generator of all matching results. Pagination is handled
automatically as you iterate over the response
- `count()` - returns an integer with the count of the matching results

```python
import cuenca
from cuenca.types import Status

# find the unique transfer using the idempotency key
transfer = cuenca.Transfer.one(idempotency_key='unique string')

# returns a generator of all succeeded transfers to the specific account
transfers = cuenca.Transfer.all(
    account_number='646180157000000004',
    status=Status.succeeded
)

# the total number of succeeded transfers
count = cuenca.Transfer.count(status=Status.succeeded)
```

## Api Keys

### Create new `ApiKey` and deactivate old
```python
import cuenca

# Create new ApiKey
new = cuenca.ApiKey.create()

# Have to use the new key to deactivate the old key
old_id = cuenca.session.auth[0]
cuenca.session.configure(new.id, new.secret)
cuenca.ApiKey.deactivate(old_id, minutes)
```