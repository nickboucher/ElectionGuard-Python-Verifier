#!/usr/bin/env python3
# ElectionGuard Verifier
# Nicholas Boucher 2020
from logging import Logger, getLogger, CRITICAL
from models import Record


def verify_election(election: Record, log: Logger = None) -> bool:
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
    if election.parameters.num_trustees <= 0:
        return fail("Invalid number of trustees: "
                    f"{election.parameters.num_trustees}")

    # Test: The threshold of trustees necessary to decrypt the election is
    # greater than zero
    if election.parameters.threshold <= 0:
        return fail("Invalid trustee decryption threshold: "
                    f"{election.parameters.threshold}")

    # Test: The threshold of trustees necessary to decrypt the election is not
    # greater than the total number of trustees
    if election.parameters.threshold > election.parameters.num_trustees:
        return fail("Trustee decryption threshold ("
                    f"{election.parameters.threshold}) is greater than the "
                    "total number of trustees "
                    f"({election.parameters.num_trustees}).")

    return True