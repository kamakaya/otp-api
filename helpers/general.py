import json, logging, os, time
import pyotp

from logging import getLogger

logger = getLogger(__name__)

def get_one_time_password(deloitte_code: str) -> str:
    try:
        totp  = pyotp.TOTP(deloitte_code).now()
        return totp
    except:
        return None