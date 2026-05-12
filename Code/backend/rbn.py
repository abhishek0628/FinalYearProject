class RBN:
    def __init__(self, data):
        self.leader_states = data["leader_states"]
        self.contributor_states = data["contributor_states"]
        self.leader_transitions = data["leader_transitions"]
        self.contributor_transitions = data["contributor_transitions"]
        self.initial_counts = data["initial_counts"]
        self.initial_leader = data["initial_leader"]