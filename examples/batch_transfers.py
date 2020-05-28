import argparse
import csv
from dataclasses import fields

from cuenca.resources.transfers import Transfer, TransferRequest


def gen_transfer_requests(
    account_number: str, amount: int, descriptor: str, recipient_name: str,
):
    idempotency_key = Transfer._gen_idempotency_key(account_number, amount)
    return TransferRequest(
        account_number=account_number,
        amount=amount,
        descriptor=descriptor,
        recipient_name=recipient_name,
        idempotency_key=idempotency_key,
    )


def main():
    parser = argparse.ArgumentParser(
        description='Process batch transfers file'
    )
    parser.add_argument(
        'input', type=str, help='Path to CSV batch transfers file',
    )
    parser.add_argument('output', type=str, help='Path to CSV output file')
    args = parser.parse_args()
    with open(args.input) as f:
        reader = csv.DictReader(f)
        # offline validation of transfers
        transfer_requests = [gen_transfer_requests(**line) for line in reader]
    with open(args.output) as f:
        fieldnames = [field.name for field in fields(Transfer)]
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for req in transfer_requests:
            tr = Transfer.create_using_request(req)
            writer.writerow(tr.to_dict())


if __name__ == '__main__':
    main()
