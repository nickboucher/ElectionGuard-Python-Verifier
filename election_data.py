# ElectionGuard Verifier Classes
# Nicholas Boucher 2020
from typing import Any, List, Optional


class ElectionDataException(Exception):
    """Raised when there is an error deserializing election data."""
    pass


class ElectionData():
    """Base class for election data with helper methods."""

    def assert_values(self, *values: Any) -> None:
        """Asserts that values are not None."""
        for value in values:
            if value is None or (isinstance(value, str) and value == ""):
                raise ElectionDataException(self.__class__.__name__
                                            + " missing required data.")

    def to_int(self, value: str) -> int:
        """Returns value converted to int with error handling."""
        try:
            return int(value)
        except ValueError:
            raise ElectionDataException("Error parsing"
                                        f"{self.__class__.__name__} required"
                                        "parameters.")


class Parameters(ElectionData):
    """All the parameters necessary to form the election."""

    def __init__(self, date: str, location: str, num_trustees: str,
                 threshold: str, prime: str, generator: str) -> None:
        self.assert_values(date, location, num_trustees, threshold, prime,
                           generator)
        self.date = date
        self.location = location
        self.num_trustees = self.to_int(num_trustees)
        self.threshold = self.to_int(threshold)
        self.prime = self.to_int(prime)
        self.generator = self.to_int(generator)


class Proof(ElectionData):
    """A proof of posession of the private key."""

    def __init__(self, commitment: str, challenge: str, response: str) -> None:
        self.assert_values(commitment, challenge, response)
        self.commitment = self.to_int(commitment)
        self.challenge = self.to_int(challenge)
        self.response = self.to_int(response)


class TrusteeCoefficient(ElectionData):
    """Public key with associated proof of knowledge."""

    def __init__(self, public_key: str, proof: Proof) -> None:
        self.assert_values(public_key, proof)
        self.public_key = self.to_int(public_key)
        self.proof = proof


class TrusteePublicKey(ElectionData):
    """Each trustee generates `k` secret coefficients, and generates a public
        key from each one. The first such key is trustee's main public key
        (that is, `Ki = K_i0`); the rest are used during decryption if this
        trustee is absent."""

    def __init__(self, coefficients: List[TrusteeCoefficient]) -> None:
        self.assert_values(coefficients)
        self.coefficients = coefficients


class BallotInfo(ElectionData):
    """Auxiliary information about a ballot other than the selections made by
       the voter."""

    def __init__(self, date: str, device_info: str, time: str,
                 tracker: str) -> None:
        self.assert_values(date, device_info, time, tracker)
        self.date = date
        self.device_info = device_info
        self.time = time
        self.tracker = tracker


class Message(ElectionData):
    """A message that has been encrypted using exponential ElGamal."""

    def __init__(self, public_key: str, ciphertext: str) -> None:
        self.assert_values(public_key, ciphertext)
        self.public_key = self.to_int(public_key)
        self.ciphertext = self.to_int(ciphertext)


class CastSelection(ElectionData):
    """Cast ballot selection and associated proof."""

    def __init__(self, message: Message, proof: Proof) -> None:
        self.assert_values(message, proof)
        self.message = message
        self.proof = proof


class CastContest(ElectionData):
    """A contests consists of a list of encrypted selections, along with a
       proof that exactly `L` of them have been selected."""

    def __init__(self, selections: List[CastSelection], max_selections: str,
                 num_selections_proof: Proof) -> None:
        self.assert_values(selections, max_selections, num_selections_proof)
        self.selections = selections
        self.max_selections = self.to_int(max_selections)
        self.num_selections_proof = num_selections_proof


class CastBallot(ElectionData):
    """An encrypted ballot, consisting of the encrypted selections for each
       contest, their proofs of well-formedness, and information about where
       and when the ballot was encrypted."""

    def __init__(self, ballot_info: BallotInfo,
                 contests: List[CastContest]) -> None:
        self.assert_values(ballot_info, contests)
        self.ballot_into = ballot_info
        self.contests = contests


class Fragment(ElectionData):
    """"A fragment of a missing trustee's share of a decryption, including the
        Lagrange coefficient."""

    def __init__(self, fragment: str, lagrange_coefficient: str, proof: Proof,
                 trustee_index: str) -> None:
        self.assert_values(fragment, lagrange_coefficient, proof,
                           trustee_index)
        self.fragment = self.to_int(fragment)
        self.lagrange_coefficient = self.to_int(lagrange_coefficient)
        self.proof = proof
        self.trustee_index = self.to_int(trustee_index)


class ShareRecovery(ElectionData):
    """The `k` fragments used to reconstruct this decryption share, if this
       trustee was absent."""

    def __init__(self, fragments: List[Fragment]) -> None:
        self.assert_values(fragments)
        self.fragments = fragments


class Share(ElectionData):
    """A single trustee's share of a decryption of some encrypted message
       `(a, b)`. The encrypted message can be an encrypted tally or a selection
       from an encrypted ballot."""

    def __init__(self, recovery: Optional[ShareRecovery],
                 proof: Optional[Proof], share: str):
        self.assert_values(share)
        self.recovery = recovery
        self.proof = proof
        self.share = self.to_int(share)


class DecryptedValue(ElectionData):
    """The decryption of an encrypted value, with proofs that it was decrypted
       properly."""

    def __init__(self, cleartext: str, decrypted_value: str,
                 encrypted_value: Message, shares: List[Share]) -> None:
        self.assert_values(cleartext, decrypted_value, encrypted_value, shares)
        self.cleartext = self.to_int(cleartext)
        self.decrypted_value = self.to_int(decrypted_value)
        self.encrypted_value = encrypted_value
        self.shares = shares


class SelectionTally(ElectionData):
    """Decrypted tallies for a specific selection."""

    def __init__(self, value: DecryptedValue) -> None:
        self.assert_values(value)
        self.value = value


class ContestTally(ElectionData):
    """Summed tallies for the election."""

    def __init__(self, selections: List[SelectionTally]) -> None:
        self.assert_values(selections)
        self.selections = selections


class SpoiledSelection(ElectionData):
    """Selection within a spoiled ballot."""

    def __init__(self, value: DecryptedValue) -> None:
        self.assert_values(value)
        self.value = value


class SpoiledContest(ElectionData):
    """Contest in a spoiled ballot."""

    def __init__(self, selections: List[SpoiledSelection]) -> None:
        self.assert_values(selections)
        self.selections = selections


class SpoiledBallot(ElectionData):
    """A decryption of an encrypted ballot that was spoiled."""

    def __init__(self, ballot_info: BallotInfo,
                 contests: List[SpoiledContest]) -> None:
        self.assert_values(ballot_info, contests)
        self.ballot_info = ballot_info
        self.contests = contests


class Record(ElectionData):
    """All data from an ElectionGuard election."""

    def __init__(self, parameters: Parameters, base_hash: str,
                 trustee_public_keys: List[TrusteePublicKey],
                 joint_public_key: str, extended_base_hash: str,
                 cast_ballots: List[CastBallot],
                 contest_tallies: List[ContestTally],
                 spoiled_ballots: List[SpoiledBallot]) -> None:
        self.assert_values(parameters, base_hash, trustee_public_keys,
                           joint_public_key, extended_base_hash, cast_ballots,
                           contest_tallies, spoiled_ballots)
        self.parameters = parameters
        self.trustee_public_keys = trustee_public_keys
        self.cast_ballots = cast_ballots
        self.spoiled_ballots = spoiled_ballots
        self.base_hash = self.to_int(base_hash)
        self.joint_public_key = self.to_int(joint_public_key)
        self.extended_base_hash = self.to_int(extended_base_hash)
