import pytest
import unittest.mock as mock
import cyberstarx
import serial

from patch_serial import patch_serial

@pytest.fixture
def cyber_mock():
    """Test the mockup"""
    with mock.patch('serial.Serial') as mock_serial:
        patch_serial(mock_serial)
        com = serial.Serial('/dev/tty0')
        yield com


@pytest.fixture
def cyber_com():
    """Test nhq communication"""
    with mock.patch('cyberstarx.communication.serial.Serial') as mock_serial:
        patch_serial(mock_serial)
        nhq = cyberstarx.CyberstarComm('/dev/tty0')
        yield nhq


@pytest.fixture()
def cyber_controller(request):
    """Test nhq controller"""
    with mock.patch('cyberstarx.communication.serial.Serial') as mock_serial:
        patch_serial(mock_serial)
        cyberstar = cyberstarx.CyberstarController('/dev/tty0', request.param)
        yield cyberstar
