# ElectionGuard Verifier Models
# Nicholas Boucher 2020
from serde import Model, fields
from serde.exceptions import ValidationError


class BigUint(fields.Int):
    """Python `int`s which serialize to `str`s."""

    def serialize(self, value):
        return str(value)

    def deserialize(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValidationError("BigUint requires a serialized string.",
                                   value=value)


class Parameters(Model):
    """All the parameters necessary to form the election."""
    date: fields.Str()
    location: fields.Str()
    num_trustees: BigUint()
    threshold: BigUint()
    prime: BigUint()
    generator: BigUint()


class Message(Model):
    """A message that has been encrypted using exponential ElGamal."""
    public_key: BigUint()
    ciphertext: BigUint()


class SchnorrProof(Model):
    """A Schnorr Proof of posession of a private key."""
    commitment: BigUint()
    challenge: BigUint()
    response: BigUint()


class ChaumPedersenProof(Model):
    """A Chaum-Pedersen Proof of value constraints."""
    commitment: fields.Nested(Message)
    challenge: BigUint()
    response: BigUint()


class ChaumPedersenDisjointProof(Model):
    """A pair of Chaum-Pedersen Proofs for constraned sums."""
    left: fields.Nested(ChaumPedersenProof)
    right: fields.Nested(ChaumPedersenProof)


class TrusteeCoefficient(Model):
    """Public key with associated proof of knowledge."""
    public_key: BigUint()
    proof: fields.Nested(SchnorrProof)


class TrusteePublicKey(Model):
    """Each trustee generates `k` secret coefficients, and generates a public
       key from each one. The first such key is trustee's main public key
       (that is, `Ki = K_i0`); the rest are used during decryption if this
       trustee is absent."""
    coefficients: fields.List(TrusteeCoefficient)


class BallotInfo(Model):
    """Auxiliary information about a ballot other than the selections made by
       the voter."""
    date: fields.Str()
    device_info: fields.Str()
    time: fields.Str()
    tracker: fields.Str()


class CastSelection(Model):
    """Cast ballot selection and associated proof."""
    message: fields.Nested(Message)
    zero_proof: fields.Nested(ChaumPedersenProof)
    one_proof: fields.Nested(ChaumPedersenProof)


class CastContest(Model):
    """A contests consists of a list of encrypted selections, along with a
       proof that exactly `L` of them have been selected."""
    selections: fields.List(CastSelection)
    max_selections: BigUint()
    num_selections_proof: fields.Nested(ChaumPedersenProof)


class CastBallot(Model):
    """An encrypted ballot, consisting of the encrypted selections for each
       contest, their proofs of well-formedness, and information about where
       and when the ballot was encrypted."""
    ballot_info: fields.Nested(BallotInfo)
    contests: fields.List(CastContest)


class Fragment(Model):
    """"A fragment of a missing trustee's share of a decryption, including the
        Lagrange coefficient."""
    fragment: BigUint()
    lagrange_coefficient: BigUint()
    proof: fields.Nested(ChaumPedersenProof)
    trustee_index: BigUint()


class ShareRecovery(Model):
    """The `k` fragments used to reconstruct this decryption share, if this
       trustee was absent."""
    fragments: fields.List(Fragment)


class Share(Model):
    """A single trustee's share of a decryption of some encrypted message
       `(a, b)`. The encrypted message can be an encrypted tally or a selection
       from an encrypted ballot."""
    recovery: fields.Optional(fields.Nested(ShareRecovery))
    proof: fields.Optional(fields.Nested(ChaumPedersenProof))
    share: fields.Str()


class DecryptedTally(Model):
    """The decryption of an encrypted tally, with proofs that it was decrypted
       properly."""
    cleartext: BigUint()
    decrypted_tally: BigUint()
    encrypted_tally: fields.Nested(Message)
    shares: fields.List(Share)


class DecryptedMessage(Model):
    """The decryption of an encrypted message, with proofs that it was
       decrypted properly."""
    cleartext: BigUint()
    decrypted_message: BigUint()
    encrypted_message: fields.Nested(Message)
    shares: fields.List(Share)


class SelectionTally(Model):
    """Decrypted tallies for a specific selection."""
    value: fields.Nested(DecryptedTally)


class ContestTally(Model):
    """Tallies for a specific contest."""
    selections: fields.List(SelectionTally)


class SpoiledSelection(Model):
    """Selection within a spoiled ballot."""
    value: fields.Nested(DecryptedMessage)


class SpoiledContest(Model):
    """Contest in a spoiled ballot."""
    selections: fields.List(SpoiledSelection)


class SpoiledBallot(Model):
    """A decryption of an encrypted ballot that was spoiled."""
    ballot_info: fields.Nested(BallotInfo)
    contests: fields.List(fields.List(DecryptedMessage))


class Record(Model):
    """All data from an ElectionGuard election."""
    parameters: fields.Nested(Parameters)
    base_hash: BigUint()
    trustee_public_keys: fields.List(fields.List(TrusteeCoefficient))
    joint_public_key: BigUint()
    extended_base_hash: BigUint()
    cast_ballots: fields.List(CastBallot)
    contest_tallies: fields.List(fields.List(DecryptedTally))
    spoiled_ballots: fields.List(SpoiledBallot)

    @classmethod
    def deserialize(cls, s, **kwargs):
        """Custom deserialization from JSON."""
        model = cls.from_json(s, **kwargs)
        
        # Fix lacking nested list support for trustee public keys
        trustee_public_keys = []
        for trustee_coefficients in model.trustee_public_keys:
            trustee_public_keys.append(TrusteePublicKey(
                    coefficients = trustee_coefficients
            ))
        model.trustee_public_keys = trustee_public_keys

        # Fix lacking nested list support for contest tallies
        contest_tallies = []
        for contest_tally in model.contest_tallies:
            selections = []
            for decrypted_tally in contest_tally:
                selections.append(SelectionTally(
                        value = decrypted_tally
                ))
            contest_tallies.append(ContestTally(
                selections = selections
            ))
        model.contest_tallies = contest_tallies

        # Fix lacking nested list support for spoiled ballots
        for spoiled_ballot in model.spoiled_ballots:
            contests = []
            for spoiled_contest in spoiled_ballot.contests:
                selections = []
                for decrypted_message in spoiled_contest:
                    selections.append(SpoiledSelection(
                        value = decrypted_message
                    ))
                contests.append(SpoiledContest(
                    selections = selections
                ))
            spoiled_ballot.contests = contests

        return model
