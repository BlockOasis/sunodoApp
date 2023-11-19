import json
import os
import requests

class MessageException(Exception):
    """Custom exception for handling messaging related errors."""
    pass

# The following classes represent various message types and responses.
# They are structured based on the expected JSON format for each message type.

class FinishResponse:
    def __init__(self, request_type, data):
        self.type = request_type
        self.data = data

class InspectResponse:
    def __init__(self, payload):
        self.payload = payload

class AdvanceResponse:
    def __init__(self, metadata, payload):
        self.metadata = metadata
        self.payload = payload

class Metadata:
    def __init__(self, msg_sender, epoch_index, input_index, block_number, timestamp):
        self.msg_sender = msg_sender
        self.epoch_index = epoch_index
        self.input_index = input_index
        self.block_number = block_number
        self.timestamp = timestamp

class Finish:
    def __init__(self, status):
        self.status = status

class Report:
    def __init__(self, payload):
        self.payload = payload

class Notice:
    def __init__(self, payload):
        self.payload = payload

class Voucher:
    def __init__(self, destination, payload):
        self.destination = destination
        self.payload = payload

class Exception:
    def __init__(self, payload):
        self.payload = payload

class IndexResponse:
    def __init__(self, index):
        self.index = index
        
class CartesiException:
    def __init__(self, payload):
        self.payload = payload

# Retrieve the rollup server URL from environment variables.
rollup_server = os.getenv("ROLLUP_HTTP_SERVER_URL")
if not rollup_server:
    raise MessageException("ROLLUP_HTTP_SERVER_URL environment variable is not set.")

def send_post(endpoint: str, json_data: dict) -> requests.Response:
    """Send a POST request to the specified endpoint with JSON data.

    Args:
        endpoint (str): The endpoint to send the POST request to.
        json_data (dict): The JSON data to send in the request.

    Returns:
        requests.Response: The response from the server.

    Raises:
        MessageException: If the HTTP request fails or if there is a JSON encoding error.
    """
    try:
        url = f"{rollup_server}/{endpoint}"
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        response = requests.post(url, data=json.dumps(json_data), headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as req_err:
        raise MessageException(f"HTTP request to {url} failed: {req_err}")
    except json.JSONDecodeError as json_err:
        raise MessageException(f"JSON encoding error: {json_err}")
    except BaseException as gen_err:
        raise MessageException(f"Unexpected error occurred: {gen_err}")

# The following functions send different types of messages to the server.
# They utilize the send_post function and handle any exceptions that it raises.

def send_finish(finish):
    """Send a finish message to the server.

    Args:
        finish (Finish): The finish message to send.

    Returns:
        requests.Response or None: The server's response, or None if an error occurred.
    """
    try:
        return send_post("finish", finish.__dict__)
    except MessageException as e:
        print(f"Error sending finish: {e}")
        return None

def send_report(report):
    """Send a report message to the server.

    Args:
        report (Report): The report message to send.

    Returns:
        requests.Response or None: The server's response, or None if an error occurred.
    """
    try:
        return send_post("report", report.__dict__)
    except MessageException as e:
        print(f"Error sending report: {e}")
        return None

def send_notice(notice):
    """Send a notice message to the server.

    Args:
        notice (Notice): The notice message to send.

    Returns:
        requests.Response or None: The server's response, or None if an error occurred.
    """
    try:
        return send_post("notice", notice.__dict__)
    except MessageException as e:
        print(f"Error sending notice: {e}")
        return None

def send_voucher(voucher):
    """Send a voucher message to the server.

    Args:
        voucher (Voucher): The voucher message to send.

    Returns:
        requests.Response or None: The server's response, or None if an error occurred.
    """
    try:
        return send_post("voucher", voucher.__dict__)
    except MessageException as e:
        print(f"Error sending voucher: {e}")
        return None

def send_exception(exception):
    """Send an exception message to the server.

    Args:
        exception (CartesiException): The exception message to send.

    Returns:
        requests.Response or None: The server's response, or None if an error occurred.
    """
    try:
        return send_post("exception", exception.__dict__)
    except MessageException as e:
        print(f"Error sending Cartesi exception: {e}")
        return None
