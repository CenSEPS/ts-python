"""Configuration variables for this package"""

SYSCON_BASE_ADDRESS = 0x80004000
"""long: base address for syscon config registers"""

DIO_OFFSET = 0x36
"""int: address offset from SYSCON_BASE_ADDRESS which points to the EVGPIO Registers"""

DIO_REGISTER_OFFSET = {
    'DATACORE0': 0x36,
    'MASKCORE0': 0x38,
    'DATACORE1': 0x3a,
    'MASKCORE1': 0x3c
}
"""dict: mapping of EVGPIO register names to their offset from DIO_BASE_ADDRESS"""

SERIAL_DEVICES = {
    "s0": {
        'file': '/dev/ttyS0',
        'proto': 'RS232',
        'header': 'DB9',
        'pins': (2, 3),
        'jumper': 'JP2 ON -> DB9 header, JP2 OFF -> microUSB',
    },
    'xuart0': {
        'file': '/dev/ttyxuart0',
        'proto': 'RS232',
        'header': 'COM2',
        'pins': (2, 3),
        'jumper': None,
    },
    'xuart1': {
        'file': '/dev/ttyxuart1',
        'proto': 'RS232',
        'header': 'COM3',
        'pins': (2, 3),
        'jumper': None,
    },
    'xuart2': {
        'file': '/dev/ttyxuart2',
        'proto': 'RS485',
        'header': 'COM2',
        'pins': (1, 6),
        'jumper': None,
    },
    'xuart3': {
        'file': '/dev/ttyxuart3',
        'proto': 'RS422',
        'header': 'COM2',
        'pins': (4, 9),
        'jumper': None,
    },
    'xuart4': {
        'file': '/dev/ttyxuart4',
        'proto': 'RS232',
        'header': 'DB9',
        'pins': (2, 3),
        'jumper': 'JP2 ON -> Not connected, JP2 OFF -> DB9',
    }
}
