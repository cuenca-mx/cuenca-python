from enum import Enum


class Estado(str, Enum):
    pendiente = 'pendiente'
    exitosa = 'exitosa'
    fallida = 'fallida'
