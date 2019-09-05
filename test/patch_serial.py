
ENCODING = 'ascii'

buffer_out = []


def patch_serial(mock_serial):

    values = {'gain': 20, 'upp': 2, 'low': 1, 'pkt': 300, 'volt': 800,
              'sat': 1}

    def write(data):
        global buffer_out
        cmd = data.decode(ENCODING)
        cmd = cmd.lower().strip()

        if '?'in cmd:
            # Take the last word
            k = cmd.strip('?').split(':')[-1]
            if k[-1].isdigit():
                k = k[:-1]
            msg = '\x06{}\n'.format(values[k])
            buffer_out.append(msg)
        else:
            cmd, value = cmd.split()
            k = cmd.split(':')[-1]
            if k[-1].isdigit():
                k = k[:-1]
            values[k] = value
            buffer_out.append('\x06')

        return len(data)

    def readline():
        global buffer_out
        try:
            result = buffer_out.pop(0)
        except IndexError:
            result = ''
        return result.encode(ENCODING)

    def read(nbytes=1):
        global buffer_out
        try:
            result = buffer_out.pop(0)
            s = result[0:nbytes]
            b = result[nbytes:]
            if b != '':
                buffer_out.insert(0, b)
            result = s
        except IndexError:
            result = ''
        return result.encode(ENCODING)

    mock_serial.return_value.write = write
    mock_serial.return_value.readline = readline
    mock_serial.return_value.read = read