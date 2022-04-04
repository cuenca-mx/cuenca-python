from dataclasses import dataclass
from typing import ClassVar, Optional, cast

from clabe import Clabe
from cuenca_validations.types import AccountQuery
from cuenca_validations.types.identities import CurpField, Rfc

from ..cuenca_validations import LimitedWalletRequest
from .base import Wallet


@dataclass
class LimitedWallet(Wallet):
    _resource: ClassVar = 'limited_wallets'
    _query_params: ClassVar = AccountQuery
    account_number: Clabe
    allowed_rfc: Rfc
    allowed_curp = CurpField

    @classmethod
    def create(
        cls,
        allowed_curp: Optional[CurpField] = None,
        allowed_rfc: Optional[Rfc] = None,
    ) -> 'LimitedWallet':
        """
        Limited wallet is a special sub-account that allow receive
        spei deposits only from accounts with specific CURP or RFC

        Args:
            allowed_curp: Valid CURP in accounts to acept deposits.
            allowed_rfc: Valid RFC in acounts to acept deposits
        """
        request = LimitedWalletRequest(
            allowed_curp=allowed_curp,
            allowed_rfc=allowed_rfc,
        )
        return cast('LimitedWallet', cls._create(**request.dict()))
