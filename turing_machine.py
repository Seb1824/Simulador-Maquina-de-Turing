class TuringMachine:
    def __init__(self, tape="", blank=" ", start_state="q0", accept_state="q_accept", reject_state="q_reject"):
        self.tape = list(tape)
        self.blank = blank
        self.head = 0
        self.state = start_state
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = {}

    def set_transition(self, state, symbol, next_state, write_symbol, move):
        self.transitions[(state, symbol)] = (next_state, write_symbol, move)

    def step(self):
        current_symbol = self.tape[self.head] if self.head < len(self.tape) else self.blank
        key = (self.state, current_symbol)
        if key in self.transitions:
            next_state, write_symbol, move = self.transitions[key]
            self.tape[self.head] = write_symbol
            self.state = next_state
            self.head += 1 if move == 'R' else -1
        else:
            self.state = self.reject_state

    def run(self, max_steps=1000):
        steps = 0
        while self.state != self.accept_state and self.state != self.reject_state and steps < max_steps:
            self.step()
            steps += 1
        return ''.join(self.tape), self.state
