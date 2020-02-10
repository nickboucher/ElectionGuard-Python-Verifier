#!/usr/bin/env python3
# ElectionGuard Verifier
# Nicholas Boucher 2020
from argparse import ArgumentParser
from json import load
from os.path import isfile
from sys import exit


def main() -> None:
    # Parse argument from command line
    parser = ArgumentParser(
            description='Verify ElectionGuard Elections Results.')
    parser.add_argument('election_data',
                        help='ElectionGuard results JSON file.')
    args = parser.parse_args()
    if not isfile(args.election_data):
        exit("election_data is invalid file path")

    # Read election results
    with open(args.election_data, 'r') as f:
        election_data = load(f)
    print(election_data)


if __name__ == '__main__':
    main()
