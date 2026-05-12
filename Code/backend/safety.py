from encoder import encode_to_rbn
from FYP.Code.backend.solver import solve_crp

def check_safety(data):
    rbn = encode_to_rbn(data)

    unsafe_states = [
        s for s, cap in data["state_capacity"].items()
        if cap == 0
    ]

    return solve_crp(rbn, unsafe_states)