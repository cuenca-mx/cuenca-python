import datetime as dt

from cuenca.resources.addresses import Address
from cuenca.resources.users import User
from cuenca.resources.users_datas import UserDataType


def test_users_step_by_step():
    user_dict = dict(
        nombres='Pedro',
        primer_apellido='Paramo',
        segundo_apellido='Gozalez',
        gender='male',
        birth_date=dt.datetime(1917, 5, 16),
    )
    # se crea un usuario con lo mínimo requerido
    user = User.create(**user_dict)
    # se van creando uno por uno los recursos que se van a ir asignando
    # al pasarle el id del usuario al recurso, internamente se hace un fetch
    # del usuario, y al usuario se le asigna el URI del recurso

    # dirección
    address_dict = dict(
        user_id=user.id,
        calle='Reforma',
        numero_ext='265',
        codigo_postal='06500',
        estado='CDMX',
        colonia='Cuauhtemoc',
    )
    address = Address.create(**address_dict)
    assert address.user_id == user.id
    user.refresh()
    assert address.id == user.address_uri

    # teléfono
    telefono_dict = dict(
        user_id=user.id,
        type=UserDataType.phone_number,
        data='5555667788',
    )
    telefono = UserDataType.create(**telefono_dict)
    assert telefono.user_id == user.id
    user.refresh()
    assert telefono.id == user.phone_uri

    # email
    email_dict = dict(
        user_id=user.id,
        type=UserDataType.email_address,
        data='1234@cuenca.com',
    )
    email = UserDataType.create(**email_dict)
    assert email.user_id == user.id
    user.refresh()
    assert email.id == user.phone_uri

    # y así con cada uno de los elementos, se van creando y
    # se asignan mutuamente


def test_users_all_at_once():
    # para este test, se manda todo de una sola vez a la creación de usuarios
    user_dict = dict(
        nombres='Pedro',
        primer_apellido='Paramo',
        segundo_apellido='Gozalez',
        gender='male',
        birth_date=dt.datetime(1917, 5, 16),
        address=dict(
            # acá el user_id se va a ligar en el método create de Identify
            calle='Reforma',
            numero_ext='265',
            codigo_postal='06500',
            estado='CDMX',
            colonia='Cuauhtemoc',
        ),
        phone_number=dict(
            type=UserDataType.phone_number,
            data='5555667788',
        ),
        email_address=dict(
            type=UserDataType.email_address,
            data='1234@cuenca.com',
        ),
    )

    user = User.create(**user_dict)

    address = user.address

    assert address.user_id == user.id
    user.refresh()
    assert address.id == user.address_uri
