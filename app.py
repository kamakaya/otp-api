from helpers.general import get_one_time_password, validate_input_parameters
from helpers.gcp_tools.secret_manager import access_secret_version


from logging import getLogger
from flask import Flask, request
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
    input_parameters = request.args.to_dict()
    
    if not validate_input_parameters(['service'], list(input_parameters.keys())):
        return "Required input parameters not present", 500

    service = input_parameters["service"]

    try:
        service_code = access_secret_version(f"{service}_otp_code")
        logger.info(f"Successfully retrieved the otp code from GSM for the following service: {service}")
    except Exception as e:
        error_message = f"Unable to retrieve the otp service. Failed with the following error: {e}"
        logger.error(error_message)
        return error_message, 500

    try:
        otp = get_one_time_password(service_code)
        logger.info(otp)
        return otp, 200
    except Exception as e:
        error_message = f"Error retrieving the one-time password. Failed with the following error: {e}"
        logger.error(error_message)
        return error_message, 500    


if __name__ == '__main__':
    if 'DEBUG' in os.environ:
        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 8080)), debug=True)
    else:
        logger.info('Starting Flask app')
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))