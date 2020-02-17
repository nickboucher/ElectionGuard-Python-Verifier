#!/usr/bin/env python3
# ElectionGuard Verifier
# Nicholas Boucher 2020
from typing import Dict
from logging import Logger, getLogger, CRITICAL


def verify_election(election_data: Dict, log: Logger = None) -> bool:
    """Returns true when the election results `election_data` are valid.
       Optionally, info can be logged by passing a Logger."""
    # Setup logging infrastructure
    if log is None:
        log = getLogger("verify_election")
        log.setLevel(CRITICAL)

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
