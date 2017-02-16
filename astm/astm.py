# -*- coding: utf-8 -*-

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
    STX = chr(2)
    ETX = chr(3)  # \x03
    CR = chr(13)
    LF = chr(10)
    ENQ = chr(5)  # \x05
    ACK = chr(6)  # \x06
    NAK = chr(21)  # \x15
    EOT = chr(4)
    ETB = chr(17)

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
    def _astm_string(self, string):
        """Pad carriage return and line feed to a string
        :param string: String to pad
        :type string: str
        :returns: the padded string
        :rtype: str
        """
        return self.STX + string + self.ETB + self.CR + self.LF

    def send_command(self, command):
        """Send a command and check if it is positively acknowledged
        :param command: The command to send
        :type command: str
        :raises IOError: if the negative acknowledged or a unknown response
            is returned
        <STX>[FN][TEXT]<ETB>[C1][C2]<CR><LF>
        """

        self.serial.write(self._astm_string(string=command))
        response = self.serial.readline()
        print response
        if response == self._cr_lf(self.NAK):
            message = 'Serial communication returned negative acknowledge'
            return IOError(message)
        elif response != self._cr_lf(self.ACK):
            message = response.encode('hex')
            return IOError(message)
    def open_session(self):
        """Get the session communication in ASTM 
        :send: data ENQ
        :return: data ACK
        """
        self.serial.write(self.ENQ)
        i = 0
        for i in range(0,9):
            self.serial.write(self.ENQ)
            i = i + 1
            data = self.serial.read()
            print 'data hex: '+data.encode('hex')
            print 'data byte: '+data
        
            if data == self.ACK:
                return "open session with ACK response"
            elif data == self.NAK:
                return "receiver send NAK"
    def get_data(self):
        """Get the data that is ready on the device
        :returns: the raw data
        :rtype:str
        """
        self.serial.write(self.ACK)
        handshake = self.serial.readline()
        if handshake != self.NAK:
            data = self.serial.readline()
        else:
            self.serial.write(self.NAK)
            return "Not Acknowledge"
        return data.rstrip(self.LF).rstrip(self.CR)

astm = AstmConn(port='/dev/ttyACM0', baudrate=9600)
#print astm.send_command(command='coba')
print astm.open_session()
#print astm.status()