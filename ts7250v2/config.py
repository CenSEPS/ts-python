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
