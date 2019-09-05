from .communication import CyberstarComm
from .channel import CyberstarX1000, CyberstarX2000
from .constant import Specs, Models


class CyberstarController:
    """
    Class controller of the Cyberstar Pulse Processing Unit.
    """

    def __init__(self, port, model, addr=0, wait_time=0.25):
        self.addr = addr
        self.model = model
        self.com = CyberstarComm(port, wait_time)
        self._channels = {}

        for i in range(1, self.channels+1):
            if self.model == Models.X1000:
                self._channels[i] = CyberstarX1000(self)
            elif self.model == Models.X2000:
                self._channels[i] = CyberstarX2000(self, i)

    def __getitem__(self, item):
        if item not in self._channels:
            raise ValueError('Bad channel value')
        return self._channels[item]

    def send_cmd(self, cmd):
        return self.com.send_cmd(cmd)

    @property
    def channels(self):
        return Specs.channels(self.model)

    def reset(self):
        cmd = '*RST{}'.format(self.addr)
        self.send_cmd(cmd)

    def set_sca(self, low, high):
        if 0 <= low < high <= Specs.max_sca(self.model):
            for channel in self._channels.values():
                channel.sca_low = low
                channel.sca_high = high
        else:
            raise ValueError('The SCA ROI must be between 0 and {}, and the '
                             'the high must be grader than low value')

    def set_peaking_time(self, value):
        for channel in self._channels.values():
            channel.peaking_time = value

    def set_gain(self, value):
        for channel in self._channels.values():
            channel.gain = value
