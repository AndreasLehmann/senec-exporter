
import struct

# System states of the SENEC PV
SYSTEM_STATE_NAME = {
    0: "INITIAL STATE",
    1: "ERROR INVERTER COMMUNICATION",
    2: "ERROR ELECTRICY METER",
    3: "RIPPLE CONTROL RECEIVER",
    4: "INITIAL CHARGE",
    5: "MAINTENANCE CHARGE",
    6: "MAINTENANCE READY",
    7: "MAINTENANCE REQUIRED",
    8: "MAN. SAFETY CHARGE",
    9: "SAFETY CHARGE READY",
    10: "FULL CHARGE",
    11: "EQUALIZATION: CHARGE",
    12: "DESULFATATION: CHARGE",
    13: "BATTERY FULL",
    14: "CHARGE",
    15: "BATTERY EMPTY",
    16: "DISCHARGE",
    17: "PV + DISCHARGE",
    18: "GRID + DISCHARGE",
    19: "PASSIVE",
    20: "OFF",
    21: "OWN CONSUMPTION",
    22: "RESTART",
    23: "MAN. EQUALIZATION: CHARGE",
    24: "MAN. DESULFATATION: CHARGE",
    25: "SAFETY CHARGE",
    26: "BATTERY PROTECTION MODE",
    27: "EG ERROR",
    28: "EG CHARGE",
    29: "EG DISCHARGE",
    30: "EG PASSIVE",
    31: "EG PROHIBIT CHARGE",
    32: "EG PROHIBIT DISCHARGE",
    33: "EMERGANCY CHARGE",
    34: "SOFTWARE UPDATE",
    35: "NSP ERROR",
    36: "NSP ERROR: GRID",
    37: "NSP ERROR: HARDWRE",
    38: "NO SERVER CONNECTION",
    39: "BMS ERROR",
    40: "MAINTENANCE: FILTER",
    41: "SLEEPING MODE",
    42: "WAITING EXCESS",
    43: "CAPACITY TEST: CHARGE",
    44: "CAPACITY TEST: DISCHARGE",
    45: "MAN. DESULFATATION: WAIT",
    46: "MAN. DESULFATATION: READY",
    47: "MAN. DESULFATATION: ERROR",
    48: "EQUALIZATION: WAIT",
    49: "EMERGANCY CHARGE: ERROR",
    50: "MAN. EQUALIZATION: WAIT",
    51: "MAN. EQUALIZATION: ERROR",
    52: "MAN: EQUALIZATION: READY",
    53: "AUTO. DESULFATATION: WAIT",
    54: "ABSORPTION PHASE",
    55: "DC-SWITCH OFF",
    56: "PEAK-SHAVING: WAIT",
    57: "ERROR BATTERY INVERTER",
    58: "NPU-ERROR",
    59: "BMS OFFLINE",
    60: "MAINTENANCE CHARGE ERROR",
    61: "MAN. SAFETY CHARGE ERROR",
    62: "SAFETY CHARGE ERROR",
    63: "NO CONNECTION TO MASTER",
    64: "LITHIUM SAFE MODE ACTIVE",
    65: "LITHIUM SAFE MODE DONE",
    66: "BATTERY VOLTAGE ERROR",
    67: "BMS DC SWITCHED OFF",
    68: "GRID INITIALIZATION",
    69: "GRID STABILIZATION",
    70: "REMOTE SHUTDOWN",
    71: "OFFPEAK-CHARGE",
    72: "ERROR HALFBRIDGE",
    73: "BMS: ERROR OPERATING TEMPERATURE",
    74: "FACOTRY SETTINGS NOT FOUND",
    75: "BACKUP POWER MODE - ACTIVE",
    76: "BACKUP POWER MODE - BATTERY EMPTY",
    77: "BACKUP POWER MODE ERROR",
    78: "INITIALISING",
    79: "INSTALLATION MODE",
    80: "GRID OFFLINE",
    81: "BMS UPDATE NEEDED",
    82: "BMS CONFIGURATION NEEDED",
    83: "INSULATION TEST",
    84: "SELFTEST",
    85: "EXTERNAL CONTROL",
    86: "ERROR: TEMPERATURESENSOR",
    87: "GRID OPERATOR: CHARGE PROHIBITED",
    88: "GRID OPERATOR: DISCHARGE PROHIBITED",
    89: "SPARE CAPACITY",
    90: "SELFTEST ERROR",
    91: "EARTH FAULT"
}

def decode(senec_value):
    # This function will decode the SENEC specific
    # data format to float/int.

    # senec_value:	a value string in the format "<type>_<value>"
    # example:  fl_000456
    # result:   number
    splitValue = senec_value.split('_')

    if splitValue[0] == 'fl':
        #Hex >> Float
        result = struct.unpack('f', struct.pack(
            'I', int('0x'+splitValue[1], 0)))[0]
    elif splitValue[0] == 'u1':
        result = int(splitValue[1], 16)
    elif splitValue[0] == 'u3':
        result = int(splitValue[1], 16)
    else:
        raise ValueError( (splitValue[0]) + " is not implemented")
    return result
