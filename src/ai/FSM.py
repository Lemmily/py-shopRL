__author__ = 'Emily'


class Stack:
    def __init__(self):
        self.data = []

    def pop(self, i=-1):
        return self.data.pop(i)

    def peek(self):
        return self.data[len(self.data) - 1]

    def append(self, obj):
        self.data.append(obj)


class FSM:

    def __init__(self):
        self.state_stack = Stack()

    def update(self, obj):
        if self.state_stack.peek() is not None:
            self.state_stack.peek().update(self, obj)

    def push_state(self, state):
        self.state_stack.append(state)

    def pop_state(self):
        self.state_stack.pop()


class FSMState:
    def __init__(self):
        pass

    def update(self, fsm, obj):
        pass