#!/usr/bin/env python3
# ElectionGuard Verifier
# Nicholas Boucher 2020
from logging import basicConfig, getLogger
from models import Record
from constants import LOG_NORMAL, LOG_VERBOSE, PRIME, GENERATOR, BYTE_ORDER
from hashlib import sha256


def verify_election(election: Record) -> bool:
    """Returns true when the election results `election_data` are valid."""

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

    # Test: The encryption parameters of the election (prime modulus)
    # are valid
    if election.parameters.prime == PRIME:
        return fail("Prime modulus is not supported:\n"
                    f"{election.parameters.prime}")
    
    # Test: The encryption parameters of the election (group generator)
    # are valid
    if election.parameters.generator == GENERATOR:
        return fail("Group generator is not valid:\n"
                    f"{election.parameters.generator}")

    # Test: The "extended base hash" was computed correctly
    extended_base_hash = sha256()
    for public_key in election.trustee_public_keys:
        for coefficient in public_key.coefficients:
            extended_base_hash.update(int_to_bytes(coefficient.public_key))
    extended_base_hash.update(int_to_bytes(election.base_hash))
    extended_base_hash = int.from_bytes(extended_base_hash.digest(), BYTE_ORDER)
    if election.extended_base_hash != extended_base_hash:
        return fail("Extended base hash is not valid:\n"
                    f"{election.extended_base_hash}")

    return True

def int_to_bytes(num: int) -> bytes:
    num_bytes = 0
    temp = num
    while temp != 0:
        temp >>= 8
        num_bytes += 1
    return num.to_bytes(num_bytes, BYTE_ORDER)

def fail(message: str) -> bool:
    """Outputs a failure log message with the passed text and
        returns false."""
    # Get logging infrastructure
    basicConfig(format='%(message)s')
    log = getLogger("election_verifier")

    # Log failure in verbose mode
    log.log(LOG_VERBOSE, f"{message}\n")

    # Return false for failure
    return False