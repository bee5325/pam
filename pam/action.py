from enum import Enum


class Action():

    def __init__(self, duration=0, dest=""):
        self.type = type(self).__name__
        self.duration = duration
        self.dest = dest
        self.start_state = dict()
        self.cumm_time = 0
        self.default_start_state()

    def default_start_state(self):
        # to be overriden by child
        pass

    def state_after(self, time_passed):
        # to be overriden by child
        return None

    def get_end_state(self):
        return self.state_after(self.duration)


class ActMove(Action):

    def default_start_state(self):
        self.start_state["position"] = (0, 0)

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


class ActRotate(Action):

    def default_start_state(self):
        self.start_state["angle"] = 0

    def state_after(self, time_passed):
        return self.start_state


class Actions():

    def __init__(self):
        self.actions = list()
        last_act = ActStop(0)
        self.actions.append(last_act)

    def add_action(self, action, duration=0, dest=""):
        new_act = action(duration, dest)

        # setting start state for new item
        if len(self.actions) >= 2:
            last_action = self.actions[-2]
            new_act.start_state.update(last_action.get_end_state())
            new_act.cumm_time = last_action.cumm_time + last_action.duration
        else:  # no action added yet (the only on is the stop at the end)
            new_act.cumm_time = 0
        # the last action will always be stop
        self.actions.insert(-1, new_act)

        # updating start state for the stop at the end
        self.actions[-1].start_state = new_act.get_end_state()
        self.actions[-1].cumm_time = new_act.cumm_time + new_act.duration

    def __len__(self):
        return len(self.actions)

    def action_at(self, time):
        for act in self.actions:
            if (act.cumm_time + act.duration) > time:
                return act
        return self.actions[-1]

    def state_at(self, time):
        act = self.action_at(time)
        return act.state_after(time-act.cumm_time)

    def __getitem__(self, idx):
        return self.actions[idx]
