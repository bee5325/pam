import sys
sys.path.append(r"D:\Programming\Python\pam")

import random
import sequence
from pam import actor, scene

S_SIZE = S_WID, S_HGT = 600, 400
NUMB_COUNT = 200


def quick_sort(nlist, partitions, check_idx, swap_idx, pivot):

    start, end = partitions[0]

    # if nothing to check
    if end-start < 1:
        partitions.pop(0)
        # for the case when sorting is done
        if len(partitions) == 0:
            return None, None, -1
        next_start, next_end = partitions[0]
        return next_end, next_start, -1

    # randomly take 11 values, use the median one as pivot
    if pivot == -1:
        randoms = [random.randrange(start, end) for _ in range(11)]
        randoms.sort(key=lambda x: nlist[x].val)
        median = randoms[5]
        if pivot != start:
            nlist.swap(median, start)
        pivot = start

    # if all items checked for this partition
    if pivot == check_idx:
        nlist.swap(pivot, swap_idx)
        left = (start, swap_idx-1)
        right = (swap_idx+1, end)
        partitions.append(left)
        partitions.append(right)
        partitions.pop(0)
        # for the case when sorting is done
        if len(partitions) == 0:
            return None, None
        next_start, next_end = partitions[0]
        return next_end, next_start, -1

    # swap_index have to be inititalize the first time encountering smaller
    # value
    if nlist[check_idx].val < nlist[pivot].val and swap_idx == start:
        swap_idx = check_idx
    # swap larger value to the swap_index item (only if smaller value is
    # encountered before)
    elif nlist[check_idx].val >= nlist[pivot].val and swap_idx != start:
        nlist.swap(check_idx, swap_idx)
        swap_idx -= 1
    check_idx -= 1

    return check_idx, swap_idx, pivot


if __name__ == '__main__':

    nlist = [random.random()*S_HGT for _ in range(NUMB_COUNT)]
    num = sequence.NumGroup(nlist, S_WID, S_HGT)
    s = scene.Scene(S_WID, S_HGT)

    partitions = [(0, len(num)-1)]
    start, end = partitions[0]
    check_idx, swap_idx, pivot = end, start, -1

    while 1:

        # if not yet finish, highlight index, pivot etc
        if len(partitions) != 0:
            start, end = partitions[0]
            for i, n in enumerate(num):
                if i >= start and i <= end:
                    num[i].set_color((255, 255, 255))
                else:
                    num[i].set_color((50, 50, 50))  # inactive
            if start < len(num):
                num[start].set_color((0, 255, 0))
                num[check_idx].set_color((0, 0, 255))
            if swap_idx != start:
                num[swap_idx].set_color((255, 0, 0))
        else:
            for n in num:
                n.set_color((255, 255, 255))

        if check_idx is not None and swap_idx is not None:
            check_idx, swap_idx, pivot = quick_sort(num, partitions, check_idx,
                                                    swap_idx, pivot)

        s.update()
        s.draw()
