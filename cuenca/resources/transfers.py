import datetime as dt
from typing import ClassVar, Literal, Optional, cast

from cuenca_validations.types import (
    TransactionStatus,
    TransferNetwork,
    TransferQuery,
    TransferRequest,
    UpdateTransferRequest,
)
from cuenca_validations.typing import DictStrAny
from requests import HTTPError

from ..exc import CuencaException
from ..http import Session, session as global_session
from .accounts import Account
from .base import Creatable, Transaction, Updateable
from .resources import retrieve_uri


class Transfer(Transaction, Creatable, Updateable):
    _resource: ClassVar = 'transfers'
    _query_params: ClassVar = TransferQuery

    updated_at: dt.datetime
    recipient_name: str
    account_number: str
    idempotency_key: str
    network: TransferNetwork
    destination_uri: str
    tracking_key: Optional[str] = None  # clave rastreo if network is SPEI

    @property  # type: ignore
    def destination(self) -> Account:
        return cast(Account, retrieve_uri(self.destination_uri))

    @classmethod
    def create(
        cls,
        account_number: str,
        amount: int,
        descriptor: str,
        recipient_name: str,
        idempotency_key: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> 'Transfer':
        """
        :param account_number: CLABE
        :param amount: needs to be in centavos (not pesos)
        :param descriptor: how it'll appear for the recipient
        :param recipient_name: name of recipient
        :param idempotency_key: must be unique for each transfer to avoid
            duplicates
        :param user_id: Source user to take the funds
        :return: Transfer object

        The recommended idempotency_key scheme:
        1. create a transfer entry in your own database with the status
            created
        2. call this method with the unique id from your database as the
            idempotency_key
        3. update your database with the status created or submitted after
            receiving a response from this method
        """
        if not idempotency_key:
            idempotency_key = cls._gen_idempotency_key(account_number, amount)
        req = TransferRequest(
            account_number=account_number,
            amount=amount,
            descriptor=descriptor,
            recipient_name=recipient_name,
            idempotency_key=idempotency_key,
            user_id=user_id,
        )
        return cls._create(**req.model_dump())

    @classmethod
    def update(
        cls,
        transfer_id: str,
        status: Literal[
            TransactionStatus.succeeded,
            TransactionStatus.failed,
        ],
        *,
        session: Session = global_session,
    ) -> 'Transfer':
        """
        Updates the status of a held transfer.

        :param transfer_id: existing transfer_id
        :param status: TransactionStatus.succeeded to approve, or
            TransactionStatus.failed to reject
        :return: Updated transfer object
        """
        req = UpdateTransferRequest(status=status)
        return cls._update(transfer_id, session=session, **req.model_dump())

    @classmethod
    def create_many(cls, requests: list[TransferRequest]) -> DictStrAny:
        transfers: DictStrAny = dict(submitted=[], errors=[])
        for req in requests:
            try:
                transfer = cls._create(**req.model_dump())
            except (CuencaException, HTTPError) as e:
                transfers['errors'].append(dict(request=req, error=e))
            else:
                transfers['submitted'].append(transfer)
        return transfers

    @staticmethod
    def _gen_idempotency_key(account_number: str, amount: int) -> str:
        """
        We *strongly* recommend using your own internal database id as the
        idempotency_key, but this provides some level of protection against
        submitting duplicate transfers
        """
        return f'{dt.datetime.utcnow().date()}:{account_number}:{amount}'
