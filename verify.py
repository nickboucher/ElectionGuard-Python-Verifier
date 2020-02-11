#!/usr/bin/env python3
# ElectionGuard Verifier
# Nicholas Boucher 2020
from argparse import ArgumentParser
from json import load
from os.path import isfile
from sys import exit
from typing import Dict
from logging import Logger, getLogger, CRITICAL, WARNING
from schema import schema
from jsonschema import validate, ValidationError


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

    # Read election results
    with open(args.election_data, 'r') as f:
        election_data = load(f)

    # Verify the election results
    verify_election(election_data, log)


def verify_json(election_data: Dict, log: Logger = None) -> bool:
    """Returns true when the deserialized json `election_data` is valid.
       Optionally, info can be logged by passing a Logger."""
    # Setup logging infrastructure
    if log is None:
        log = getLogger("verify_json")
        log.setLevel(CRITICAL)

    # Validate election_data against JSON schema
    try:
        validate(instance=election_data, schema=schema)
    except ValidationError as err:
        log.warning(f"JSON did not match required schema: {err.message}")
        return False
    return True


def verify_election(election_data: Dict, log: Logger = None) -> bool:
    """Returns true when the election results `election_data` are valid.
       Optionally, info can be logged by passing a Logger."""
    # Setup logging infrastructure
    if log is None:
        log = getLogger("verify_json")
        log.setLevel(CRITICAL)

    # Ensure function paraeters are valid
    if not verify_json(election_data, log):
        return False

    def fail(message: str) -> bool:
        """Outputs a failure log message with the passed text and
           returns false."""
        log.warning(message)
        return False

    # Test: The number of trustees who can together decrypt the election is
    # greater than zero
    try:
        num_trustees = int(election_data['parameters']['num_trustees'])
    except ValueError:
        return fail(f"'num_trustees' value "
                    "'{election_data['parameters']['num_trustees']}' is not a "
                    "valid number.")
    if num_trustees <= 0:
        return fail(f"Invalid number of trustees: {num_trustees}")

    # Test: The threshold of trustees necessary to decrypt the election is
    # greater than zero
    try:
        trustees_threshold = int(election_data['parameters']['threshold'])
    except ValueError:
        return fail("'threshold' value "
                    f"'{election_data['parameters']['threshold']}' is not a "
                    "valid number.")
    if trustees_threshold <= 0:
        return fail("Invalid trustee decryption threshold: "
                    f"{trustees_threshold}")

    # Test: The threshold of trustees necessary to decrypt the election is not
    # greater than the total number of trustees
    if trustees_threshold > num_trustees:
        return fail(f"Trustee decryption threshold ({trustees_threshold}) is "
                    "greater than the total number of trustees "
                    f"({num_trustees}).")


if __name__ == '__main__':
    main()
