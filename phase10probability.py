import re
import random as _rnd
from collections import Counter, defaultdict
import phase10config

MC_TRIALS_DEFAULT = phase10config.CONFIG["MC_TRIALS_DEFAULT"]
PHASE_PROB_CACHE = phase10config.CONFIG.get("PHASE_PROB_CACHE", {})


# -------------------- Deck model --------------------


def build_deck():
    """
    Phase 10 deck model:
    - 96 number cards: values 1..12, 4 colors, 2 copies each
    - 8 Wild
    - 4 Skip (cannot help satisfy requirements)
    """
    colors = ["R", "G", "B", "Y"]
    deck = []
    for _copy in range(2):
        for c in colors:
            for v in range(1, 13):
                deck.append(("num", v, c))
    for _ in range(8):
        deck.append(("wild", None, None))
    for _ in range(4):
        deck.append(("skip", None, None))
    return deck


def draw_hand(rng=None):
    if rng is None:
        rng = _rnd
    deck = build_deck()
    rng.shuffle(deck)
    return deck[:10]


def hand_counts(hand):
    nums_by_value = defaultdict(list)   # value -> list of (value,color)
    color_counts = Counter()
    wilds = 0
    skips = 0
    for t, v, c in hand:
        if t == "num":
            nums_by_value[v].append((v, c))
            color_counts[c] += 1
        elif t == "wild":
            wilds += 1
        else:
            skips += 1
    return nums_by_value, color_counts, wilds, skips


# -------------------- Parsers --------------------

_runpairs_re = re.compile(r"\brun of (\d+)\s+pairs\b", re.I)
_run_re2 = re.compile(r"\b(\d+)\s+runs?\s+of\s+(\d+)\b", re.I)
_run_re1 = re.compile(r"\brun of (\d+)\b", re.I)
_set_re = re.compile(r"\b(\d+)\s+sets?\s+of\s+(\d+)\b", re.I)
_colorblock_re = re.compile(r"\b(\d+)\s+of\s+one\s+color\b", re.I)
_evenodd_re = re.compile(r"\b(\d+)\s+(?:color\s+)?(even|odd|even or odd)\s+of\s+(\d+)\b", re.I)
_hilo_re = re.compile(r"\b(\d+)\s+(over|under)\s+(\d+)\b", re.I)


def parse_part(s):
    """
    Parse a single requirement string (e.g. '6 of One Color', 'Run of 3 Pairs').
    Returns a list of (kind, param) tasks.
    """
    s = s.strip()

    # Run of X Pairs
    m = _runpairs_re.search(s)
    if m:
        return [("runpairs", int(m.group(1)))]

    # X Runs of Y
    m = _run_re2.search(s)
    if m:
        x = int(m.group(1))
        y = int(m.group(2))
        return [("run", y)] * x

    # Run of X
    m = _run_re1.search(s)
    if m:
        return [("run", int(m.group(1)))]

    # X Sets of Y
    m = _set_re.search(s)
    if m:
        x = int(m.group(1))
        y = int(m.group(2))
        return [("set", y)] * x

    # X of One Color
    m = _colorblock_re.search(s)
    if m:
        return [("color", int(m.group(1)))]

    # 1 (Color) Even/Odd of Y
    m = _evenodd_re.search(s)
    if m:
        x = int(m.group(1))  # usually 1 in your strings
        mode = m.group(2).lower()
        y = int(m.group(3))
        if mode == "even or odd":
            mode = "either"
        color_required = "color" in s.lower()
        return [("evenodd", (y, mode, color_required))]

    # X Over/Under N
    m = _hilo_re.search(s)
    if m:
        x = int(m.group(1))
        ou = m.group(2).lower()
        thr = int(m.group(3))
        return [("hilo", (x, ou, thr))]

    # Unknown pattern → treat as impossible
    return [("unknown", s)]


def tasks_from_selection(selection):
    """
    Convert a list of PhasePart objects (selection) into a list of tasks.
    Each PhasePart's .str is parsed into zero or more (kind, param) tasks.
    """
    tasks = []
    for part in selection:
        tasks.extend(parse_part(getattr(part, "str", "")))
    return tasks


# -------------------- Feasibility helpers --------------------

def can_take_run(nums_by_value, wilds, run_len):
    for start in range(1, 13 - run_len + 1):
        need = 0
        for v in range(start, start + run_len):
            if len(nums_by_value[v]) >= 1:
                continue
            need += 1
            if need > wilds:
                break
        if need <= wilds:
            # consume
            for v in range(start, start + run_len):
                if len(nums_by_value[v]) >= 1:
                    nums_by_value[v].pop()
                else:
                    wilds -= 1
            return True, wilds
    return False, wilds


def can_take_runpairs(nums_by_value, wilds, pair_run_len):
    for start in range(1, 13 - pair_run_len + 1):
        need = 0
        deficits = []
        for v in range(start, start + pair_run_len):
            have = len(nums_by_value[v])
            d = max(0, 2 - have)
            need += d
            deficits.append((v, d))
            if need > wilds:
                break
        if need <= wilds:
            # consume
            for v, d in deficits:
                take = min(2, len(nums_by_value[v]))
                for _ in range(take):
                    nums_by_value[v].pop()
                if d > 0:
                    wilds -= d
            return True, wilds
    return False, wilds


def can_take_set(nums_by_value, wilds, set_size):
    best_v = None
    best_real = -1
    for v in range(1, 13):
        have = len(nums_by_value[v])
        need = max(0, set_size - have)
        if need <= wilds and have > best_real:
            best_real = have
            best_v = v
    if best_v is None:
        return False, wilds
    take = min(set_size, len(nums_by_value[best_v]))
    for _ in range(take):
        nums_by_value[best_v].pop()
    wilds -= max(0, set_size - take)
    return True, wilds


def can_take_colorblock(color_counts, wilds, target):
    best_color, best_cnt = None, -1
    for c, cnt in color_counts.items():
        if cnt > best_cnt:
            best_color, best_cnt = c, cnt
    if best_color is None:
        best_color, best_cnt = "R", 0
    need = max(0, target - best_cnt)
    if need > wilds:
        return False, wilds
    real_take = min(target, color_counts[best_color])
    color_counts[best_color] -= real_take
    wilds -= (target - real_take)
    return True, wilds


def can_take_evenodd(nums_by_value, color_counts, wilds, target, mode, color_required):
    def is_even(v):
        return (v % 2) == 0

    want_even = None
    if mode == "even":
        want_even = True
    elif mode == "odd":
        want_even = False

    # No color restriction: any color works
    if not color_required:
        real = 0
        picked = []
        for v in range(1, 13):
            if want_even is None or (is_even(v) == want_even):
                k = len(nums_by_value[v])
                take = min(k, target - real)
                if take > 0:
                    real += take
                    picked.extend([v] * take)
                if real >= target:
                    break
        need = max(0, target - real)
        if need > wilds:
            return False, wilds
        for v in picked:
            nums_by_value[v].pop()
        wilds -= need
        return True, wilds

    # Color-specific even/odd (e.g. "1 Color Even of 4")
    best_color = None
    best_real = -1
    colors = list(color_counts.keys()) or ["R", "G", "B", "Y"]
    for c in colors:
        real = 0
        for v in range(1, 13):
            if want_even is None or (is_even(v) == want_even):
                k = sum(1 for (_v, _c) in nums_by_value[v] if _c == c)
                real += k
        if real > best_real:
            best_real = real
            best_color = c

    need = max(0, target - best_real)
    if need > wilds:
        return False, wilds

    remaining = target
    for v in range(1, 13):
        if remaining == 0:
            break
        if want_even is None or (is_even(v) == want_even):
            keep = []
            for (vv, cc) in nums_by_value[v]:
                if cc == best_color and remaining > 0:
                    remaining -= 1
                else:
                    keep.append((vv, cc))
            nums_by_value[v] = keep

    wilds -= (target - min(target, best_real))
    return True, wilds


def can_take_hilo(nums_by_value, wilds, target, over_under, thresh):
    def ok(v):
        return v > thresh if over_under == "over" else v < thresh

    real = 0
    picked = []
    for v in range(1, 13):
        if ok(v):
            k = len(nums_by_value[v])
            take = min(k, target - real)
            if take > 0:
                real += take
                picked.extend([v] * take)
            if real >= target:
                break
    need = max(0, target - real)
    if need > wilds:
        return False, wilds
    for v in picked:
        nums_by_value[v].pop()
    wilds -= need
    return True, wilds


# -------------------- Phase feasibility and MC --------------------

def can_satisfy_phase(selection, hand):
    """
    selection: list of PhasePart
    hand: list of (type, value, color) tuples
    """
    nums_by_value, color_counts, wilds, _ = hand_counts(hand)
    tasks = tasks_from_selection(selection)

    # Priority helps reduce conflicts: sets/color first, then structured runs, then hi/lo
    priority = {"set": 0, "color": 1, "runpairs": 2, "run": 3, "evenodd": 4, "hilo": 5, "unknown": 9}
    tasks.sort(key=lambda t: priority.get(t[0], 9))

    for kind, param in tasks:
        if kind == "set":
            ok, wilds = can_take_set(nums_by_value, wilds, param)
        elif kind == "color":
            ok, wilds = can_take_colorblock(color_counts, wilds, param)
        elif kind == "runpairs":
            ok, wilds = can_take_runpairs(nums_by_value, wilds, param)
        elif kind == "run":
            ok, wilds = can_take_run(nums_by_value, wilds, param)
        elif kind == "evenodd":
            y, mode, color_required = param
            ok, wilds = can_take_evenodd(nums_by_value, color_counts, wilds, y, mode, color_required)
        elif kind == "hilo":
            x, ou, thr = param
            ok, wilds = can_take_hilo(nums_by_value, wilds, x, ou, thr)
        else:
            ok = False

        if not ok:
            return False

    return True


def estimate_phase_prob_mc(selection, trials=MC_TRIALS_DEFAULT, seed=1337):
    wins = 0
    rng = _rnd.Random(seed)
    for _ in range(trials):
        hand = draw_hand(rng)
        if can_satisfy_phase(selection, hand):
            wins += 1
    return wins / trials


def _phase_key(selection):
    # create an order-independent key from the phase part strings
    parts = []
    for p in selection:
        s = getattr(p, "str", "")
        parts.append(s.strip().lower())
    parts.sort()
    return tuple(parts)


def Total_Prob_MC(array):
    key = _phase_key(array)
    if key in PHASE_PROB_CACHE:
        return PHASE_PROB_CACHE[key]
    val = estimate_phase_prob_mc(array, MC_TRIALS_DEFAULT)
    PHASE_PROB_CACHE[key] = val
    return val


def Sort_Total_Prob(array_of_arrays):
    # compute and attach MC probability to each phase (reuse .probability field)
    for phase in array_of_arrays:
        mc = Total_Prob_MC(phase)
        for part in phase:
            part.probability = mc

    # easiest first (highest success rate)
    return sorted(array_of_arrays, key=lambda arr: arr[0].probability, reverse=True)

