
def normalize_actions(x):

    """
    Converts:
        a1              -> ['a1']
        {a1,a2}         -> ['a1','a2']
        ['a1','a2']     -> ['a1','a2']
    """

    if isinstance(x, list):
        return x

    x = x.strip()

    if x.startswith("{") and x.endswith("}"):

        inner = x[1:-1].strip()

        if not inner:
            return []

        return [
            a.strip()
            for a in inner.split(",")
        ]

    return [x]


# =====================================
# OMAS -> RBN
# =====================================

def encode_to_rbn(omas, logger=None):

    # =====================================
    # LOGGER
    # =====================================

    def log(msg):

        if logger:
            logger(msg)

        print(msg)

    log("\n========== ENCODING START ==========\n")

    L = list(omas["states"].keys())
    LE = omas["env_states"]

    transitions = omas["transitions"]
    env_trans = omas["env_trans"]

    env_protocol = omas["env_protocol"]
    protocol = omas["protocol"]

    initial_agent_state = omas["initial"]
    leave_state = omas.get("leave")

    # =====================================
    # RC (contributors)
    # =====================================

    RC = {
        "states": set(L + ["sleep"]),
        "transitions": [],
        "Q0": ["sleep"]
    }

    # =====================================
    # RL (leader)
    # =====================================

    RL = {
        "states": set(LE),
        "transitions": [],
        "Q0": [omas["env_initial"]]
    }

    Sigma = set()

    # =====================================
    # JOIN
    # =====================================

    RC["transitions"].append(
        ("sleep", "τ", initial_agent_state)
    )

    log(
        f"Added JOIN transition: "
        f"(sleep, τ, {initial_agent_state})"
    )

    # =====================================
    # LEAVE
    # =====================================

    if leave_state:

        leave_states = [
            x.strip()
            for x in leave_state.split(",")
        ]

        for ls in leave_states:

            RC["transitions"].append(
                (ls, "τ", "sleep")
            )

            log(
                f"Added LEAVE transition: "
                f"({ls}, τ, sleep)"
            )

    # =====================================
    # MAIN ENCODING
    # =====================================

    for (
        ele,
        env_action,
        env_agent_actions,
        enxt
    ) in env_trans:

        log(
            f"\nChecking environment transition:\n"
            f"{ele} --{env_action}/{env_agent_actions}--> {enxt}"
        )

        # =====================================
        # protocol check
        # =====================================

        allowed_actions = [
            x.strip()
            for x in env_protocol.get(ele, "").split(",")
            if x.strip()
        ]

        log(f"Allowed env actions at {ele}: {allowed_actions}")

        if env_action not in allowed_actions:

            log(
                f"SKIPPED: {env_action} "
                f"not allowed in protocol"
            )

            continue

        # =====================================
        # joint actions
        # =====================================

        joint_actions = normalize_actions(
            env_agent_actions
        )

        joint_actions = sorted(joint_actions)

        log(f"Joint actions: {joint_actions}")

        prev_leader_state = ele

        # =====================================
        # sequential broadcasts
        # =====================================

        for i, current_action in enumerate(joint_actions):

            prefix = joint_actions[:i]

            if not prefix:
                prefix_str = "φ"
            else:
                prefix_str = (
                    "{"
                    + ",".join(prefix)
                    + "}"
                )

            msg = (
                f"({env_action},"
                f"({current_action},{prefix_str}))"
            )

            log(f"\nBuilding message: {msg}")

            Sigma.add(f"!{msg}")
            Sigma.add(f"?{msg}")

            # =====================================
            # RC transitions
            # =====================================

            for (
                src,
                ag_action,
                ag_env_action,
                other_actions,
                dst
            ) in transitions:

                other_actions = normalize_actions(
                    other_actions
                )

                log(
                    f"Checking agent transition:\n"
                    f"({src}, {ag_action}, "
                    f"{ag_env_action}, "
                    f"{other_actions}, {dst})"
                )

                # env consistency
                if ag_env_action != env_action:
                    continue

                # serialized action match
                if ag_action != current_action:
                    continue

                # protocol consistency
                if ag_action not in protocol.get(src, []):
                    continue

                # same joint action
                if sorted(other_actions) != sorted(joint_actions):
                    continue

                RC["transitions"].append(
                    (
                        src,
                        f"?{msg}",
                        dst
                    )
                )

                log(
                    f"Added RC transition:\n"
                    f"({src}, ?{msg}, {dst})"
                )

            # =====================================
            # RL transitions
            # =====================================

            if i == len(joint_actions) - 1:

                next_leader_state = enxt

            else:

                next_leader_state = (
                    f"{ele}_"
                    f"{'_'.join(joint_actions[:i+1])}"
                )

                RL["states"].add(
                    next_leader_state
                )

            RL["transitions"].append(
                (
                    prev_leader_state,
                    f"!{msg}",
                    next_leader_state
                )
            )

            log(
                f"Added RL transition:\n"
                f"({prev_leader_state}, "
                f"!{msg}, "
                f"{next_leader_state})"
            )

            prev_leader_state = next_leader_state

    # =====================================
    # REMOVE DUPLICATES
    # =====================================

    RC["transitions"] = sorted(
        list(set(RC["transitions"]))
    )

    RL["transitions"] = sorted(
        list(set(RL["transitions"]))
    )

    log("\nDuplicates removed")

    # =====================================
    # UNSAFE STATES
    # =====================================

    unsafe_states = [
        s
        for s, label in omas["states"].items()
        if label == 0
    ]

    log(f"Unsafe states: {unsafe_states}")

    # =====================================
    # SAFETY FORMULA
    # =====================================

    safety_formula = [
        f"#({u}) >= 1"
        for u in unsafe_states
    ]

    log(f"Safety formula: {safety_formula}")

    log("\n========== ENCODING FINISHED ==========\n")

    # =====================================
    # RESULT
    # =====================================

    return {

        "RC": {
            "states": sorted(list(RC["states"])),
            "transitions": RC["transitions"],
            "Q0": RC["Q0"]
        },

        "RL": {
            "states": sorted(list(RL["states"])),
            "transitions": RL["transitions"],
            "Q0": RL["Q0"]
        },

        "Sigma": sorted(list(Sigma)),

        "unsafe_states": unsafe_states,

        "safety_formula": safety_formula
    }