#!/usr/bin/env python3
# ElectionGuard Command Line Verifier Utility
# Nicholas Boucher 2020
from argparse import ArgumentParser
from json import load
from os.path import isfile
from sys import exit
from logging import getLogger, WARNING
from deserialize import load_election
from data_types import ElectionDataException
from verify import verify_election


def main() -> None:
    """Main point of entry for command line execution."""
    # Parse argument from command line
    parser = ArgumentParser(
            description='Verify ElectionGuard Elections Results.')
    parser.add_argument('election_data',
                        help='ElectionGuard results JSON file.')
    args = parser.parse_args()
    if not isfile(args.election_data):
        exit("election_data is invalid file path")

    # Setup logging infrastructure
    log = getLogger()
    log.setLevel(WARNING)

    # Load election results
    with open(args.election_data, 'r') as f:
        try:
            election = load_election(load(f), log)
        except ElectionDataException:
            log.warning("Election Invalid.")
            return

    # Verify the election results
    if verify_election(election):
        log.warning("Election Valid.")
    else:
        log.warning("Election Invalid.")


if __name__ == '__main__':
    main()
