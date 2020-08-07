import argparse
import csv
import logging
from dataclasses import fields

import cuenca
from cuenca.resources.transfers import Transfer, TransferRequest

logging.basicConfig(level=logging.INFO, format='cuenca-python: %(message)s')


def convert_amount(data):
    data['amount'] = int(data['amount'])
    return data


def main():
    parser = argparse.ArgumentParser(
        description='Process batch transfers file'
    )
    parser.add_argument(
        'input', type=str, help='Path to CSV batch transfers file',
    )
    parser.add_argument('output', type=str, help='Path to CSV output file')
    parser.add_argument('apikey', type=str, help='api key')
    parser.add_argument('secret', type=str, help='secret key')

    args = parser.parse_args()
    with open(args.input) as f:
        print('reading file')
        reader = csv.DictReader(f)
        # offline validation of transfers
        print('validate data')
        transfer_requests = [
            TransferRequest(**convert_amount(line)) for line in reader
        ]
    print(f'apikey: {args.apikey}')
    print(f'secret: {args.secret}')
    print(transfer_requests)
    cuenca.configure(api_key=args.apikey, api_secret=args.secret)
    print('CREATE MANY' * 10)
    transfers = Transfer.create_many(transfer_requests)
    with open(args.output, 'w') as f:
        fieldnames = [field.name for field in fields(Transfer)]
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        print('WRITE RESULTS')
        for tr in transfers['submitted']:
            tr.refresh()
            writer.writerow(tr.to_dict())
    for error in transfers['errors']:
        logging.info(f'REQUEST: {error["request"]}, ERROR: {error["error"]}')


if __name__ == '__main__':
    main()
