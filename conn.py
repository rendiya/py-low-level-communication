"""This module contains drivers for the following equipment from Pfeiffer
Vacuum:
* TPG 262 and TPG 261 Dual Gauge. Dual-Channel Measurement and Control
    Unit for Compact Gauges
"""

import time
import serial

class AstmConn(object):
    r"""Abstract class that implements the common driver for the TPG 261 and
    TPG 262 dual channel measurement and control unit. The driver implements
    the following 6 commands out the 39 in the specification:
    * PNR: Program number (firmware version)
    * PR[1,2]: Pressure measurement (measurement data) gauge [1, 2]
    * PRX: Pressure measurement (measurement data) gauge 1 and 2
    * TID: Transmitter identification (gauge identification)
    * UNI: Pressure unit
    * RST: RS232 test
    This class also contains the following class variables, for the specific
    characters that are used in the communication:
    :var ETX: End text (Ctrl-c), chr(3), \\x15
    :var CR: Carriage return, chr(13), \\r
    :var LF: Line feed, chr(10), \\n
    :var ENQ: Enquiry, chr(5), \\x05
    :var ACK: Acknowledge, chr(6), \\x06
    :var NAK: Negative acknowledge, chr(21), \\x15
    """

    ETX = chr(3)  # \x03
    CR = chr(13)
    LF = chr(10)
    ENQ = chr(5)  # \x05
    ACK = chr(6)  # \x06
    NAK = chr(21)  # \x15

    def __init__(self, port='/dev/ttyACM0', baudrate=9600,timeout=10):
        """Initialize internal variables and serial connection
        :param port: The COM port to open. See the documentation for
            `pyserial <http://pyserial.sourceforge.net/>`_ for an explanation
            of the possible value. The default value is '/dev/ttyUSB0'.
        :type port: str or int
        :param baudrate: 9600, 19200, 38400 where 9600 is the default
        :type baudrate: int
        """
        # The serial connection should be setup with the following parameters:
        # 1 start bit, 8 data bits, No parity bit, 1 stop bit, no hardware
        # handshake. These are all default for Serial and therefore not input
        # below
        #self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        self.serial = serial.Serial(port = port, baudrate=baudrate, 
        timeout=timeout, writeTimeout=timeout,stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
    def _cr_lf(self, string):
        """Pad carriage return and line feed to a string
        :param string: String to pad
        :type string: str
        :returns: the padded string
        :rtype: str
        """
        return string + self.CR + self.LF

    def _send_command(self, command):
        """Send a command and check if it is positively acknowledged
        :param command: The command to send
        :type command: str
        :raises IOError: if the negative acknowledged or a unknown response
            is returned
        """
        
        self.serial.write(self._cr_lf(command))
        response = self.serial.readline()
        if response == self._cr_lf(self.NAK):
            message = 'Serial communication returned negative acknowledge'
            return IOError(message)
        elif response != self._cr_lf(self.ACK):
            message = 'Serial communication returned unknown response:\n{}'\
                ''.format(repr(response))
            return IOError(message)

    def _get_data(self):
        """Get the data that is ready on the device
        :returns: the raw data
        :rtype:str
        """
        self.serial.write(self.ENQ)
        data = self.serial.readline()
        return data.rstrip(self.LF).rstrip(self.CR)
astm = AstmConn()
print astm._send_command(command='coba')