"""Exact original-Write boundary and signed-response construction.

Placement addresses determine B and T.  K additionally needs the original
source action table and selected connector ledger; it cannot be decoded from
placement addresses alone.  No retained K or fitted response is used here.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from importlib.resources import files
import json


PLACEMENT_CODES = (46501, 46525, 49061, 81829)
BUNDLED_RESPONSE_SHA256 = "9e44bdc8373f88c5348e81b056265bb7dcb1e191772aa1c44772ea0757e40c67"


def bundled_response_bytes():
    """Read the separately identified recovered original source operand."""
    raw = files("sam_chapter1").joinpath("data/placement_response.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != BUNDLED_RESPONSE_SHA256:
        raise ValueError("Bundled original response operand changed")
    return raw


def chapter_source():
    """Generate the chapter's complete B,T,K from its bundled original ledger."""
    packet = json.loads(bundled_response_bytes())
    return generate_source(packet["source"], packet["ledger"])


def _integer(value, name):
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    return value


def _exact(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError(f"{name} must be an exact integer/rational")
    return Fraction(value)


def decode_placement(code, slots=7):
    """Decode a nonnegative base-eight address, retaining leading zero sites."""
    _integer(code, "placement code")
    _integer(slots, "slot count")
    if not 3 <= slots <= 8:
        raise ValueError("A retained cube path has between three and eight slots")
    if not 0 <= code < 8 ** slots:
        raise ValueError("Placement address does not fit its declared slots")
    return tuple((code >> (3 * (slots - i - 1))) & 7 for i in range(slots))


def encode_placement(sites):
    """Encode an ambient cube-slot address, including forbidden targets."""
    sites = tuple(sites)
    if not 3 <= len(sites) <= 8:
        raise ValueError("A retained cube path has between three and eight slots")
    result = 0
    for site in sites:
        _integer(site, "cube site")
        if not 0 <= site < 8:
            raise ValueError("Cube sites must lie between zero and seven")
        result = 8 * result + site
    return result


def is_cube_path(sites):
    """Whether labelled slots form an injective nearest-neighbor cube path."""
    sites = tuple(sites)
    return (3 <= len(sites) <= 8 and
            all(type(site) is int and 0 <= site < 8 for site in sites) and
            len(set(sites)) == len(sites) and
            all((left ^ right).bit_count() == 1
                for left, right in zip(sites, sites[1:])))


@dataclass(frozen=True)
class Boundary:
    codes: tuple
    paths: tuple
    target_codes: tuple
    B: tuple
    T: tuple


def generate_boundary(codes=PLACEMENT_CODES, slots=7):
    """Enumerate every forbidden one-slot hop with its signed weight -2.

    The two original C4-character-zero incidences add before contraction.
    Columns are sorted ambient target identities; target collisions between
    different source rows are retained, rather than merged by cube symmetry.
    """
    codes = tuple(codes)
    if not codes or len(set(codes)) != len(codes):
        raise ValueError("Supply nonempty, distinct ordered placement codes")
    paths = tuple(decode_placement(code, slots) for code in codes)
    if not all(is_cube_path(path) for path in paths):
        raise ValueError("Every source placement must be an injective cube path")
    rows = []
    for path in paths:
        row = Counter()
        for slot in range(slots):
            for bit in (1, 2, 4):
                target = list(path)
                target[slot] ^= bit
                if is_cube_path(target):
                    raise ValueError("Unexpected legal direct hop in path boundary")
                row[encode_placement(target)] -= 2
        rows.append(row)
    targets = tuple(sorted(set().union(*(set(row) for row in rows))))
    b = tuple(tuple(row.get(target, 0) for target in targets) for row in rows)
    t = tuple(tuple(sum(x * y for x, y in zip(left, right))
                    for right in b) for left in b)
    return Boundary(codes, paths, targets, b, t)


def response_return(t, responses):
    """Contract all three signed response channels: K_ij=T_ij d_i dot d_j."""
    t, responses = tuple(map(tuple, t)), tuple(map(tuple, responses))
    n = len(t)
    if not n or len(responses) != n or any(len(row) != n for row in t):
        raise ValueError("Return matrix and response extents must agree")
    if any(len(row) != 3 for row in responses):
        raise ValueError("Retain all three X/Y/Z response channels")
    t = tuple(tuple(_exact(x, "return entry") for x in row) for row in t)
    responses = tuple(tuple(_exact(x, "response entry") for x in row)
                      for row in responses)
    if any(t[i][j] != t[j][i] for i in range(n) for j in range(n)):
        raise ValueError("The original real return matrix must be symmetric")
    return tuple(tuple(t[i][j] * sum(x * y for x, y in
                                    zip(responses[i], responses[j]))
                       for j in range(n)) for i in range(n))


@dataclass(frozen=True)
class Source:
    boundary: Boundary
    responses: tuple
    witnesses: tuple
    K: tuple


def generate_source(source, ledger, codes=PLACEMENT_CODES, charges=None,
                    mode="original"):
    """Generate B,T,K from placements and explicitly supplied original records.

    ``source`` contains original ``actions`` and ``edges`` arrays. ``ledger``
    contains ``objects`` and ``cycles`` as in the retained assembly input.
    Actions are transported by endpoint sites and the retained FORWARD/REVERSE
    choice. No action is selected by matching the desired resulting matrix.
    Control modes follow the original source-bound interaction implementation.
    """
    if source is None or ledger is None:
        raise ValueError("K requires the original source actions and selected connector ledger")
    if mode not in {"original", "reciprocal", "flip_primary", "erase_sign"}:
        raise ValueError("Unknown original signed-response control mode")
    objects, cycles = ledger["objects"], ledger["cycles"]
    n = len(objects)
    boundary = generate_boundary(codes, n)
    roles, original_sites = [], []
    for obj in objects:
        role = _integer(obj["role"], "object role")
        site = _integer(obj["site"], "object site")
        if not 0 <= role < 100 or not 0 <= site < 8:
            raise ValueError("Original object role/site outside source carrier")
        if obj["kind"] not in {"proton", "neutron"}:
            raise ValueError("Original object kind must be proton or neutron")
        roles.append(role)
        original_sites.append(site)
    if len(set(roles)) != n or not is_cube_path(original_sites):
        raise ValueError("Original objects must retain distinct roles and a cube path")
    if charges is None:
        if any(obj["kind"] not in {"proton", "neutron"} for obj in objects):
            raise ValueError("Original object kind must be proton or neutron")
        charges = tuple(1 if obj["kind"] == "proton" else -1 for obj in objects)
    else:
        charges = tuple(_exact(q, "species charge") for q in charges)
    if len(charges) != n:
        raise ValueError("Species charges must retain every labelled slot")
    if len(cycles) != n - 1:
        raise ValueError("The original path ledger must retain all connectors")
    actions, edges = source["actions"], source["edges"]
    if len(actions) != 48:
        raise ValueError("Retain all 48 original directed source actions")
    lookup = {}
    for index, action in enumerate(actions):
        u, v = action["source_site"], action["target_site"]
        _integer(u, "action source site")
        _integer(v, "action target site")
        if not 0 <= u < 8 or not 0 <= v < 8 or (u ^ v).bit_count() != 1:
            raise ValueError("Source actions must be cube-edge incidences")
        choice, vertex = action["action"], action["octahedral_vertex"]
        if choice not in {"FORWARD", "REVERSE"} or vertex not in {
                "X+", "X-", "Y+", "Y-", "Z+", "Z-"}:
            raise ValueError("Invalid source action choice or signed octahedral vertex")
        if type(action["sigma_chi"]) is not int or action["sigma_chi"] not in {-1, 1}:
            raise ValueError("Retain the original signed sigma_chi")
        key = (u, v, choice)
        if key in lookup:
            raise ValueError("Ambiguous transported source action")
        lookup[key] = (index, action)
    # Validate the complete table before transporting any connector. Placements
    # can use reciprocal pairs absent from the original ledger's six links.
    for (u, v, choice), (_, action) in lookup.items():
        reciprocal_choice = "REVERSE" if choice == "FORWARD" else "FORWARD"
        try:
            _, reciprocal = lookup[(v, u, reciprocal_choice)]
        except KeyError as exc:
            raise ValueError("Every source action must retain its transported reciprocal") from exc
        if (action["octahedral_vertex"] != reciprocal["octahedral_vertex"] or
                action["sigma_chi"] != -reciprocal["sigma_chi"]):
            raise ValueError("Every source action must retain its signed transported reciprocal")
    links = set()
    for cycle in cycles:
        u, v = cycle["u"], cycle["v"]
        _integer(u, "connector source slot")
        _integer(v, "connector target slot")
        if not 0 <= u < n or not 0 <= v < n or u == v:
            raise ValueError("Connector endpoints must be distinct retained slots")
        links.add(tuple(sorted((u, v))))
        for name, table in (("forward", actions), ("reverse", actions), ("edge", edges)):
            index = _integer(cycle[name], f"connector {name} index")
            if not 0 <= index < len(table):
                raise ValueError(f"Connector {name} index out of range")
        f, r = actions[cycle["forward"]], actions[cycle["reverse"]]
        if (f["source_site"] != r["target_site"] or
                f["target_site"] != r["source_site"] or
                f["action"] == r["action"] or
                f["octahedral_vertex"] != r["octahedral_vertex"] or
                f["sigma_chi"] != -r["sigma_chi"]):
            raise ValueError("Connector must retain its signed reciprocal action")
        if (f["source_site"], f["target_site"]) != (objects[u]["site"], objects[v]["site"]):
            raise ValueError("Connector action does not match original object sites")
        edge = edges[cycle["edge"]]
        if {edge["u"], edge["v"]} != {objects[u]["role"], objects[v]["role"]}:
            raise ValueError("Connector edge does not match original object roles")
        _exact(edge["J"], "source edge J")
    if links != {(i, i + 1) for i in range(n - 1)}:
        raise ValueError("Connector ledger must retain the ordered path connectivity")
    responses, witnesses = [], []
    for sites in boundary.paths:
        response, terms = [Fraction(0)] * 3, []
        for cycle in cycles:
            u, v, old = cycle["u"], cycle["v"], cycle["forward"]
            if mode == "reciprocal":
                u, v, old = v, u, cycle["reverse"]
            choice = actions[old]["action"]
            if mode == "flip_primary":
                choice = "REVERSE" if choice == "FORWARD" else "FORWARD"
            try:
                index, action = lookup[(sites[u], sites[v], choice)]
            except KeyError as exc:
                raise ValueError("Missing transported source action") from exc
            vertex = action["octahedral_vertex"]
            axis = "XYZ".index(vertex[0])
            sigma = 1 if mode == "erase_sign" else action["sigma_chi"]
            weight = (_exact(edges[cycle["edge"]]["J"], "source edge J") *
                      (charges[u] - charges[v]) * sigma * (1 if vertex[1] == "+" else -1))
            response[axis] += weight
            terms.append((cycle["edge"], index, axis, weight))
        responses.append(tuple(response))
        witnesses.append(tuple(terms))
    responses = tuple(responses)
    return Source(boundary, responses, tuple(witnesses), response_return(boundary.T, responses))
