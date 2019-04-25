"""Used for creating number sequences for display"""

import pygame

class Number(pygame.sprite.Sprite):
    """A single number"""

    def __init__(self, val, width):
        super().__init__()
        self.val = int(val)
        self.image = pygame.Surface((width, val))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()

    # def set_val(self, val):
    #     self.val = int(val)
    #     self.image = pygame.Surface((R_WID, int(val)))
    #     self.image.fill((255,255,255))

    def set_color(self, color):
        self.image.fill(color)


class NumGroup(pygame.sprite.AbstractGroup):
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
            n.rect.bottomleft = (self.bottomleft[0] + i*self.sprite_w, self.bottomleft[1])

    def swap(self, n1, n2):
        temp = self.nlist[n1]
        self.nlist[n1] = self.nlist[n2]
        self.nlist[n2] = temp

    def __iter__(self):
        return iter(self.nlist)

    def __getitem__(self, idx):
        return self.nlist[idx]
