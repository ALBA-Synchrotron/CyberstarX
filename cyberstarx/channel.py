import weakref
from .constant import Specs

__all__ = ['CyberstarX1000', 'CyberstarX2000']


class CyberstarBaseChannel:
    """
    Cyberstar base channel.
    """

    def __init__(self, parent, channel_id=''):
        self._id = channel_id
        self._parent = weakref.proxy(parent)

    @property
    def model(self):
        return self._parent.model

    @property
    def gain(self):
        cmd = ':INP{}:GAIN{}?'.format(self._parent.addr, self._id)
        value = self._parent.send_cmd(cmd)
        return float(value)

    @gain.setter
    def gain(self, value):
        if value < 0 or value > 100:
            raise ValueError('The gain value must be between 0 and 100')
        cmd = ':INP{}:GAIN{} {}'.format(self._parent.addr, self._id, value)
        self._parent.send_cmd(cmd)

    @property
    def peaking_time(self):
        cmd = ':SENS{}:PKT{}?'.format(self._parent.addr, self._id)
        value = self._parent.send_cmd(cmd)
        return float(value)

    @peaking_time.setter
    def peaking_time(self, value):
        Specs.check_peaking_time(self.model, value)
        cmd = ':SENS{}:PKT{} {}'.format(self._parent.addr, self._id, value)
        self._parent.send_cmd(cmd)

    @property
    def sca_high(self):
        cmd = ':SENS{}:SCA:UPP{}?'.format(self._parent.addr, self._id)
        value = self._parent.send_cmd(cmd)
        return float(value)

    @sca_high.setter
    def sca_high(self, value):
        Specs.check_sca(self.model, value)
        cmd = ':SENS{}:SCA:UPP{} {}'.format(self._parent.addr, self._id, value)
        self._parent.send_cmd(cmd)

    @property
    def sca_low(self):
        cmd = ':SENS{}:SCA:LOW{}?'.format(self._parent.addr, self._id)
        value = self._parent.send_cmd(cmd)
        return float(value)

    @sca_low.setter
    def sca_low(self, value):
        Specs.check_sca(self.model, value)
        cmd = ':SENS{}:SCA:LOW{} {}'.format(self._parent.addr, self._id, value)
        self._parent.send_cmd(cmd)


class CyberstarX1000(CyberstarBaseChannel):
    @property
    def voltage(self):
        cmd = ':SOUR{}:VOLT?'.format(self._parent.addr)
        value = self._parent.send_cmd(cmd)
        return float(value)

    @voltage.setter
    def voltage(self, value):
        Specs.check_voltage(self.model, value)
        cmd = ':SOUR{}:VOLT {}'.format(self._parent.addr, value)
        self._parent.send_cmd(cmd)

    @property
    def security_enabled(self):
        cmd = ':SYST{}:SEC?'.format(self._parent.addr)
        value = self._parent.send_cmd(cmd)
        if value == '0':
            value = False
        elif value == '1':
            value = True
        else:
            raise RuntimeError('Wrong answer from HW {}'.format(value))
        return value

    @security_enabled.setter
    def security_enabled(self, value):
        cmd = ':SYST{}:SEC {}'.format(self._parent.addr, ['OFF', 'ON'][value])
        self._parent.send_cmd(cmd)

    @property
    def delay(self):
        cmd = ':TRIG{}:ECO?'.format(self._parent.addr)
        value = self._parent.send_cmd(cmd)
        return float(value)

    @delay.setter
    def delay(self, value):
        if value < 2 and value > 300:
            raise ValueError('The value must be between 2 and 300')
        value *= 10
        cmd = ':TRIG{}ECO {}'.format(self._parent.addr, value)
        self._parent.send_cmd(cmd)


class CyberstarX2000(CyberstarBaseChannel):
    @property
    def saturation(self):
        cmd = ':SENS{}:SAT{}?'.format(self._parent.addr, self._id)
        value = self._parent.send_cmd(cmd)
        if value == '0':
            value = False
        elif value == '1':
            value = True
        else:
            raise RuntimeError('Wrong answer from HW {}'.format(value))
        return value
