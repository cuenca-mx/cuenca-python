import argparse
import csv
import logging
from dataclasses import fields

from cuenca.resources.transfers import Transfer, TransferRequest

logging.basicConfig(level=logging.INFO, format='cuenca-python: %(message)s')


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
        transfer_requests = [TransferRequest(**line) for line in reader]
    transfers = Transfer.create_many(transfer_requests)
    with open(args.output, 'w') as f:
        fieldnames = [field.name for field in fields(Transfer)]
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for tr in transfers['submitted']:
            writer.writerow(tr.to_dict())
    for error in transfers['errors']:
        logging.info(f'REQUEST: {error["request"]}, ERROR: {error["error"]}')


if __name__ == '__main__':
    main()

