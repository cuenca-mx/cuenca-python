from typing import Optional

from cuenca_validations.types.identities import CurpField, Rfc
from cuenca_validations.types.requests import BaseRequest


# TODO: move to cuenca_validations
class LimitedWalletRequest(BaseRequest):
    allowed_curp: CurpField
    allowed_rfc: Optional[Rfc]

    
