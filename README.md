# Cuenca – Python client library

## Create transfer

```python
from cuenca import Client

client = Client()
transferencia = client.transferencias.create(
    clabe='646180157042875763',
    monto=12345,  # Mx$123.45
    concepto='sending money',
    idempotency_key='unique string',
)

# To get updated status (estado)
transferencia.refresh()
```


## Retrieve by id

```python
from cuenca import Client

client = Client()
transferencia = client.transferencias.retrieve('tr_123')
```

## Retrieve by `idempotency_key`

```python
from cuenca import Client

client = Client()
transferencia = client.transferencias.list(idempotency_key='unique string')[0]
```