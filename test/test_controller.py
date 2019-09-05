import pytest
from cyberstarx import Models


@pytest.mark.parametrize('cyber_controller', [Models.X2000,
                                              Models.X1000],
                         indirect=True)
def test_controller(cyber_controller):
    if cyber_controller.model == Models.X1000:
        nr_channels = 1
    elif cyber_controller.model == Models.X2000:
        nr_channels = 5
    assert cyber_controller.channels == nr_channels
    channel = cyber_controller[1]
    with pytest.raises(ValueError):
        channel.peaking_time = 200
    channel.sca_high = 3.5
    assert channel.sca_high == 3.5
    with pytest.raises(ValueError):
        channel.sca_low = 3.6
    channel.sca_low = 2.2
    assert channel.sca_low == 2.2
    if cyber_controller.model == Models.X2000:
        assert channel.saturation is True
        channel.peaking_time = 50
        assert channel.peaking_time == 50

    if cyber_controller.model == Models.X1000:
        channel.voltage = 300
        assert channel.voltage == 300
        channel.peaking_time = 500
        assert channel.peaking_time == 500
