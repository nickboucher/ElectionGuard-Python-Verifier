# ElectionGuard Verifier
# Nicholas Boucher 2020
from models import ElectionRecord
from constants import PRIME, GENERATOR, BYTE_ORDER
from utils import fail, int_to_bytes
from hashlib import sha256


def verify_election(election: ElectionRecord) -> bool:
    """Returns true when the election results `election` are valid."""

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
