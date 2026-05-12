# from collections import defaultdict

# def encode_to_rbn(omas):
#     transitions = omas.get("transitions", [])
#     agents = omas.get("agents", [])
#     init = omas.get("initial", {})

#     graph = defaultdict(list)

#     for t in transitions:
#         if len(t) < 5:
#             continue

#         src, agent, act, _, dst = t
#         graph[(src, agent)].append(dst)

#     return {
#         "graph": dict(graph),
#         "agents": agents,
#         "initial": init,
#         "states": omas.get("states", {})
#     }

from collections import defaultdict

def encode_to_rbn(omas):
    transitions = omas.get("transitions", [])
    agents = omas.get("agents", [])
    initial = omas.get("initial", {})

    graph = defaultdict(list)

    for t in transitions:
        if len(t) < 5:
            continue

        src, agent, act, _, dst = t
        graph[(src, agent)].append(dst)

    # FIX: fallback if initial missing
    if not initial:
        initial = {"unknown": agents}

    return {
        "graph": graph,
        "agents": agents,
        "initial": initial
    }