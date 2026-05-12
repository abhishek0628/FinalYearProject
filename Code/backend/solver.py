
from collections import deque


# =========================================
# extract message
# =========================================

def get_msg(x):

    if x.startswith("?") or x.startswith("!"):
        return x[1:]

    return x


# =========================================
# BFS SAFETY CHECKING
# =========================================

def check_safety(rbn, logger=print):

    RC = rbn["RC"]

    RL = rbn["RL"]

    unsafe_states = set(
        rbn["unsafe_states"]
    )

    # =====================================
    # INITIAL GLOBAL STATE
    # =====================================

    initial_agents = frozenset(["sleep"])

    initial_env = RL["Q0"][0]

    initial_global = (
        initial_agents,
        initial_env
    )

    # =====================================
    # BFS
    # =====================================

    q = deque()

    q.append(initial_global)

    visited = set()

    visited.add(initial_global)

    level = 0

    logger("\n========== BFS START ==========\n")

    while q:

        size = len(q)

        logger(f"\n==============================")

        logger(f"BFS LEVEL : {level}")

        logger(f"==============================\n")

        for _ in range(size):

            current_agents, current_env = q.popleft()

            logger("CURRENT GLOBAL STATE:")

            logger(
                f"Agents = {set(current_agents)} , "
                f"Env = {current_env}"
            )

            # =====================================
            # UNSAFE CHECK
            # =====================================

            unsafe_found = False

            for s in current_agents:

                if s in unsafe_states:

                    logger(
                        f"\n❌ UNSAFE STATE REACHED : {s}"
                    )

                    unsafe_found = True

                    break

            if unsafe_found:

                return {

                    "safe": False,

                    "unsafe_reached": list(
                        unsafe_states.intersection(
                            current_agents
                        )
                    ),

                    "reachable_states": [
                        {
                            "agents": list(g[0]),
                            "env": g[1]
                        }
                        for g in visited
                    ]
                }

            # =====================================
            # POSSIBLE TRANSITIONS
            # =====================================

            logger("\nPOSSIBLE TRANSITIONS:\n")

            found_transition = False

            # =====================================
            # 1. CONTRIBUTOR TAU TRANSITIONS
            # =====================================

            for (
                src,
                action,
                dst
            ) in RC["transitions"]:

                if action != "τ":
                    continue

                # =====================================
                # JOIN TRANSITION
                # =====================================

                if src == "sleep":

                    found_transition = True

                    new_agents = set(current_agents)

                    # keep sleep state
                    new_agents.add(src)

                    # add contributor
                    new_agents.add(dst)

                    new_global = (
                        frozenset(new_agents),
                        current_env
                    )

                    logger(
                        f"[JOIN] "
                        f"{src} --τ--> {dst}"
                    )

                    logger(
                        f"NEXT = "
                        f"({set(new_agents)}, "
                        f"{current_env})"
                    )

                    if new_global not in visited:

                        visited.add(new_global)

                        q.append(new_global)

                        logger("STATUS = NEW\n")

                    else:

                        logger("STATUS = VISITED\n")

                # =====================================
                # LEAVE TRANSITION
                # =====================================

                else:

                    if src not in current_agents:
                        continue

                    found_transition = True

                    new_agents = set(current_agents)

                    # contributor leaves
                    # but others may remain

                    new_agents.add(src)

                    # add sleep state
                    new_agents.add(dst)

                    new_global = (
                        frozenset(new_agents),
                        current_env
                    )

                    logger(
                        f"[LEAVE] "
                        f"{src} --τ--> {dst}"
                    )

                    logger(
                        f"NEXT = "
                        f"({set(new_agents)}, "
                        f"{current_env})"
                    )

                    if new_global not in visited:

                        visited.add(new_global)

                        q.append(new_global)

                        logger("STATUS = NEW\n")

                    else:

                        logger("STATUS = VISITED\n")

            # =====================================
            # 2. LEADER BROADCASTS
            # =====================================

            for (
                lsrc,
                laction,
                ldst
            ) in RL["transitions"]:

                # only broadcasts
                if not laction.startswith("!"):
                    continue

                # env state must match
                if lsrc != current_env:
                    continue

                leader_msg = get_msg(laction)

                possible_moves = []

                # =====================================
                # find matching contributor receives
                # =====================================

                for (
                    csrc,
                    caction,
                    cdst
                ) in RC["transitions"]:

                    # only receive transitions
                    if not caction.startswith("?"):
                        continue

                    # contributor must exist
                    if csrc not in current_agents:
                        continue

                    contributor_msg = get_msg(caction)

                    # message match
                    if contributor_msg != leader_msg:
                        continue

                    possible_moves.append(
                        (
                            csrc,
                            cdst,
                            caction
                        )
                    )

                # =====================================
                # apply simultaneous transitions
                # =====================================

                if possible_moves:

                    found_transition = True

                    logger(
                        f"[BROADCAST] "
                        f"{lsrc} --{laction}--> {ldst}"
                    )

                    logger(
                        "MATCHING CONTRIBUTORS:"
                    )

                    new_agents = set(current_agents)

                    for (
                        src,
                        dst,
                        act
                    ) in possible_moves:

                        logger(
                            f"    {src} --{act}--> {dst}"
                        )

                        # contributors remain
                        # because infinitely many
                        # may still exist

                        new_agents.add(src)

                        # some contributors move
                        # to destination state

                        new_agents.add(dst)

                    new_global = (
                        frozenset(new_agents),
                        ldst
                    )

                    logger(
                        f"NEXT = "
                        f"({set(new_agents)}, "
                        f"{ldst})"
                    )

                    if new_global not in visited:

                        visited.add(new_global)

                        q.append(new_global)

                        logger("STATUS = NEW\n")

                    else:

                        logger("STATUS = VISITED\n")

            # =====================================
            # 3. LEADER TAU TRANSITIONS
            # =====================================

            for (
                lsrc,
                laction,
                ldst
            ) in RL["transitions"]:

                if laction != "τ":
                    continue

                if lsrc != current_env:
                    continue

                found_transition = True

                new_global = (
                    current_agents,
                    ldst
                )

                logger(
                    f"[LEADER TAU] "
                    f"{lsrc} --τ--> {ldst}"
                )

                logger(
                    f"NEXT = "
                    f"({set(current_agents)}, "
                    f"{ldst})"
                )

                if new_global not in visited:

                    visited.add(new_global)

                    q.append(new_global)

                    logger("STATUS = NEW\n")

                else:

                    logger("STATUS = VISITED\n")

            # =====================================
            # NO TRANSITIONS
            # =====================================

            if not found_transition:

                logger("NO TRANSITIONS POSSIBLE\n")

        level += 1

    # =====================================
    # SAFE
    # =====================================

    logger("\n================================")

    logger("✅ SYSTEM IS SAFE")

    logger("================================\n")

    return {

        "safe": True,

        "unsafe_reached": [],

        "reachable_states": [

            {
                "agents": list(g[0]),
                "env": g[1]
            }

            for g in visited
        ]
    }


# =========================================
# STANDALONE TEST
# =========================================

if __name__ == "__main__":

    from parser import parse_input

    from encoder import encode_to_rbn

    with open("test.txt", "r") as f:

        text = f.read()

    omas = parse_input(text)

    rbn = encode_to_rbn(omas)

    result = check_safety(rbn)

    print("\n========== FINAL RESULT ==========\n")

    print(result)