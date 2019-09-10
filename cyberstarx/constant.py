from enum import IntEnum, unique

# TODO: change to use auto method when support python 3.6
@unique
class Models(IntEnum):
    X1000 = 1
    X2000 = 2
    @staticmethod
    def from_str(model):
        model = model.upper()
        str2model = {'X1000': Models.X1000, 'X2000': Models.X2000, }
        return str2model[model]


# Models specifications: high voltage, peaking_time, sca_max, channels,
class Specs:
    _specs = {
        Models.X1000: [[250, 1250], [300, 500, 1000, 3000], 10, 1],
        Models.X2000: [[None, None], [50, 100, 300, 1000], 4, 5],
    }

    @staticmethod
    def check_peaking_time(model, value):
        peaking_time = Specs._specs[model][1]
        if value not in peaking_time:
            raise ValueError('Allowed peaking time: '
                             '{}'.format(repr(peaking_time)))

    @staticmethod
    def check_sca(model, value):
        max_sca = Specs._specs[model][2]
        if value < 0 or value > max_sca:
            err_msg = 'Allowed SCA from 0 to {}'.format(max_sca)
            raise ValueError(err_msg)

    @staticmethod
    def check_voltage(model, value):
        low, high = Specs._specs[model][0]
        if low is None or high is None:
            return RuntimeError('Model does not have voltage range defined')
        if value < low or value > high:
            return ValueError('Allowed voltage from {} to '
                              '{}'.format(low, high))

    @staticmethod
    def channels(model):
        return Specs._specs[model][3]
