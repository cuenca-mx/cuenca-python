import datetime as dt
from typing import List

from cuenca_validations.types import (
    Currency,
    EntryType,
    SavingCategory,
    TransactionStatus,
    WalletType,
)

from cuenca import BalanceEntry
from cuenca.resources.savings import Saving
from cuenca.resources.wallet_transactions import WalletDeposit, WalletTransfer


def test_flows_saving():
    # STEP 1: CREATE SAVING
    saving = Saving.create(
        name='Ahorros',
        category=SavingCategory.travel,
        goal_amount=1000000,
        goal_date=dt.datetime.now() + dt.timedelta(days=365),
        currency=Currency.mxn,
    )
    assert saving.type == WalletType.saving
    assert saving.balance == 0
    assert saving.id is not None

    default_la = 'LA_123'
    account_uri = f'accounts/{default_la}'
    wallet_uri = f'savings/{saving.id}'

    # STEP 2 : DEPOSIT MONEY IN SAVING
    wallet_transfer = WalletTransfer.create(
        source_id=default_la,
        destination_id=saving.id,
        amount=10000,
    )
    assert wallet_transfer.funding_instrument_uri == account_uri
    assert wallet_transfer.status == TransactionStatus.submitted
    assert wallet_transfer.amount == 10000
    deposit_id = wallet_transfer.id  # LT_123

    # After processing transaction in core
    wallet_transfer.refresh()
    assert wallet_transfer.status == TransactionStatus.succeeded

    # Check deposit exists in wallet
    saving.refresh()
    assert saving.balance == 10000
    wallet_deposit: WalletDeposit = WalletDeposit.retrieve(deposit_id)
    assert wallet_deposit.funding_instrument_uri == wallet_uri
    assert wallet_deposit.status == TransactionStatus.succeeded

    # STEP 3: WITHDRAW MONEY FROM SAVING
    wallet_transfer = WalletTransfer.create(
        source_id=saving.id,
        destination_id=default_la,
        amount=2000,
    )
    assert wallet_transfer.status == TransactionStatus.submitted
    assert wallet_transfer.amount == 2000
    withdraw_id = wallet_transfer.id  # LT_123

    # After processing transaction in core
    wallet_transfer.refresh()
    assert wallet_transfer.status == TransactionStatus.succeeded
    saving.refresh()
    assert saving.balance == 8000
    wallet_deposit: WalletDeposit = WalletDeposit.retrieve(withdraw_id)
    assert wallet_deposit.funding_instrument_uri == account_uri
    assert wallet_deposit.status == TransactionStatus.succeeded

    # BALANCES IN WALLET
    entries: List[BalanceEntry] = BalanceEntry.all(
        funding_instrument_uri=wallet_uri
    )
    assert len(entries) == 2
    credit = [be for be in entries if be.type == EntryType.credit][0]
    assert credit.amount == 10000
    assert credit.related_transaction == f'wallet_deposits/{deposit_id}'
    debit = [be for be in entries if be.type == EntryType.debit][0]
    assert debit.related_transaction == f'wallet_transfers/{withdraw_id}'
    assert debit.amount == 2000

    # BALANCES IN DEFAULT LA
    entries = BalanceEntry.all(funding_instrument_uri=account_uri)
    assert len(entries) == 2
    debit = [be for be in entries if be.type == EntryType.debit][0]
    assert debit.related_transaction == f'wallet_transfers/{deposit_id}'
    assert debit.amount == 10000
    credit = [be for be in entries if be.type == EntryType.credit][0]
    assert credit.related_transaction == f'wallet_deposits/{withdraw_id}'
    assert credit.amount == 2000
