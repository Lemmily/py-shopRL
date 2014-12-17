__author__ = 'James'
# DATE   : 13 March 2012
# FILE   : goap.py
# AUTHOR : Stavros Vassos
# EMAIL  : stavros@cs.toronto.edu
# WWW    : stavros.lostre.org/pyPlan

from goap import Action
from goap import WorldModel
from goap import PlanningTask


def example1():
    model = WorldModel(["empty-hands", "empty-backpack", "at-armory"])
    print "Initial world model: ",
    model.nice_print()

    print "\nUpdating the model with respect to a pickup-spear action"
    action = Action("pickup-spear",
                    ["at-armory", "empty-hands"],
                    ["hold-spear"],
                    ["empty-hands"])
    model.execute(action)

    print "Successor world model: ",
    model.nice_print()

    print "\nUpdating the model with respect to a drop-spear action"
    action = Action("pickup-spear",
                    ["at-armory", "holds-spear"],
                    ["empty-hands"],
                    ["hold-spear"])
    model.execute(action)

    print "Successor world model: ",
    model.nice_print()


def example2():
    initial_model = WorldModel(["empty-hands",
                                "empty-backpack",
                                "ready-to-move"])
    goal = ["carry-food"]

    actions = []

    actions.append(Action("pickup-spear",
                          ["at-armory", "empty-hands"],
                          ["hold-spear"],
                          ["empty-hands"]))

    actions.append(Action("store-spear",
                          ["at-armory", "hold-spear"],
                          ["empty-hands"],
                          ["hold-spear"]))

    actions.append(Action("hunt-deer",
                          ["at-forest", "hold-spear", "empty-backpack"],
                          ["carry-rawmeat"],
                          ["empty-backpack"]))

    actions.append(Action("cook-rawmeat",
                          ["at-kitchen", "carry-rawmeat"],
                          ["carry-food"],
                          ["carry-rawmeat"]))

    actions.append(Action("new-destination",
        [],
                          ["ready-to-move"],
                          ["at-forest", "at-gates", "at-armory",
                           "at-kitchen", "at-farmhouse"]))

    actions.append(Action("moveto-armory",
                          ["ready-to-move"],
                          ["at-armory"],
                          ["ready-to-move"]))

    actions.append(Action("moveto-kitchen",
                          ["ready-to-move"],
                          ["at-kitchen"],
                          ["ready-to-move"]))

    actions.append(Action("moveto-gates",
                          ["ready-to-move"],
                          ["at-gates"],
                          ["ready-to-move"]))

    actions.append(Action("moveto-forest",
                          ["ready-to-move"],
                          ["at-forest"],
                          ["ready-to-move"]))

    actions.append(Action("moveto-farmhouse",
                          ["ready-to-move"],
                          ["at-farmhouse"],
                          ["ready-to-move"]))

    task = PlanningTask(initial_model, actions, goal)
    print "Solving the peasant planning problem"
    plan = task.depth_first_search(8)
    print "Plan: ",
    print plan

    # >>>
    #
    #  Plan: ['moveto-armory', 'pickup-spear',
    #         'new-destination', 'moveto-forest',
    #         'hunt-deer', 'new-destination',
    #         'moveto-kitchen', 'cook-rawmeat']

    print "\nAdding harvesting for rice as a new available action"
    actions.append(Action("harvest-rice",
                          ["at-farmhouse", "empty-backpack"],
                          ["carry-food"],
                          ["empty-backpack"]))

    print "Solving the peasant planning problem"
    task = PlanningTask(initial_model, actions, goal)
    plan = task.depth_first_search(8)
    print "Plan: ",
    print plan

# >>>
#
#  Plan:  ['moveto-farmhouse', 'harvest-rice']

