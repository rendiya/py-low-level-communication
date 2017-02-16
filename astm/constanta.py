# -*- coding: utf-8 -*-
#
# rendiya (c) 2017

#: ASTM specification base encoding.
ENCODING = 'latin-1'

#: Message start token.
STX = chr(2) #b'\x02'
#: Message end token.
ETX = chr(3) #b'\x03'
#: ASTM session termination token.
EOT = chr(4) #b'\x04'
#: ASTM session initialization token.
ENQ = chr(5) #b'\x05'
#: Command accepted token.
ACK = chr(6) #b'\x06'
#: Command rejected token.
NAK = chr(15) #b'\x15'
#: Message chunk end token.
ETB = chr(17) #b'\x17'
LF  = chr(13) #b'\x0A'
CR  = chr(10) #b'\x0D'
#: CR + LF shortcut.
CRLF = CR + LF

#: Message records delimiter.
RECORD_SEP    = b'\x0D' # \r #
#: Record fields delimiter.
FIELD_SEP     = b'\x7C' # |  #
#: Delimeter for repeated fields.
REPEAT_SEP    = b'\x5C' # \  #
#: Field components delimiter.
COMPONENT_SEP = b'\x5E' # ^  #
#: Date escape token.
ESCAPE_SEP    = b'\x26' # &  #
