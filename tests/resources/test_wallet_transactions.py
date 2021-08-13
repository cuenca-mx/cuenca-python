import datetime as dt
from typing import List

from cuenca_validations.types import (
    EntryType,
    SavingCategory,
    TransactionStatus,
    WalletTransactionType,
)

from cuenca import BalanceEntry, Saving, WalletTransaction


def test_flow_savings_mxn():
    # STEP 1: CREATE SAVING
    saving = Saving.create(
        name='Ahorros',
        category=SavingCategory.travel,
        goal_amount=1000000,
        goal_date=dt.datetime.now() + dt.timedelta(days=365),
    )
    assert saving.balance == 0
    wallet_uri = f'/savings/{saving.id}'

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
    deposit_uri = f'wallet_transactions/{deposit.id}'

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
    withdrawal_uri = f'wallet_transactions/{withdrawal.id}'

    # STEP 4 : QUERY TRANSACTIONS OF WAlLET
    transactions_db = WalletTransaction.all(wallet_uri=wallet_uri)
    transactions = [deposit, withdrawal]
    assert all(wt in transactions for wt in transactions_db)

    # CHECK BALANCES ENTRIES IN DEFAULT
    entries: List[BalanceEntry] = BalanceEntry.all(
        funding_instrument_uri=wallet_uri
    )
    assert len(entries) == 2
    # debit associated to Deposit
    debit = [be for be in entries if be.type == EntryType.debit][0]
    assert debit.related_transaction_uri == deposit_uri
    assert debit.amount == deposit.amount
    # credit associated to Withdrawal
    credit = [be for be in entries if be.type == EntryType.credit][0]
    assert credit.amount == withdrawal.amount
    assert credit.related_transaction_uri == withdrawal_uri

    # CHECK BALANCES ENTRIES IN WALLET
    entries: List[BalanceEntry] = BalanceEntry.all(wallet_id=saving.id)
    assert len(entries) == 2
    # credit associated to Deposit
    credit = [be for be in entries if be.type == EntryType.credit][0]
    assert credit.related_transaction_uri == deposit_uri
    assert credit.amount == deposit.amount
    # debit associated to Withdrawal
    debit = [be for be in entries if be.type == EntryType.debit][0]
    assert debit.amount == withdrawal.amount
    assert debit.related_transaction_uri == withdrawal_uri
