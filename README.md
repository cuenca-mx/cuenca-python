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
```
