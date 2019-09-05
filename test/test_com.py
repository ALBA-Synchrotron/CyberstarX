import pytest


def test_cyberstartx_mock(cyber_mock):
    cyber_mock.write(b':inp0:gain 12\n')
    assert cyber_mock.read(1) == b'\x06'
    cyber_mock.write(b':inp0:gain?\n')
    ans = cyber_mock.readline()
    assert ans == b'\x0612\n'


def test_cyberstartx_com(cyber_com):
    ans = cyber_com.send_cmd(':inp0:gain?')
    assert ans == '20'
    ans = cyber_com.send_cmd(':sens0:pkt 100')
    assert ans == ''
    ans = cyber_com.send_cmd(':sens0:pkt?')
    assert ans == '100'