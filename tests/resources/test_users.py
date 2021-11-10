import datetime as dt

from cuenca_validations.types.enums import (
    CardIssuerType,
    GovtIdType,
    UserDataType,
    UserProofType,
)

from cuenca.resources.addresses import Address
from cuenca.resources.govt_id import GovtID
from cuenca.resources.tos_agreements import TOSAgreement
from cuenca.resources.users import User
from cuenca.resources.users_datas import UserData
from cuenca.resources.users_proofs import UserProof


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
    telefono = UserData.create(**telefono_dict)
    assert telefono.user_id == user.id
    user.refresh()
    assert telefono.id == user.phone_uri

    # email
    email_dict = dict(
        user_id=user.id,
        type=UserDataType.email_address,
        data='1234@cuenca.com',
    )
    email = UserData.create(**email_dict)
    assert email.user_id == user.id
    user.refresh()
    assert email.id == user.email_uri

    # profession
    profession_dict = dict(
        user_id=user.id,
        type=UserDataType.profession,
        data='engineer',
    )
    profession = UserData.create(**profession_dict)
    assert profession.user_id == user.id
    user.refresh()
    assert profession.id == user.profession_uri

    # proof_of_address
    proof_of_address_dict = dict(
        user_id=user.id,
        type=UserProofType.proof_of_address,
        feedme_uri='prueba.com',
    )
    proof_of_address = UserProof.create(**proof_of_address_dict)
    assert proof_of_address.user_id == user.id
    user.refresh()
    assert proof_of_address.id == user.proof_of_address_uri

    # proof_of_life
    proof_of_life_dict = dict(
        user_id=user.id,
        type=UserProofType.proof_of_life,
        feedme_uri='prueba.com',
    )
    proof_of_life = UserProof.create(**proof_of_life_dict)
    assert proof_of_life.user_id == user.id
    user.refresh()
    assert proof_of_life.id == user.proof_of_life_uri

    # curp
    curp_dict = dict(
        user_id=user.id,
        type=UserProofType.curp,
        feedme_uri='prueba.com',
        value='curpgenerico',
    )
    curp = UserProof.create(**curp_dict)
    assert curp.user_id == user.id
    user.refresh()
    assert curp.id == user.curp_uri

    # blacklist_check (quien es quien)
    blacklist_check_dict = dict(
        user_id=user.id,
        type=UserProofType.blacklist_check,
        feedme_uri='prueba.com',
        value='Pedro Páramo Gonzalez',
    )
    blacklist_check = UserProof.create(**blacklist_check_dict)
    assert blacklist_check.user_id == user.id
    user.refresh()
    assert blacklist_check.id == user.blacklist_check_uri

    # govt_id
    govt_id_dict = dict(
        user_id=user.id,
        type=GovtIdType.ine_front,
        is_mx=True,
        feedme_uri='test.com',
        number='123456',
    )
    govt_id = GovtID.create(**govt_id_dict)
    assert govt_id.user_id == user.id
    user.refresh()
    assert govt_id.id == user.govt_id_uri

    # tos
    tos_agreement_dict = dict(
        user_id=user.id,
        type=CardIssuerType.tarjetas_cuenca,
        version=1,
        ip='1.0.0.0.127',
        location='123454.245',
    )
    tos_agreement = TOSAgreement.create(**tos_agreement_dict)
    assert tos_agreement.user_id == user.id
    user.refresh()
    assert tos_agreement.id == user.tos_agreement_uri


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
        profession=dict(
            type=UserDataType.profession,
            data='engineer',
        ),
        proof_of_address=dict(
            type=UserProofType.proof_of_address,
            feedme_uri='prueba.com',
        ),
        proof_of_life=dict(
            type=UserProofType.proof_of_life,
            feedme_uri='prueba.com',
        ),
        curp=dict(
            type=UserProofType.curp,
            feedme_uri='prueba.com',
            value='curpgenerico',
        ),
        blacklist_check_dict=dict(
            type=UserProofType.blacklist_check,
            feedme_uri='prueba.com',
            value='Pedro Páramo Gonzalez',
        ),
        govt_id_dict=dict(
            type=GovtIdType.ine_front,
            is_mx=True,
            feedme_uri='test.com',
            number='123456',
        ),
        tos_agreement_dict=dict(
            type=CardIssuerType.tarjetas_cuenca,
            version=1,
            ip='1.0.0.0.127',
            location='123454.245',
        ),
    )

    user = User.create(**user_dict)

    address = user.address

    assert address.user_id == user.id
    user.refresh()
    assert address.id == user.address_uri
