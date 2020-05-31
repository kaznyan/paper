import torch
import torch.nn as nn
import torch.nn.functional as F

import sklearn
import sklearn.ensemble
from sklearn import datasets
from sklearn.model_selection import train_test_split

from config import gamma

import numpy as np

class RFR(object):
    def __init__(self, num_inputs, num_outputs):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        self.rf = sklearn.ensemble.RandomForestRegressor()
        self.rf.fit(np.random.rand(2, num_inputs + num_outputs), np.random.rand(2, 1))

    @classmethod
    def train_model(cls, online_net, target_net, optimizer, batch):
        ### 経験データの取り出し
        states = batch.state
        next_states = batch.next_state
        actions = batch.action
        rewards = batch.reward
        masks = batch.mask

        batch_size = states.shape[0]
        n_states   = states.shape[1]
        n_actions  = actions.shape[1]

        ### 状態sにおけるQ(s, a1), Q(s, a2), ... を推論により求める × バッチ数
        ### TODO: actionは1要素につき1変数
        input = np.empty((batch_size, n_states + n_actions))
        input[:, :n_states] = states
        input[:, n_states:] = actions
        pred = online_net.rf.predict(input) ### 1次元 batch_size要素

        ### 状態s'におけるQ(s', a1), Q(s', a2), ... を推論により求める × バッチ数
        next_pred = np.empty((batch_size, n_actions))
        input = np.empty((batch_size, n_states + n_actions))
        input[:, :n_states] = states
        for i in range(n_actions):
            input[:, n_states:] = 0
            input[:, n_states + i] = 1
            next_pred[:, i] = target_net.rf.predict(input)

        ### Q(st, at)を求める
        # pred = (pred * actions).sum(axis=1) ### もしかして使わない？

        ### δ = rt + γ max(Q(s(t+1), a')) - Q(st, at)
        target = rewards.reshape((-1)) + masks.reshape((-1)) * gamma * next_pred.max(axis=1)

        ### 学習
        input = np.empty((batch_size, n_states + n_actions))
        input[:, :n_states] = states
        input[:, n_states:] = actions
        online_net.rf.fit(input, target)
        return None
        # return loss

    def get_action(self, state):
        ### TODO ベタ書き
        n_actions = 2

        next_pred = np.empty((1, n_actions))
        input = np.empty((1, state.shape[1] + n_actions))
        input[0, :state.shape[1]] = state
        for i in range(n_actions):
            input[0, state.shape[1]:] = 0
            input[0, state.shape[1] + i] = 1
            next_pred[0, i] = self.rf.predict(input)
        next_pred = next_pred.reshape((-1))
        next_pred = next_pred.argmax()
        return next_pred

        # return action.numpy()[0]







#
