import datetime as dt
from typing import List

from cuenca_validations.types import (
    EntryType,
    SavingCategory,
    TransactionStatus,
    WalletTransactionType,
)

from cuenca import BalanceEntry
from cuenca.resources.savings import Saving
from cuenca.resources.wallet_transactions import WalletTransaction


def test_flow_savings_mxn():
    # STEP 1: CREATE SAVING

    saving = Saving.create(
        name='Ahorros',
        category=SavingCategory.travel,
        goal_amount=1000000,
        goal_date=dt.datetime.now() + dt.timedelta(days=365),
    )
    assert saving.balance == 0

    # STEP 2 : DEPOSIT MONEY IN SAVING
    deposit = WalletTransaction.create(
        wallet_id=saving.id,
        transaction_type=WalletTransactionType.deposit,
        amount=10000,
    )
    assert deposit.status == TransactionStatus.submitted
    # After processing deposit in core
    deposit.refresh()
    assert deposit.status == TransactionStatus.succeeded
    saving.refresh()
    assert saving.balance == deposit.amount

    # STEP 3: WITHDRAW MONEY FROM SAVING
    withdrawal = WalletTransaction.create(
        wallet_id=saving.id,
        transaction_type=WalletTransactionType.withdrawal,
        amount=2000,
    )
    assert withdrawal.status == TransactionStatus.submitted
    # After processing deposit in core
    withdrawal.refresh()
    assert withdrawal.status == TransactionStatus.succeeded
    saving.refresh()
    assert saving.balance == deposit.amount - withdrawal.amount

    # CHECK BALANCES ENTRIES
    entries: List[BalanceEntry] = BalanceEntry.all(
        funding_instrument_uri=f'/savings/{saving.id}'
    )
    assert len(entries) == 2
    resource = 'wallet_transactions'
    debit = [be for be in entries if be.type == EntryType.debit][0]
    assert debit.related_transaction_uri == f'{resource}/{deposit.id}'
    assert debit.amount == deposit.amount
    credit = [be for be in entries if be.type == EntryType.credit][0]
    assert credit.amount == withdrawal.amount
    assert credit.related_transaction_uri == f'{resource}/{withdrawal.id}'
