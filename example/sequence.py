"""Used for creating number sequences for display"""

from pam import action, actor


class Number(actor.Actor):
    """A single number"""

    def __init__(self, width, val):
        super().__init__()
        self.val = int(val)
        self.color = (255, 255, 255)
        self.alpha = 255
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)

    def set_val(self, val):
        self.val = int(val)
        self.rect = (self.rect.left, self.rect.top, self.rect.width, val)
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)

    def set_color(self, color):
        self.color = color
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)

    def set_alpha(self, alpha):
        self.alpha = alpha


class NumGroup(actor.ActorGroup):
    """A container for all the numbers"""

    def __init__(self, nlist, screen_w, screen_h):
        super().__init__()
        self.bottomleft = (0, screen_h)
        self.length = len(nlist)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.sprite_w = screen_w // self.length
        self.nlist = [Number(n, self.sprite_w) for n in nlist]
        self.add(self.nlist)

    def update(self):
        for i, n in enumerate(self.nlist):
            n.rect.bottomleft = (self.bottomleft[0] + i*self.sprite_w,
                                 self.bottomleft[1])

    def swap(self, n1, n2):
        temp = self[n1]
        self[n1] = self[n2]
        self[n2] = temp

    def __iter__(self):
        return iter(self.nlist)

    def __getitem__(self, idx):
        return self.nlist[idx]

    def __setitem__(self, idx, val):
        self.nlist[idx] = val
