from sentient import Motive

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
            if self.state_stack.peek().update(self, obj):
                self.state_stack.pop()

    def push_state(self, state):
        self.state_stack.append(state)

    def pop_state(self):
        self.state_stack.pop()


class FSMState:
    def __init__(self):
        pass

    def update(self, fsm, obj):
        # base state don't pop
        return False


class HeroBrain(FSM):
    def __init__(self, hero):
        FSM.__init__(self)
        self.hero = hero
        self.stack = Stack()
        self.active_state = self.idle

    def update(self, dt):
        self.active_state(dt)

    def idle(self, dt):
        if self.hero.has_motive():
            pass
        else:
            self.hero.self_assessment()
            self.hero.assess_motives()
            print self.hero.motive


class Hero:
    def __init__(self):
        self.attributes = {
            "hp": 10,
            "max_hp": 10,
            "gold": 100,
            "adventure": 0,
            "inventory_slots": 10,
            "items": ["sword", "shield", "helmet"]
        }

        # collection of built up motivation.
        self.motivations = []
        self.dict_motive = {}
        # whats the current driving force here?
        self.motive = None
        # self.goal sme kind of validation function it needs 2 meet? eg "if self.gold == 100" if true === goal achieved.
        self.goal = None

    def self_assessment(self):
        curr_hp = self.attributes["hp"]
        max_hp = self.attributes["max_hp"]

        motive = None

        if curr_hp < max_hp:
            if curr_hp >= max_hp * 0.8:  # 80% health
                motive = Motive(1, "health")
            elif curr_hp >= max_hp * 0.5:  # 50% health
                motive = Motive(2, "health")
            elif curr_hp >= max_hp * 0.3:  # 30% health
                motive = Motive(4, "health", "comfort")
            elif curr_hp >= max_hp * 0.1:  # 10% health
                motive = Motive(7, "health", "comfort")
        self.dict_motive[motive.main].append(motive)
        print ("boop")

    def assess_motives(self):
        for motive in self.motivations:
            if motive.main in self.dict_motive:
                self.dict_motive[motive.main] += motive.importance
            else:
                self.dict_motive[motive.main] = motive.importance

            if motive.other != "":
                if motive.other in self.dict_motive:
                    self.dict_motive[motive.other] += motive.other_imp
                else:
                    self.dict_motive[motive.other] = motive.other_imp

        highest_no = 0
        highest = ""
        for key in self.dict_motive.keys():
            if self.dict_motive[key] > highest_no:
                highest = key
                highest_no = self.dict_motive[key]

        return highest, highest_no
