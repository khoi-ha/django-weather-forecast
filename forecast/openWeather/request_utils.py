import requests
import logging

ARGUMENT_SEPARATOR = "&"
RESPONSE_SUCCESS = 200

logger = logging.getLogger(__name__)

def send_get_request(endpoint: str, headers: dict, **vars):
    """Send a GET request to a REST API endpoint

    Args:
        endpoint (str): The API endpoint URL
        headers (dict): Headers to include in the request

    Returns:
        The response object from the requests library. Empty response if the request
        fails or is unsuccessful
    """
    args_list = []

    for k, v in vars.items():
        args_list.append(f"{k}={v}")
    
    full_query = ARGUMENT_SEPARATOR.join(args_list)
    target_url = f"{endpoint}?{full_query}"

    try:
        response = requests.get(target_url, headers=headers)
    except Exception as e:
        logger.debug("Error sending request. More details below:")
        logger.debug(e)
        return None

    if response.status_code != RESPONSE_SUCCESS:
        logger.debug("Request is sent but unsuccessful")
        logger.debug(f"Status code: {response.status_code}")
        logger.debug(f"Response message: {response.content}")
        return None

    return response
