# Simple STRIPS planning in Python
# DATE   : 13 March 2012
# FILE   : goap.py
# AUTHOR : Stavros Vassos
# EMAIL  : stavros@cs.toronto.edu
# WWW    : stavros.lostre.org/pyPlan


class WorldModel:
    # A world model is initialized with a list of facts
    def __init__(self, facts):
        self.facts = facts

    # Adding a fact in a world model is simply adding it
    # in the internal list of facts unless already present
    def add_fact(self, fact):
        if fact not in self.facts:
            self.facts.append(fact)

    # Removing a fact in a world model is simply taking it
    # out of the internal list of facts if present
    def remove_fact(self, fact):
        if fact in self.facts:
            self.facts.remove(fact)

    # A goal is satisfied by the world model if all facts
    # in the goal list are present in the world model
    def satisfies_goal(self, goal):
        for fact in goal:
            if fact not in self.facts:
                # If any fact in the goal list is absent then
                # return false
                return False
        # If all facts in the goal list are present in the
        # world model then return true.
        return True

        # Checks if an action can be executed in the world model

    def can_execute(self, action):
        # An action can be executed in a world model if the list of
        # facts called preconditions are present in the world model
        for fact in action.preconds:
            # If any fact in the action list of preconditions is
            # absent then return false
            if fact not in self.facts:
                return False
        # If all facts in the action list of precondition are
        # present in the world model then return true.
        return True

    # Executes an action in the world model updating the facts
    # of the model
    def execute(self, action):
        # When an action is executed it alters the world model by
        # removing from the model the negative effects of the action
        for fact in action.neg_effects:
            self.remove_fact(fact)
        # and inserting the positive effects of the action.
        for fact in action.pos_effects:
            self.add_fact(fact)

    # Creates and returns a copy of the successor of the world
    # model using execute_action()
    def create_successor(self, action):
        successor_model = WorldModel(list(self.facts))
        successor_model.execute(action)
        return successor_model

    # Print the world model as a list of facts for display
    # and debug purposes
    def nice_print(self):
        for fact in self.facts:
            print fact,
        print ""


class Action:
    # An action is defined by a name, and three lists of facts:
    # a list of preconditions, a list of positive, and a list
    # of negative effects
    def __init__(self, name, preconds, pos_effects, neg_effects):
        self.name = name
        self.preconds = preconds
        self.pos_effects = pos_effects
        self.neg_effects = neg_effects

    # Print the action for display and debug purposes
    def nice_print(self):
        print "Action " + self.name
        print "Preconditions: ",
        for fact in self.preconds:
            print fact,
        print ""
        print "Positive effects: ",
        for fact in self.pos_effects:
            print fact,
        print ""
        print "Negative effects: ",
        for fact in self.neg_effects:
            print fact,
        print ""


class PartialPlan:
    # A partial plan holds a list of actions that have been
    # executed so far and the resulting world model
    def __init__(self, actions, model):
        self.actions = actions
        self.model = model

    def nice_print(self):
        print "Partial actions: ",
        print self.actions
        print "Partial world model: ",
        self.model.nice_print()


class PlanningTask:
    def __init__(self, initial_model, available_actions, goal):
        self.initial_model = initial_model
        self.available_actions = available_actions
        self.goal = goal

    def depth_first_search(self, bound):
        # Initialize search
        node = PartialPlan([], self.initial_model)
        open_nodes = [node]

        # As long as there are nodes in the list of open nodes
        # proceed with searching for a solution to the planning task
        while open_nodes:
            # Take the last node from the list of open search nodes
            node = open_nodes.pop()
            # node.nice_print()

            # If the model of the partial plan satisfies the goal then
            # the corresponding actions that led to this world model is
            # a solution to the planning task
            if node.model.satisfies_goal(self.goal):
                return node.actions

            # If the actions of the partial plan have already reached
            # the maximum number of actions specified by the bound
            # then do not do any more search for this partial plan
            if len(node.actions) == bound:
                continue

            # Otherwise generate all the successor world models using
            # those actions that can be executed in the model of the
            # partial plan and add them at the end of the open list of
            # nodes as new partial plans
            for action in self.available_actions:
                if node.model.can_execute(action):
                    successor = node.model.create_successor(action)
                    actions = list(node.actions)
                    actions.append(action.name)
                    open_nodes.append(PartialPlan(actions, successor))

                    # That's all, now loop back to check the list of open nodes

        # If the list of open nodes is empty then there is no
        # solution for the planning task with a number of actions
        # that does not exceed the given bound.
        return False
