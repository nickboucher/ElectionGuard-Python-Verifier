# ElectionGuard JSON Deserialization
# Nicholas Boucher 2020
from jsonschema import validate, ValidationError
from schema import schema
from data_types import Record, ElectionDataException, Parameters, TrusteeCoefficient, SchnorrProof, TrusteePublicKey, BallotInfo, CastSelection, Message, CastBallot, ChaumPedersenProof, ChaumPedersenDisjointProof
from json import loads
from typing import List


def load_election(election_json: str) -> Record:
    """Returns deserialized json string `election_data` as election `Record`.
       Raises ElectionDataException on error."""

    # Validate election_data against JSON schema
    try:
        validate(instance=election_json, schema=schema)
    except ValidationError as err:
        raise ElectionDataException("JSON did not match required schema:"
                                    + err.message)

    # Load JSON string into dict
    election = loads(election_json)

    # Instantiate election objects with data
    parameters = Parameters(election['date'], election['location'],
                            election['num_trustees'], election['threshold'],
                            election['prime'], election['generator'])

    trustee_public_keys: List[TrusteePublicKey] = []
    for keyset in election['trustee_public_keys']:
        coefficients: List[TrusteeCoefficient] = []
        for key in keyset:
            proof = SchnorrProof(key['proof']['commitment'],
                                 key['proof']['challenge'],
                                 key['proof']['response'])
            coefficients.append(TrusteeCoefficient(key['public_key'], proof))
        trustee_public_keys.append(TrusteePublicKey(coefficients))

    cast_ballots: List[CastBallot] = []
    for ballot in election['cast_ballots']:
        ballot_info = BallotInfo(ballot['ballot_info']['date'],
                                 ballot['ballot_info']['device_info'],
                                 ballot['ballot_info']['time'],
                                 ballot['ballot_info']['tracker'])
        for contest in ballot['contests']:
            selections: List[CastSelection] = []
            for selection in contest['selections']:
                message = Message(selection['message']['public_key'],
                                  selection['message']['ciphertext'])
                zero_proof_message = Message(
                        selection['zero_proof']['commitment']['public_key'],
                        selection['zero_proof']['commitment']['ciphertext'])
                zero_proof = ChaumPedersenProof(zero_proof_message,
                                                key['zero_proof']['challenge'],
                                                key['zero_proof']['response'])
                one_proof_message = Message(
                        selection['one_proof']['commitment']['public_key'],
                        selection['one_proof']['commitment']['ciphertext'])
                one_proof = ChaumPedersenProof(one_proof_message,
                                               key['one_proof']['challenge'],
                                               key['one_proof']['response'])
                disjoint_proof = ChaumPedersenDisjointProof(zero_proof,
                                                            one_proof)
                selections.append(CastSelection(message, disjoint_proof))
