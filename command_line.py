#!/usr/bin/env python3
# ElectionGuard Command Line Verifier Utility
# Nicholas Boucher 2020
from argparse import ArgumentParser, Namespace
from os.path import isfile
from logging import basicConfig, getLogger
from verify import verify_election
from models import election_record_from_dict
from json import loads
from constants import LOG_VERBOSE, LOG_NORMAL


def main() -> None:
    """Main point of entry for command line execution."""
    # Parse argument from command line
    args = parse_args()

    # Setup logging infrastructure
    basicConfig(format='%(message)s')
    log = getLogger("election_verifier")
    if args.verbose:
        log.setLevel(LOG_VERBOSE)
    else:
        log.setLevel(LOG_NORMAL)

    # Deserialize election data JSON
    with open(args.election_data, 'r') as f:
        election = election_record_from_dict(loads(f.read()))

    # Verify the election results
    if verify_election(election):
        log.log(LOG_NORMAL, "Election Valid.")
    else:
        log.log(LOG_NORMAL, "Election Invalid.")


def parse_args() -> Namespace:
    """Parses, verifies, and returns command line line arguments."""
    # Configure arguments
    parser = ArgumentParser(
            description='Verify ElectionGuard Elections Results.')
    parser.add_argument('election_data',
                        help='ElectionGuard results JSON file.')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="Verbose output.")

    # Parse arguments
    args = parser.parse_args()

    # Verify arguments
    if not isfile(args.election_data):
        exit("election_data is invalid file path")
    
    # Return results
    return args


if __name__ == '__main__':
    main()
