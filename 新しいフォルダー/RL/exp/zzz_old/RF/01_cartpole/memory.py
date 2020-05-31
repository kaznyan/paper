import random
from collections import namedtuple, deque

import numpy as np

Transition = namedtuple('Transition', ('state', 'next_state', 'action', 'reward', 'mask'))


class Memory(object):
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)
        self.capacity = capacity

    def push(self, state, next_state, action, reward, mask):
        ### dequeの機能にappendなのでオーバーしたら最初のほうから消えていく
        self.memory.append(Transition(state, next_state, action, reward, mask))

    def sample(self, batch_size):
        transitions = random.sample(self.memory, batch_size)

        state      = np.empty((batch_size, transitions[0].state.size))
        next_state = np.empty((batch_size, transitions[0].next_state.size))
        action     = np.empty((batch_size, transitions[0].action.size))
        reward     = np.empty((batch_size, 1))
        mask       = np.empty((batch_size, 1))
        for i, tr in enumerate(transitions):
            state[i]      = tr.state
            next_state[i] = tr.next_state
            action[i]     = tr.action
            reward[i][0]  = tr.reward
            mask[i][0]    = tr.mask

        batch = Transition(state, next_state, action, reward, mask)
        return batch

    def __len__(self):
        return len(self.memory)
