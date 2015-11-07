# -*- coding: utf-8 -*-
from __future__ import absolute_import
from keras.utils.theano_utils import floatX
from keras.layers.recurrent import Recurrent


class StatefulRNN(Recurrent):

    def set_weights(self, weights):
        np = len(self.params)
        nw = len(weights)
        ns = len(self.state)
        if nw == np - ns:
            np = nw
        params = self.params[:np]
        weights = weights[:nw]
        assert len(params) == len(weights), 'Provided weight array does not match layer weights (' + \
            str(len(params)) + ' layer params vs. ' + str(len(weights)) + ' provided weights)'
        for p, w in zip(params, weights):
            if p.eval().shape != w.shape:
                raise Exception("Layer shape %s not compatible with weight shape %s." % (p.eval().shape, w.shape))
            p.set_value(floatX(w))

    def get_hidden_state(self):
        state = [h.get_value() for h in self.state]
        return state

    def set_hidden_state(self, state):
        if len(state) != len(self.state):
            raise Exception("Provided hidden state array does not match layer hidden states")
        for s, h in zip(self.state, state):
            if s.eval().shape != h.shape:
                raise Exception("Hidden state shape not compatible")
            s.set_value(floatX(h))

    def reset_hidden_state(self):
        for h in self.state:
            h.set_value(h.get_value()*0)
