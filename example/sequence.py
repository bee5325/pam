"""Used for creating number sequences for display"""

from pam import action, actor


class Number(actor.Actor):
    """A single number"""

    def __init__(self, width, val):
        super().__init__()
        self.val = int(val)
        self.color = (255, 255, 255)
        self.alpha = 255
        self.rect = (0, 0, width, val)
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)

    def set_val(self, val):
        self.val = int(val)
        self.rect = (self.rect.left, self.rect.top, self.rect.width, val)
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)


class NumGroup(actor.ActorGroup):
    """A container for all the numbers"""

    def __init__(self, nlist, screen_w, screen_h):
        super().__init__()
        self.bottomleft = (0, screen_h)
        self.length = len(nlist)
        self.sprite_w = screen_w // self.length
        self.nlist = [Number(self.sprite_w, n) for n in nlist]
        self.add(self.nlist)
        for i, n in enumerate(self.nlist):
            n.position = (i*self.sprite_w, screen_h-n.val)

    def swap(self, n1, n2, duration=1):
        n1dest = (n2*self.sprite_w, self[n1].rect.top)
        n2dest = (n1*self.sprite_w, self[n2].rect.top)
        self[n1].act(action.ActMove, duration, n1dest)
        self[n2].act(action.ActMove, duration, n2dest)
        self[n1], self[n2] = self[n2], self[n1]

    def __iter__(self):
        return iter(self.nlist)

    def __getitem__(self, idx):
        return self.nlist[idx]

    def __setitem__(self, idx, val):
        self.nlist[idx] = val
