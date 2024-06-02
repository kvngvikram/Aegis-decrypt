#!/usr/bin/env python3
"""
usage: aegis-decrypt.py [-h] --vault VAULT [--entryname ENTRYNAME] [--output {None,csv,qrcode,json,otp}]
password: test
"""
import argparse
import getpass

from src.AegisDB import AegisDB
from src.Output import Output


def main():
    parser = argparse.ArgumentParser(prog="aegis-decrypt.py",
                                     description="Decrypt an Aegis vault and produce an output as requested", add_help=True)
    parser.add_argument("--vault", dest="vault", required=True, help="The encrypted Aegis vault file")
    # optional args
    parser.add_argument("--entryname", dest="entryname", required=False,
                        help="The name of the entry for which you want to generate the OTP code")
    parser.add_argument("--output", dest="output", required=False, choices=[None, 'csv', 'qrcode', 'json', 'otp'],
                        help="The output format (default is stdout)")
    parser.add_argument("--password", dest="password", required=False,
                        help="The encryption password")
    args = parser.parse_args()

    if args.password is None:
        password = getpass.getpass().encode("utf-8")
    else:
        password = args.password.encode("utf-8")

    db = AegisDB(args.vault, password)

    if args.entryname is None:
        entries = db.getAll()
    else:
        entries = db.getByName(args.entryname)

    if entries:
        output = Output(entries, args.entryname)

        match args.output:
            case 'csv':
                output.csv()
            case 'qrcode':
                output.qrcode()
            case 'json':
                output.json()
            case 'otp':
                output.otp()
            case _:
                output.stdout()
    else:
        print("No entries found")


if __name__ == '__main__':
    main()
