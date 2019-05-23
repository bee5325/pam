from enum import Enum


class Action():

    def __init__(self, duration=0, dest=""):
        self.type = type(self).__name__
        self.duration = duration
        self.dest = dest
        self.start_state = dict()
        self.cumm_time = 0

    def state_after(self, time_passed):
        # to be overriden by child
        return None

    def get_end_state(self):
        return self.state_after(self.duration)


class ActMove(Action):

    def state_after(self, time_passed):
        t_ratio = time_passed/self.duration
        startx, starty = self.start_state["position"]
        destx, desty = self.dest
        return dict(self.start_state,
                    position=(startx + ((destx-startx)*t_ratio),
                              starty + ((desty-starty)*t_ratio)))


class ActStop(Action):

    def state_after(self, time_passed):
        return self.start_state


class ActColor(Action):

    def state_after(self, time_passed):
        t_ratio = time_passed/self.duration
        startr, startg, startb = self.start_state["color"]
        destr, destg, destb = self.dest
        return dict(self.start_state,
                    color=(startr + ((destr-startr)*t_ratio),
                           startg + ((destg-startg)*t_ratio),
                           startb + ((destb-startb)*t_ratio)))


class ActRotate(Action):

    def state_after(self, time_passed):
        return self.start_state


class Actions():

    def __init__(self):
        self.actions = list()
        self.end_time = 0
        self.start_states = {"position": (0, 0),
                             "color": (255, 255, 255),
                             "angle": 0}

    def init_states(self, updatedict):
        self.start_states.update(updatedict)

    def add_action(self, action, duration=0, dest=""):
        new_act = action(duration, dest)

        # setting start state for new item
        if self.actions:
            last_action = self.actions[-1]
            new_act.start_state.update(last_action.get_end_state())
            new_act.cumm_time = last_action.cumm_time + last_action.duration
        else:  # no action added yet (the only on is the stop at the end)
            new_act.start_state.update(self.start_states)
            new_act.cumm_time = 0
        # the last action will always be stop
        self.actions.append(new_act)
        self.end_time = new_act.cumm_time + new_act.duration

    def __len__(self):
        return len(self.actions)

    def action_at(self, time):
        for act in self.actions:
            if (act.cumm_time + act.duration) > time:
                return act
        no_action = ActStop()
        no_action.cumm_time = self.end_time
        if self.actions:
            no_action.start_state = self.actions[-1].get_end_state()
        else:
            no_action.start_state.update(self.start_states)
        return no_action

    def state_at(self, time):
        act = self.action_at(time)
        return act.state_after(time-act.cumm_time)

    def __getitem__(self, idx):
        return self.actions[idx]
