import logging
from tango import DevState, UserDefaultAttrProp, Attr, DevDouble, \
    DevBoolean, DevLong, AttrWriteType
from tango.server import Device, command
from tango.server import device_property
from .constant import Models
from .controller import CyberstarController


class CyberstarX(Device):

    port = device_property(dtype=str, doc='Serial port')
    model = device_property(dtype=str, doc='Cyberstar model e.g.: X1000')
    addr = device_property(dtype=int, doc='Unit address', default_value=0)
    cyber = None
    library_debug = device_property(dtype=bool, default_value=False)

    ATTR_DICT = {'peakingtime': 'peaking_time',
                 'gain': 'gain',
                 'scalow': 'sca_low',
                 'scahigh': 'sca_high',
                 'voltage': 'voltage',
                 'delay': 'delay',
                 'securityenabled': 'security_enabled',
                 'saturation': 'saturation'}

    def init_device(self):
        Device.init_device(self)
        self.info_stream('Connecting to Cyberstart model: {} '
                         'port: {} addr: {}'.format(self.model,
                                                    self.port,
                                                    self.addr))
        model = Models.from_str(self.model)
        if self.library_debug:
            logging.basicConfig(level=logging.DEBUG)
        try:
            self.cyber = CyberstarController(self.port, model, self.addr)
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status('Can not connect to HW: {}'.format(e))

        self.set_state(DevState.ON)
        self.set_status('Device ready')

        # Attribute configuration: Name, unit, type, R/W
        attrs_conf = [
            ['PeakingTime', 'ns', DevLong, AttrWriteType.READ_WRITE],
            ['Gain', '%', DevDouble, AttrWriteType.READ_WRITE],
            ['SCALow', 'V', DevDouble, AttrWriteType.READ_WRITE],
            ['SCAHigh', 'V', DevDouble, AttrWriteType.READ_WRITE],
        ]
        if model == Models.X1000:
            attrs_conf += [
                ['Voltage', 'V', DevDouble, AttrWriteType.READ_WRITE],
                ['Delay', 's', DevDouble, AttrWriteType.READ_WRITE],
                ['SecurityEnabled', '', DevBoolean, AttrWriteType.READ_WRITE]
            ]
        elif model == Models.X2000:
            attrs_conf += [
                ['Saturation', '', DevBoolean, AttrWriteType.READ]
            ]

        for i in range(1, self.cyber.channels+1):
            for attr_conf in attrs_conf:
                name, unit, dtype, r_w = attr_conf
                attr_name = 'Chn{}{}'.format(i, name)

                attr_prop = UserDefaultAttrProp()
                if unit != '':
                    attr_prop.set_display_unit(unit)
                    attr_prop.set_standard_unit(unit)
                    attr_prop.set_unit(unit)

                attr = Attr(attr_name, dtype, r_w)
                attr.set_default_properties(attr_prop)
                r_meth = self.read_attribute
                w_meth = None
                if r_w == AttrWriteType.READ_WRITE:
                    w_meth = self.write_attribute
                self.add_attribute(attr, r_meth, w_meth)

    def read_attribute(self, attr):
        attr_name = attr.get_name()
        chn = int(attr_name[3])
        cyber_attr = self.ATTR_DICT[attr_name[4:].lower()]
        value = self.cyber[chn].__getattribute__(cyber_attr)
        attr.set_value(value)

    def write_attribute(self, attr):
        value = []
        attr.get_write_value(value)
        value = value[0]
        attr_name = attr.get_name()
        chn = int(attr_name[3])
        cyber_attr = self.ATTR_DICT[attr_name[4:].lower()]
        setattr(self.cyber[chn], cyber_attr, value)

    @command
    def reset(self):
        self.cyber.reset()

    @command(dtype_in=[float], doc_in='SCA values [Low, High]')
    def setSCA(self, sca):
        self.cyber.set_sca(sca[0], sca[1])

    @command(dtype_in=float, doc_in='Gain value')
    def setGain(self, value):
        self.cyber.set_gain(value)

    @command(dtype_in=int, doc_in='Peaking time value')
    def setPeakingTime(self, value):
        self.cyber.set_peaking_time(value)


def main():
    CyberstarX.run_server()


if __name__ == "__main__":
    main()
