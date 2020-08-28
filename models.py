# ElectionGuard Verifier Models
# Autogenerated from Microsoft ElectionGuard SDK Specification Repository
# Nicholas Boucher 2020
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = election_record_from_dict(json.loads(json_string))
from typing import Any, List, Optional, TypeVar, Type, cast, Callable
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class BallotInformation:
    """Auxiliary information about a ballot other than the selections made by the voter."""
    """The date the ballot was encrypted."""
    date: str
    """Information about the device that encrypted the ballot"""
    device_info: str
    """The time the ballot was encrypted."""
    time: str
    """The tracker code generated for this ballot."""
    tracker: str

    def __init__(self, date: str, device_info: str, time: str, tracker: str) -> None:
        self.date = date
        self.device_info = device_info
        self.time = time
        self.tracker = tracker

    @staticmethod
    def from_dict(obj: Any) -> 'BallotInformation':
        assert isinstance(obj, dict)
        date = from_str(obj.get("date"))
        device_info = from_str(obj.get("device_info"))
        time = from_str(obj.get("time"))
        tracker = from_str(obj.get("tracker"))
        return BallotInformation(date, device_info, time, tracker)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_str(self.date)
        result["device_info"] = from_str(self.device_info)
        result["time"] = from_str(self.time)
        result["tracker"] = from_str(self.tracker)
        return result


class ElGamalMessage:
    """An ElGamal message `(α, β)` encoding zero. This is useful because you can only combine
    two ciphertexts if they both encode zero, as in the equation `hᵘ = hᵗ⁺ᶜʳ = hᵗ (hʳ)ᶜ = β
    bᶜ`. This acts as a committment to the one-time private key `t` used in this proof.
    
    A message that has been encrypted using exponential ElGamal.
    
    The encrypted message of the selection (the one or zero).
    """
    """The encoding `b = gᵐ hʳ`, where `m` is the cleartext and `h` is the recipient public key
    being used for encryption.
    """
    ciphertext: int
    """The one-time public key `a = gʳ`, where `r` is the randomly generated one-time public key."""
    public_key: int

    def __init__(self, ciphertext: int, public_key: int) -> None:
        self.ciphertext = ciphertext
        self.public_key = public_key

    @staticmethod
    def from_dict(obj: Any) -> 'ElGamalMessage':
        assert isinstance(obj, dict)
        ciphertext = from_int(obj.get("ciphertext"))
        public_key = from_int(obj.get("public_key"))
        return ElGamalMessage(ciphertext, public_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ciphertext"] = from_int(self.ciphertext)
        result["public_key"] = from_int(self.public_key)
        return result


class ChaumPedersonProof:
    """A proof that the sum of the selections is equal to `L`, by proving that their difference
    is zero.
    
    A non-interactive zero-knowledge Chaum-Pederson proof shows that an ElGamal message
    `(a,b) = (gʳ, gᵐ hʳ)` is actually an encryption of zero (`m = 0`) without revealing the
    nonce `r` used to encode it. This can be used to show that two ElGamal messages encrypt
    the same message, by creating a Chaum-Pederson proof for their quotient `(a₁/a₂, b₁/b₂) =
    (gʳ¹⁻ʳ², gᵐ¹⁻ᵐ² hʳ¹⁻ʳ²)`.
    
    The proof that the fragment encodes the same values as the encrypted message
    
    The proof that the share encodes the same value as the encrypted message.
    """
    """The challenge value `c` that is produced by hashing relevent parameters, including the
    original ElGamal message `(a,b)` and the zero message `(α, β)`.
    """
    challenge: int
    """An ElGamal message `(α, β)` encoding zero. This is useful because you can only combine
    two ciphertexts if they both encode zero, as in the equation `hᵘ = hᵗ⁺ᶜʳ = hᵗ (hʳ)ᶜ = β
    bᶜ`. This acts as a committment to the one-time private key `t` used in this proof.
    """
    committment: ElGamalMessage
    """The response `u = t + c r mod (p-1)` to the challenge `c`, where `r` is the one-time
    private key used to encrypt the original message and `t` is the one-time private key used
    to encrypt the zero message used in this proof.
    """
    response: int

    def __init__(self, challenge: int, committment: ElGamalMessage, response: int) -> None:
        self.challenge = challenge
        self.committment = committment
        self.response = response

    @staticmethod
    def from_dict(obj: Any) -> 'ChaumPedersonProof':
        assert isinstance(obj, dict)
        challenge = from_int(obj.get("challenge"))
        committment = ElGamalMessage.from_dict(obj.get("committment"))
        response = from_int(obj.get("response"))
        return ChaumPedersonProof(challenge, committment, response)

    def to_dict(self) -> dict:
        result: dict = {}
        result["challenge"] = from_int(self.challenge)
        result["committment"] = to_class(ElGamalMessage, self.committment)
        result["response"] = from_int(self.response)
        return result


class EncryptedSelection:
    """A single selection in a contest, which contains the encrypted value of the selection
    (zero or one), as well as a zero-knowledge proof that the encrypted value is either a
    zero or a one. Both a proof that the selection is zero and a proof that the selection is
    one are always included, but depending on the actual value of the selection, one of the
    proofs is "faked" in a way that makes the verification go through. The verifier cannot
    and (need not) determine which proof is "real" and which is "faked", but instead verifies
    that one of them must be real.
    """
    message: ElGamalMessage
    one_proof: ChaumPedersonProof
    zero_proof: ChaumPedersonProof

    def __init__(self, message: ElGamalMessage, one_proof: ChaumPedersonProof, zero_proof: ChaumPedersonProof) -> None:
        self.message = message
        self.one_proof = one_proof
        self.zero_proof = zero_proof

    @staticmethod
    def from_dict(obj: Any) -> 'EncryptedSelection':
        assert isinstance(obj, dict)
        message = ElGamalMessage.from_dict(obj.get("message"))
        one_proof = ChaumPedersonProof.from_dict(obj.get("one_proof"))
        zero_proof = ChaumPedersonProof.from_dict(obj.get("zero_proof"))
        return EncryptedSelection(message, one_proof, zero_proof)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = to_class(ElGamalMessage, self.message)
        result["one_proof"] = to_class(ChaumPedersonProof, self.one_proof)
        result["zero_proof"] = to_class(ChaumPedersonProof, self.zero_proof)
        return result


class EncryptedContest:
    """A contests consists of a list of encrypted selections, along with a proof that exactly
    `L` of them have been selected.
    """
    """The maximum number of selections `L` that can be made in this contest."""
    max_selections: int
    """A proof that the sum of the selections is equal to `L`, by proving that their difference
    is zero.
    """
    num_selections_proof: ChaumPedersonProof
    """The encrypted selections made on the ballot."""
    selections: List[EncryptedSelection]

    def __init__(self, max_selections: int, num_selections_proof: ChaumPedersonProof, selections: List[EncryptedSelection]) -> None:
        self.max_selections = max_selections
        self.num_selections_proof = num_selections_proof
        self.selections = selections

    @staticmethod
    def from_dict(obj: Any) -> 'EncryptedContest':
        assert isinstance(obj, dict)
        max_selections = from_int(obj.get("max_selections"))
        num_selections_proof = ChaumPedersonProof.from_dict(obj.get("num_selections_proof"))
        selections = from_list(EncryptedSelection.from_dict, obj.get("selections"))
        return EncryptedContest(max_selections, num_selections_proof, selections)

    def to_dict(self) -> dict:
        result: dict = {}
        result["max_selections"] = from_int(self.max_selections)
        result["num_selections_proof"] = to_class(ChaumPedersonProof, self.num_selections_proof)
        result["selections"] = from_list(lambda x: to_class(EncryptedSelection, x), self.selections)
        return result


class EncryptedBallot:
    """An encrypted ballot, consisting of the encrypted selections for each contest, their
    proofs of well-formedness, and information about where and when the ballot was encrypted.
    """
    ballot_info: BallotInformation
    contests: List[EncryptedContest]

    def __init__(self, ballot_info: BallotInformation, contests: List[EncryptedContest]) -> None:
        self.ballot_info = ballot_info
        self.contests = contests

    @staticmethod
    def from_dict(obj: Any) -> 'EncryptedBallot':
        assert isinstance(obj, dict)
        ballot_info = BallotInformation.from_dict(obj.get("ballot_info"))
        contests = from_list(EncryptedContest.from_dict, obj.get("contests"))
        return EncryptedBallot(ballot_info, contests)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ballot_info"] = to_class(BallotInformation, self.ballot_info)
        result["contests"] = from_list(lambda x: to_class(EncryptedContest, x), self.contests)
        return result


class DecryptionFragment:
    """A fragment of a missing trustee's share of a decryption, including the LaGrange
    coefficient.
    """
    """The actual fragment `M_{i,j}` which is trustee `j`'s piece of the missing trustee `i`'s
    share of a decryption.
    """
    fragment: int
    """The LaGrange coefficient `w_{i,j}` used to compute the decryption share from the
    fragments.
    """
    lagrange_coefficient: int
    """The proof that the fragment encodes the same values as the encrypted message"""
    proof: ChaumPedersonProof
    """The index of the trustee who produced this fragment."""
    trustee_index: int

    def __init__(self, fragment: int, lagrange_coefficient: int, proof: ChaumPedersonProof, trustee_index: int) -> None:
        self.fragment = fragment
        self.lagrange_coefficient = lagrange_coefficient
        self.proof = proof
        self.trustee_index = trustee_index

    @staticmethod
    def from_dict(obj: Any) -> 'DecryptionFragment':
        assert isinstance(obj, dict)
        fragment = from_int(obj.get("fragment"))
        lagrange_coefficient = from_int(obj.get("lagrange_coefficient"))
        proof = ChaumPedersonProof.from_dict(obj.get("proof"))
        trustee_index = from_int(obj.get("trustee_index"))
        return DecryptionFragment(fragment, lagrange_coefficient, proof, trustee_index)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fragment"] = from_int(self.fragment)
        result["lagrange_coefficient"] = from_int(self.lagrange_coefficient)
        result["proof"] = to_class(ChaumPedersonProof, self.proof)
        result["trustee_index"] = from_int(self.trustee_index)
        return result


class DecryptionShare:
    """A single trustee's share of a decryption of some encrypted message `(a, b)`. The
    encrypted message can be an encrypted tally or an encrypted ballot.
    """
    """The `k` fragments used to reconstruct this decryption share, if this trustee was absent."""
    fragments: Optional[List[DecryptionFragment]]
    """The proof that the share encodes the same value as the encrypted message."""
    proof: ChaumPedersonProof
    """The share of the decrypted message `M_i`."""
    share: int

    def __init__(self, fragments: Optional[List[DecryptionFragment]], proof: ChaumPedersonProof, share: int) -> None:
        self.fragments = fragments
        self.proof = proof
        self.share = share

    @staticmethod
    def from_dict(obj: Any) -> 'DecryptionShare':
        assert isinstance(obj, dict)
        fragments = from_union([lambda x: from_list(DecryptionFragment.from_dict, x), from_none], obj.get("fragments"))
        proof = ChaumPedersonProof.from_dict(obj.get("proof"))
        share = from_int(obj.get("share"))
        return DecryptionShare(fragments, proof, share)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fragments"] = from_union([lambda x: from_list(lambda x: to_class(DecryptionFragment, x), x), from_none], self.fragments)
        result["proof"] = to_class(ChaumPedersonProof, self.proof)
        result["share"] = from_int(self.share)
        return result


class TallyDecryption:
    """A decryption of the encrypted tally of a single option in a contest."""
    """The actual tally encrypted."""
    cleartext: int
    """The decrypted tally `M`."""
    decrypted_tally: int
    encrypted_tally: ElGamalMessage
    """The decryption shares `M_i` used to compute the decrypted tally `M`."""
    shares: List[DecryptionShare]

    def __init__(self, cleartext: int, decrypted_tally: int, encrypted_tally: ElGamalMessage, shares: List[DecryptionShare]) -> None:
        self.cleartext = cleartext
        self.decrypted_tally = decrypted_tally
        self.encrypted_tally = encrypted_tally
        self.shares = shares

    @staticmethod
    def from_dict(obj: Any) -> 'TallyDecryption':
        assert isinstance(obj, dict)
        cleartext = from_int(obj.get("cleartext"))
        decrypted_tally = from_int(obj.get("decrypted_tally"))
        encrypted_tally = ElGamalMessage.from_dict(obj.get("encrypted_tally"))
        shares = from_list(DecryptionShare.from_dict, obj.get("shares"))
        return TallyDecryption(cleartext, decrypted_tally, encrypted_tally, shares)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cleartext"] = from_int(self.cleartext)
        result["decrypted_tally"] = from_int(self.decrypted_tally)
        result["encrypted_tally"] = to_class(ElGamalMessage, self.encrypted_tally)
        result["shares"] = from_list(lambda x: to_class(DecryptionShare, x), self.shares)
        return result


class BallotStyle:
    districts: List[str]
    id: str
    party_id: Optional[str]
    precincts: List[str]

    def __init__(self, districts: List[str], id: str, party_id: Optional[str], precincts: List[str]) -> None:
        self.districts = districts
        self.id = id
        self.party_id = party_id
        self.precincts = precincts

    @staticmethod
    def from_dict(obj: Any) -> 'BallotStyle':
        assert isinstance(obj, dict)
        districts = from_list(from_str, obj.get("districts"))
        id = from_str(obj.get("id"))
        party_id = from_union([from_str, from_none], obj.get("partyId"))
        precincts = from_list(from_str, obj.get("precincts"))
        return BallotStyle(districts, id, party_id, precincts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["districts"] = from_list(from_str, self.districts)
        result["id"] = from_str(self.id)
        result["partyId"] = from_union([from_str, from_none], self.party_id)
        result["precincts"] = from_list(from_str, self.precincts)
        return result


class BMDConfig:
    require_activation: Optional[bool]
    show_help_page: Optional[bool]
    show_settings_page: Optional[bool]

    def __init__(self, require_activation: Optional[bool], show_help_page: Optional[bool], show_settings_page: Optional[bool]) -> None:
        self.require_activation = require_activation
        self.show_help_page = show_help_page
        self.show_settings_page = show_settings_page

    @staticmethod
    def from_dict(obj: Any) -> 'BMDConfig':
        assert isinstance(obj, dict)
        require_activation = from_union([from_bool, from_none], obj.get("requireActivation"))
        show_help_page = from_union([from_bool, from_none], obj.get("showHelpPage"))
        show_settings_page = from_union([from_bool, from_none], obj.get("showSettingsPage"))
        return BMDConfig(require_activation, show_help_page, show_settings_page)

    def to_dict(self) -> dict:
        result: dict = {}
        result["requireActivation"] = from_union([from_bool, from_none], self.require_activation)
        result["showHelpPage"] = from_union([from_bool, from_none], self.show_help_page)
        result["showSettingsPage"] = from_union([from_bool, from_none], self.show_settings_page)
        return result


class Candidate:
    id: str
    is_write_in: Optional[bool]
    name: str
    party_id: Optional[str]

    def __init__(self, id: str, is_write_in: Optional[bool], name: str, party_id: Optional[str]) -> None:
        self.id = id
        self.is_write_in = is_write_in
        self.name = name
        self.party_id = party_id

    @staticmethod
    def from_dict(obj: Any) -> 'Candidate':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        is_write_in = from_union([from_bool, from_none], obj.get("isWriteIn"))
        name = from_str(obj.get("name"))
        party_id = from_union([from_str, from_none], obj.get("partyId"))
        return Candidate(id, is_write_in, name, party_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["isWriteIn"] = from_union([from_bool, from_none], self.is_write_in)
        result["name"] = from_str(self.name)
        result["partyId"] = from_union([from_str, from_none], self.party_id)
        return result


class TypeEnum(Enum):
    CANDIDATE = "candidate"
    YESNO = "yesno"


class Contest:
    allow_write_ins: Optional[bool]
    candidates: Optional[List[Candidate]]
    district_id: str
    id: str
    party_id: Optional[str]
    seats: Optional[float]
    section: str
    title: str
    type: TypeEnum
    description: Optional[str]
    short_title: Optional[str]

    def __init__(self, allow_write_ins: Optional[bool], candidates: Optional[List[Candidate]], district_id: str, id: str, party_id: Optional[str], seats: Optional[float], section: str, title: str, type: TypeEnum, description: Optional[str], short_title: Optional[str]) -> None:
        self.allow_write_ins = allow_write_ins
        self.candidates = candidates
        self.district_id = district_id
        self.id = id
        self.party_id = party_id
        self.seats = seats
        self.section = section
        self.title = title
        self.type = type
        self.description = description
        self.short_title = short_title

    @staticmethod
    def from_dict(obj: Any) -> 'Contest':
        assert isinstance(obj, dict)
        allow_write_ins = from_union([from_bool, from_none], obj.get("allowWriteIns"))
        candidates = from_union([lambda x: from_list(Candidate.from_dict, x), from_none], obj.get("candidates"))
        district_id = from_str(obj.get("districtId"))
        id = from_str(obj.get("id"))
        party_id = from_union([from_str, from_none], obj.get("partyId"))
        seats = from_union([from_float, from_none], obj.get("seats"))
        section = from_str(obj.get("section"))
        title = from_str(obj.get("title"))
        type = TypeEnum(obj.get("type"))
        description = from_union([from_str, from_none], obj.get("description"))
        short_title = from_union([from_str, from_none], obj.get("shortTitle"))
        return Contest(allow_write_ins, candidates, district_id, id, party_id, seats, section, title, type, description, short_title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["allowWriteIns"] = from_union([from_bool, from_none], self.allow_write_ins)
        result["candidates"] = from_union([lambda x: from_list(lambda x: to_class(Candidate, x), x), from_none], self.candidates)
        result["districtId"] = from_str(self.district_id)
        result["id"] = from_str(self.id)
        result["partyId"] = from_union([from_str, from_none], self.party_id)
        result["seats"] = from_union([to_float, from_none], self.seats)
        result["section"] = from_str(self.section)
        result["title"] = from_str(self.title)
        result["type"] = to_enum(TypeEnum, self.type)
        result["description"] = from_union([from_str, from_none], self.description)
        result["shortTitle"] = from_union([from_str, from_none], self.short_title)
        return result


class County:
    id: str
    name: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'County':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return County(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


class District:
    id: str
    name: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'District':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return District(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


class Party:
    abbrev: str
    id: str
    name: str

    def __init__(self, abbrev: str, id: str, name: str) -> None:
        self.abbrev = abbrev
        self.id = id
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Party':
        assert isinstance(obj, dict)
        abbrev = from_str(obj.get("abbrev"))
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return Party(abbrev, id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["abbrev"] = from_str(self.abbrev)
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


class Precinct:
    id: str
    name: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Precinct':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return Precinct(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


class BallotCoding:
    """The configuration file used in the election."""
    ballot_styles: List[BallotStyle]
    bmd_config: Optional[BMDConfig]
    contests: List[Contest]
    county: County
    date: str
    districts: List[District]
    parties: List[Party]
    precincts: List[Precinct]
    seal: Optional[str]
    seal_url: Optional[str]
    state: str
    title: str

    def __init__(self, ballot_styles: List[BallotStyle], bmd_config: Optional[BMDConfig], contests: List[Contest], county: County, date: str, districts: List[District], parties: List[Party], precincts: List[Precinct], seal: Optional[str], seal_url: Optional[str], state: str, title: str) -> None:
        self.ballot_styles = ballot_styles
        self.bmd_config = bmd_config
        self.contests = contests
        self.county = county
        self.date = date
        self.districts = districts
        self.parties = parties
        self.precincts = precincts
        self.seal = seal
        self.seal_url = seal_url
        self.state = state
        self.title = title

    @staticmethod
    def from_dict(obj: Any) -> 'BallotCoding':
        assert isinstance(obj, dict)
        ballot_styles = from_list(BallotStyle.from_dict, obj.get("ballotStyles"))
        bmd_config = from_union([BMDConfig.from_dict, from_none], obj.get("bmdConfig"))
        contests = from_list(Contest.from_dict, obj.get("contests"))
        county = County.from_dict(obj.get("county"))
        date = from_str(obj.get("date"))
        districts = from_list(District.from_dict, obj.get("districts"))
        parties = from_list(Party.from_dict, obj.get("parties"))
        precincts = from_list(Precinct.from_dict, obj.get("precincts"))
        seal = from_union([from_str, from_none], obj.get("seal"))
        seal_url = from_union([from_str, from_none], obj.get("sealURL"))
        state = from_str(obj.get("state"))
        title = from_str(obj.get("title"))
        return BallotCoding(ballot_styles, bmd_config, contests, county, date, districts, parties, precincts, seal, seal_url, state, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ballotStyles"] = from_list(lambda x: to_class(BallotStyle, x), self.ballot_styles)
        result["bmdConfig"] = from_union([lambda x: to_class(BMDConfig, x), from_none], self.bmd_config)
        result["contests"] = from_list(lambda x: to_class(Contest, x), self.contests)
        result["county"] = to_class(County, self.county)
        result["date"] = from_str(self.date)
        result["districts"] = from_list(lambda x: to_class(District, x), self.districts)
        result["parties"] = from_list(lambda x: to_class(Party, x), self.parties)
        result["precincts"] = from_list(lambda x: to_class(Precinct, x), self.precincts)
        result["seal"] = from_union([from_str, from_none], self.seal)
        result["sealURL"] = from_union([from_str, from_none], self.seal_url)
        result["state"] = from_str(self.state)
        result["title"] = from_str(self.title)
        return result


class ElectionParameters:
    """All the parameters necessary to form the election."""
    """The configuration file used in the election."""
    ballot_coding_file: BallotCoding
    """The date on which the election takes place."""
    date: str
    """The generator `g` of the multiplicative subgroup `Z^*_q`, where `p = 2q + 1`."""
    generator: int
    """The location where the election takes place"""
    location: str
    """The number of election trustees `n`."""
    num_trustees: int
    """The safe prime modulus `p`"""
    prime: int
    """The threshold `k` of trustees required to complete verification."""
    threshold: int

    def __init__(self, ballot_coding_file: BallotCoding, date: str, generator: int, location: str, num_trustees: int, prime: int, threshold: int) -> None:
        self.ballot_coding_file = ballot_coding_file
        self.date = date
        self.generator = generator
        self.location = location
        self.num_trustees = num_trustees
        self.prime = prime
        self.threshold = threshold

    @staticmethod
    def from_dict(obj: Any) -> 'ElectionParameters':
        assert isinstance(obj, dict)
        ballot_coding_file = BallotCoding.from_dict(obj.get("ballotCodingFile"))
        date = from_str(obj.get("date"))
        generator = from_int(obj.get("generator"))
        location = from_str(obj.get("location"))
        num_trustees = from_int(obj.get("num_trustees"))
        prime = from_int(obj.get("prime"))
        threshold = from_int(obj.get("threshold"))
        return ElectionParameters(ballot_coding_file, date, generator, location, num_trustees, prime, threshold)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ballotCodingFile"] = to_class(BallotCoding, self.ballot_coding_file)
        result["date"] = from_str(self.date)
        result["generator"] = from_int(self.generator)
        result["location"] = from_str(self.location)
        result["num_trustees"] = from_int(self.num_trustees)
        result["prime"] = from_int(self.prime)
        result["threshold"] = from_int(self.threshold)
        return result


class SelectionDecryption:
    """The decryption of the selection, including the encrypted message, the decrypted message,
    the decryption shares, and the cleartext.
    """
    """The actual value encrypted, so either a zero or a one."""
    cleartext: int
    """The decrypted message of the selection."""
    decrypted_message: int
    """The encrypted message of the selection (the one or zero)."""
    encrypted_message: ElGamalMessage
    """The decryption shares `M_i` used to compute the decryption `M`."""
    shares: List[DecryptionShare]

    def __init__(self, cleartext: int, decrypted_message: int, encrypted_message: ElGamalMessage, shares: List[DecryptionShare]) -> None:
        self.cleartext = cleartext
        self.decrypted_message = decrypted_message
        self.encrypted_message = encrypted_message
        self.shares = shares

    @staticmethod
    def from_dict(obj: Any) -> 'SelectionDecryption':
        assert isinstance(obj, dict)
        cleartext = from_int(obj.get("cleartext"))
        decrypted_message = from_int(obj.get("decrypted_message"))
        encrypted_message = ElGamalMessage.from_dict(obj.get("encrypted_message"))
        shares = from_list(DecryptionShare.from_dict, obj.get("shares"))
        return SelectionDecryption(cleartext, decrypted_message, encrypted_message, shares)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cleartext"] = from_int(self.cleartext)
        result["decrypted_message"] = from_int(self.decrypted_message)
        result["encrypted_message"] = to_class(ElGamalMessage, self.encrypted_message)
        result["shares"] = from_list(lambda x: to_class(DecryptionShare, x), self.shares)
        return result


class BallotDecryption:
    """A decryption of an encrypted ballot that was spoiled."""
    ballot_info: BallotInformation
    contests: List[List[SelectionDecryption]]

    def __init__(self, ballot_info: BallotInformation, contests: List[List[SelectionDecryption]]) -> None:
        self.ballot_info = ballot_info
        self.contests = contests

    @staticmethod
    def from_dict(obj: Any) -> 'BallotDecryption':
        assert isinstance(obj, dict)
        ballot_info = BallotInformation.from_dict(obj.get("ballot_info"))
        contests = from_list(lambda x: from_list(SelectionDecryption.from_dict, x), obj.get("contests"))
        return BallotDecryption(ballot_info, contests)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ballot_info"] = to_class(BallotInformation, self.ballot_info)
        result["contests"] = from_list(lambda x: from_list(lambda x: to_class(SelectionDecryption, x), x), self.contests)
        return result


class SchnorrProof:
    """A proof of posession of the private key.
    
    A non-interactive zero-knowledge proof of knowledge of a private key `s` corresponding to
    a public key `h`.
    """
    """The challenge `c` that is produced by hashing relevent parameters, including the original
    public key `h` and the one-time public key `k`.
    """
    challenge: int
    """The one-use public key `k = gʳ` generated from the random one-use private key `r`. This
    acts as a committment to `r`.
    """
    committment: int
    """The response `u = r + c s mod (p - 1)` to the challenge, where `r` is the one-time
    private key corresponding to the one-time public key `k`, and `s` is the private-key
    corresponding to the original public key `h`.
    """
    response: int

    def __init__(self, challenge: int, committment: int, response: int) -> None:
        self.challenge = challenge
        self.committment = committment
        self.response = response

    @staticmethod
    def from_dict(obj: Any) -> 'SchnorrProof':
        assert isinstance(obj, dict)
        challenge = from_int(obj.get("challenge"))
        committment = from_int(obj.get("committment"))
        response = from_int(obj.get("response"))
        return SchnorrProof(challenge, committment, response)

    def to_dict(self) -> dict:
        result: dict = {}
        result["challenge"] = from_int(self.challenge)
        result["committment"] = from_int(self.committment)
        result["response"] = from_int(self.response)
        return result


class TrusteePublicKey:
    """A proof of posession of the private key."""
    proof: SchnorrProof
    """An ElGamal public key."""
    public_key: int

    def __init__(self, proof: SchnorrProof, public_key: int) -> None:
        self.proof = proof
        self.public_key = public_key

    @staticmethod
    def from_dict(obj: Any) -> 'TrusteePublicKey':
        assert isinstance(obj, dict)
        proof = SchnorrProof.from_dict(obj.get("proof"))
        public_key = from_int(obj.get("public_key"))
        return TrusteePublicKey(proof, public_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["proof"] = to_class(SchnorrProof, self.proof)
        result["public_key"] = from_int(self.public_key)
        return result


class ElectionRecord:
    """All data from an ElectionGuard election."""
    """The base hash `Q` which is a SHA-256 hash of eleciton parameters including the prime
    modulus, generator, number of trustees, decryption threshold value, date, and
    jurisdictional information, as well as the contest configurations.
    """
    base_hash: str
    """The encrypted ballots cast in the election."""
    cast_ballots: List[EncryptedBallot]
    """The decryptions of the tallies of each option for each contests in the election."""
    contest_tallies: List[List[TallyDecryption]]
    """The extended base hash `Q̅`."""
    extended_base_hash: str
    """The election public key `K`."""
    joint_public_key: int
    parameters: ElectionParameters
    """The decryptions of the ballots spoiled in the election, including their encrypted
    selections, their decrypted selections, the cleartext of each selection, and proofs of
    the correctness of the decryptions.
    """
    spoiled_ballots: List[BallotDecryption]
    """The public keys/coefficient commitments for each trustee."""
    trustee_public_keys: List[List[TrusteePublicKey]]

    def __init__(self, base_hash: str, cast_ballots: List[EncryptedBallot], contest_tallies: List[List[TallyDecryption]], extended_base_hash: str, joint_public_key: int, parameters: ElectionParameters, spoiled_ballots: List[BallotDecryption], trustee_public_keys: List[List[TrusteePublicKey]]) -> None:
        self.base_hash = base_hash
        self.cast_ballots = cast_ballots
        self.contest_tallies = contest_tallies
        self.extended_base_hash = extended_base_hash
        self.joint_public_key = joint_public_key
        self.parameters = parameters
        self.spoiled_ballots = spoiled_ballots
        self.trustee_public_keys = trustee_public_keys

    @staticmethod
    def from_dict(obj: Any) -> 'ElectionRecord':
        assert isinstance(obj, dict)
        base_hash = from_str(obj.get("base_hash"))
        cast_ballots = from_list(EncryptedBallot.from_dict, obj.get("cast_ballots"))
        contest_tallies = from_list(lambda x: from_list(TallyDecryption.from_dict, x), obj.get("contest_tallies"))
        extended_base_hash = from_str(obj.get("extended_base_hash"))
        joint_public_key = from_int(obj.get("joint_public_key"))
        parameters = ElectionParameters.from_dict(obj.get("parameters"))
        spoiled_ballots = from_list(BallotDecryption.from_dict, obj.get("spoiled_ballots"))
        trustee_public_keys = from_list(lambda x: from_list(TrusteePublicKey.from_dict, x), obj.get("trustee_public_keys"))
        return ElectionRecord(base_hash, cast_ballots, contest_tallies, extended_base_hash, joint_public_key, parameters, spoiled_ballots, trustee_public_keys)

    def to_dict(self) -> dict:
        result: dict = {}
        result["base_hash"] = from_str(self.base_hash)
        result["cast_ballots"] = from_list(lambda x: to_class(EncryptedBallot, x), self.cast_ballots)
        result["contest_tallies"] = from_list(lambda x: from_list(lambda x: to_class(TallyDecryption, x), x), self.contest_tallies)
        result["extended_base_hash"] = from_str(self.extended_base_hash)
        result["joint_public_key"] = from_int(self.joint_public_key)
        result["parameters"] = to_class(ElectionParameters, self.parameters)
        result["spoiled_ballots"] = from_list(lambda x: to_class(BallotDecryption, x), self.spoiled_ballots)
        result["trustee_public_keys"] = from_list(lambda x: from_list(lambda x: to_class(TrusteePublicKey, x), x), self.trustee_public_keys)
        return result


def election_record_from_dict(s: Any) -> ElectionRecord:
    return ElectionRecord.from_dict(s)


def election_record_to_dict(x: ElectionRecord) -> Any:
    return to_class(ElectionRecord, x)
