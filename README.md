# Cuenca – Python client library

[![test](https://github.com/cuenca-mx/cuenca-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/cuenca-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/cuenca-python/branch/main/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/cuenca-python)
[![PyPI](https://img.shields.io/pypi/v/cuenca.svg)](https://pypi.org/project/cuenca/)

# Installation

`pip install cuenca`

# Authentication

The preferred way to configure the credentials for the client is to set the
`CUENCA_API_KEY` and `CUENCA_API_SECRET` environment variables. The client
library will automatically configure based on the values of those variables.

To configure manually:
```python
import cuenca

cuenca.configure(api_key='PKxxxx', api_secret='yyyyyy')
```

### Jwt

JWT tokens can also be used if your credentials have enough permissions. To
do so, you may include the parameter `use_jwt` as part of your `configure`

```python
import cuenca

cuenca.configure(use_jwt=True)
```

A new token will be created at this moment and automatically renewed before
sending any request if there is less than 5 minutes to be expired according
to its payload data.


## Transfers

### Create transfer

```python
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
local_transfer_id = '078efdc20bab456285437309c4b75673'
transfer = cuenca.Transfer.one(idempotency_key=local_transfer_id)

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
cuenca.ApiKey.deactivate(old_id, 60)  # revoke prior API key in an hour
```
