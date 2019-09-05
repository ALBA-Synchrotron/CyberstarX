import serial
import time
import logging


class CyberstarComm:
    CODING = 'ascii'

    def __init__(self, port, wait_time=0):
        log_name = '{}.CyberstarComm'.format(__name__)
        self.log = logging.getLogger(log_name)
        self._com = serial.Serial(port,
                                  baudrate=9600,
                                  parity=serial.PARITY_NONE,
                                  stopbits=1)
        self._com.timeout = 0
        self.wait_time = wait_time

    def _send(self, cmd):
        cmd += '\n'
        raw_cmd = cmd.encode(self.CODING)
        self._com.write(raw_cmd)
        self.log.debug('Sent raw: {}'.format(repr(raw_cmd)))

    def _read(self):
        ans = self._com.readline()
        self.log.debug('Read raw: {}'.format(ans))
        ans = ans.decode(self.CODING)
        ans = ans.strip()
        if '\x06' not in ans:
            raise RuntimeError('HW did not set acknowledged')
        ans = ans.replace('\x06', '')
        return ans

    def send_cmd(self, cmd):
        self._send(cmd)
        time.sleep(self.wait_time)
        return self._read()

