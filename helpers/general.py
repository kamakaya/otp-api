import json, logging, os, time
import pyotp

from logging import getLogger

logger = getLogger(__name__)

def get_one_time_password(code: str) -> str:
    try:
        totp  = pyotp.TOTP(code).now()
        return totp
    except:
        return None

def validate_input_parameters(arguments: list, request_arguments: list) -> bool:
    
    for argument in arguments:
        argument_present = request_arguments.count(argument)
        if argument_present == 0:
            return False
            
    return True