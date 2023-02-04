from helpers.general import get_one_time_password

from logging import getLogger
from flask import Flask
from requests import get
import os


app = Flask(__name__)
logger = getLogger(__name__)

@app.route('/', methods=['GET'])
def root():
    # load_environment_mode()
    logger.info('ping received')
    ip: str = get('https://api.ipify.org').text

    logger.debug(f'My public IP address is: {ip}')
    # emit_debug_info(request)
    return f'Hello! Your ip is {ip}', 200


@app.route('/get_otp', methods=['GET'])
def get_otp():
    #TODO: get deloitte code from secrets
    return get_one_time_password("lphsyrkkfvqtbxxp")


if __name__ == '__main__':
    if 'DEBUG' in os.environ:
        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 8080)), debug=True)
    else:
        logger.info('Starting Flask app')
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))