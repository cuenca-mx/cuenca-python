from typing import ClassVar, Optional, cast

from clabe import Clabe
from cuenca_validations.types import (
    AccountQuery,
    CurpField,
    LimitedWalletRequest,
    Rfc,
)

from ..http import Session, session as global_session
from .base import Wallet


class LimitedWallet(Wallet):
    _resource: ClassVar = 'limited_wallets'
    _query_params: ClassVar = AccountQuery
    account_number: Clabe
    allowed_rfc: Optional[Rfc]
    allowed_curp: CurpField

    @classmethod
    def create(
        cls,
        allowed_curp: Optional[CurpField] = None,
        allowed_rfc: Optional[Rfc] = None,
    ) -> 'LimitedWallet':
        """
        Limited wallet is a special sub-account to receive money only from
        specific person, SPEI Deposits will be accepted only if the sender
        account curp/rfc match with registered data

        Args:
            allowed_curp: Valid CURP
            allowed_rfc: Valid RFC
        """
        request = LimitedWalletRequest(
            allowed_curp=allowed_curp,
            allowed_rfc=allowed_rfc,
        )
        return cast('LimitedWallet', cls._create(**request.dict()))

    @classmethod
    def block(
        cls, limited_wallet_id: str, *, session: Session = global_session
    ) -> 'LimitedWallet':
        """
        Blocks a Limited Wallet avoiding it to send and receive transactions

        Args:
            limited_wallet_id: Limited Wallet ID
        """
        url = f'{cls._resource}/{limited_wallet_id}'
        resp = session.delete(url)
        return cast('LimitedWallet', cls._from_dict(resp))
