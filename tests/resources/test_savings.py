import datetime as dt
from typing import List

from cuenca_validations.types import (
    Currency,
    EntryType,
    SavingCategory,
    TransactionStatus,
    WalletTransactionType,
    WalletType,
)

from cuenca import BalanceEntry
from cuenca.resources.savings import Saving
from cuenca.resources.wallet_transactions import WalletTransaction


def test_flow_savings_mxn():
    # Create saving
    saving = Saving.create(
        name='Ahorros',
        category=SavingCategory.travel,
        goal_amount=1000000,
        goal_date=dt.datetime.now() + dt.timedelta(days=365),
        currency=Currency.mxn,
    )
    assert saving.type == WalletType.saving
    assert saving.balance == 0

    # Deposit money to saving
    wallet_deposit = WalletTransaction.create(
        wallet_id=saving.id,
        transaction_type=WalletTransactionType.deposit,
        amount=10000,
    )
    assert wallet_deposit.status == TransactionStatus.submitted
    assert wallet_deposit.amount_currency == 10000
    # After processing deposit in core
    wallet_deposit.refresh()
    assert wallet_deposit.status == TransactionStatus.succeeded
    saving.refresh()
    assert saving.balance == wallet_deposit.amount

    # Withdraw money from saving
    wallet_withdrawal = WalletTransaction.create(
        wallet_id=saving.id,
        transaction_type=WalletTransactionType.withdrawal,
        amount=5000,
    )
    assert wallet_withdrawal.status == TransactionStatus.submitted
    assert wallet_withdrawal.amount_currency == 5000

    # After processing deposit in core
    wallet_withdrawal.refresh()
    assert wallet_withdrawal.status == TransactionStatus.succeeded
    saving.refresh()
    assert saving.balance == wallet_deposit.amount - wallet_withdrawal.amount

    # Movements in balance LA
    entries: List[BalanceEntry] = BalanceEntry.all(
        funding_instrument_uri=f'/savings/{saving.id}'
    )
    assert len(entries) == 2
    debit = [be for be in entries if be.type == EntryType.debit][0]
    assert (
        debit.related_transaction_uri
        == f'wallet_transactions/{wallet_deposit.id}'
    )
    credit = [be for be in entries if be.type == EntryType.credit][0]
    assert (
        credit.related_transaction_uri
        == f'wallet_transactions/{wallet_withdrawal.id}'
    )
