import re


# =========================================
# SMART SPLIT
# =========================================

def smart_split(line):

    """
    Split by commas
    but ignore commas inside {}
    """

    parts = re.split(
        r',(?![^{]*\})',
        line
    )

    return [p.strip() for p in parts]


# =========================================
# PARSER
# =========================================

def parse_input(text, logger=print):

    logger("\n========== PARSER START ==========\n")

    sections = [
        s.strip()
        for s in text.split("#")
        if s.strip()
    ]

    logger("Sections identified:")
    logger(str(sections))

    if len(sections) < 2:

        return {
            "error": "Invalid format"
        }

    # =====================================
    # BLOCKS
    # =====================================

    agent_block = sections[0].splitlines()[1:]
    env_block = sections[1].splitlines()[1:]

    logger("\n========== AGENT BLOCK ==========\n")
    logger(str(agent_block))

    logger("\n========== ENV BLOCK ==========\n")
    logger(str(env_block))

    # =====================================
    # AGENT VARIABLES
    # =====================================

    agent_states = {}
    actions = []
    protocol = {}
    transitions = []

    initial_state = None
    leave_state = None

    standalone = []

    # =====================================
    # AGENT PARSING
    # =====================================

    for line in agent_block:

        line = line.strip()

        if not line:
            continue

        logger(f"\n[AGENT LINE] {line}")

        # ---------------------------------
        # STATE LABELS
        # ---------------------------------

        if ":" in line and all(

            ":" in p and
            p.split(":")[1].strip() in ["0", "1"]

            for p in smart_split(line)
        ):

            for p in smart_split(line):

                k, v = p.split(":")

                agent_states[k.strip()] = int(v.strip())

            logger(f"Parsed states: {agent_states}")

            continue

        # ---------------------------------
        # ACTIONS
        # ---------------------------------

        if "," in line and all(

            x.strip().startswith("a")
            for x in smart_split(line)

        ) and ":" not in line:

            actions = [
                x.strip()
                for x in smart_split(line)
            ]

            logger(f"Parsed actions: {actions}")

            continue

        # ---------------------------------
        # TRANSITIONS
        # ---------------------------------

        parts = smart_split(line)

        if len(parts) == 5:

            transition = tuple(parts)

            transitions.append(transition)

            logger(
                f"Parsed transition: {transition}"
            )

            continue

        # ---------------------------------
        # PROTOCOL
        # ---------------------------------

        if ":" in line:

            k, v = line.split(":", 1)

            protocol[k.strip()] = [
                x.strip()
                for x in smart_split(v)
            ]

            logger(
                f"Parsed protocol: "
                f"{k.strip()} -> "
                f"{protocol[k.strip()]}"
            )

            continue

        # ---------------------------------
        # INITIAL / LEAVE
        # ---------------------------------

        standalone.append(line)

        logger(
            f"Standalone item found: {line}"
        )

    # =====================================
    # INITIAL + LEAVE
    # =====================================

    if standalone:

        initial_state = standalone[0]

        logger(
            f"\nInitial state: {initial_state}"
        )

        if len(standalone) > 1:

            leave_state = standalone[1]

            logger(
                f"Leave state: {leave_state}"
            )

    # =====================================
    # ENVIRONMENT VARIABLES
    # =====================================

    env_states = []
    env_action = []
    env_protocol = {}
    env_trans = []
    env_initial = None

    env_stage = 0

    # =====================================
    # ENVIRONMENT PARSING
    # =====================================

    for line in env_block:

        line = line.strip()

        if not line:
            continue

        logger(f"\n[ENV LINE] {line}")

        parts = smart_split(line)

        # ---------------------------------
        # ENV STATES
        # ---------------------------------

        if env_stage == 0 and "," in line and ":" not in line:

            env_states = parts

            env_stage = 1

            logger(
                f"Parsed env states: {env_states}"
            )

            continue

        # ---------------------------------
        # ENV ACTIONS
        # ---------------------------------

        if env_stage == 1 and "," in line and ":" not in line:

            env_action = parts

            env_stage = 2

            logger(
                f"Parsed env actions: {env_action}"
            )

            continue

        # ---------------------------------
        # ENV PROTOCOL
        # ---------------------------------

        if ":" in line:

            k, v = line.split(":", 1)

            env_protocol[k.strip()] = v.strip()

            logger(
                f"Parsed env protocol: "
                f"{k.strip()} -> {v.strip()}"
            )

            continue

        # ---------------------------------
        # ENV TRANSITIONS
        # ---------------------------------

        if len(parts) == 4:

            transition = tuple(parts)

            env_trans.append(transition)

            logger(
                f"Parsed env transition: "
                f"{transition}"
            )

            continue

        # ---------------------------------
        # ENV INITIAL
        # ---------------------------------

        if len(parts) == 1:

            env_initial = parts[0]

            logger(
                f"Parsed env initial: "
                f"{env_initial}"
            )

    # =====================================
    # FINAL RESULT
    # =====================================

    result = {

        "states": agent_states,

        "actions": actions,

        "protocol": protocol,

        "transitions": transitions,

        "initial": initial_state,

        "leave": leave_state,

        "env_states": env_states,

        "env_action": env_action,

        "env_protocol": env_protocol,

        "env_initial": env_initial,

        "env_trans": env_trans
    }

    logger(
        "\n========== FINAL PARSED RESULT ==========\n"
    )

    logger(str(result))

    logger(
        "\n========== PARSER END ==========\n"
    )

    return result