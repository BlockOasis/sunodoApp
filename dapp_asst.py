import json
import logging
import os
import re
import model.model  # Assuming model.py is the Python equivalent of dapp/model
import processor.processor  # Assuming processor.py is the Python equivalent of dapp/processor

# Set up logging
info_log = logging.getLogger('info')
error_log = logging.getLogger('error')
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Global variables
claim_timeout = 30  # Example value, adjust as needed
dispute_timeout = 30  # Example value, adjust as needed
users = {}
claims = {}

# Function definitions
def get_user(address):
    user = users.get(address)
    if user is None:
        new_user = model.User(open_claims={}, open_disputes={})
        users[address] = new_user
        user = users[address]
    return user

def get_claim_list(payload_map):
    info_log.info("Got claim list request")
    claim_list = []
    for k in claims:
        simplified_claim = model.SimplifiedClaim(
            id=k, 
            status=claims[k].status, 
            value=claims[k].value
        )
        claim_list.append(simplified_claim)

    claim_list_json = json.dumps(claim_list)
    # The rest of the function would involve sending this data as a report
    # Depends on the Python equivalent of rollups.SendReport
    return None

def show_user(payload_map):
    info_log.info("Got show user request")
    user_address = payload_map.get("id")

    if not user_address:
        message = "ShowUser: Not enough parameters, you must provide string 'id'"
        report = Report(payload=message)
        try:
            send_report(report)
        except MessageException as e:
            error_log.error(f"ShowUser: error making http request: {e}")
            raise MessageException(message) from e
        raise MessageException(message)

    user_address = user_address.lower()
    info_log.info(f"For user {user_address}")

    if user_address not in users:
        message = "ShowUser: User doesn't exist"
        report = Report(payload=message)
        try:
            send_report(report)
        except MessageException as e:
            error_log.error(f"ShowUser: error making http request: {e}")
            raise MessageException(message) from e
        raise MessageException(message)

    user = users[user_address]

    try:
        user_json = json.dumps(user.__dict__)  # Assuming User class has __dict__ for serialization
        report = Report(payload=user_json)
        response = send_report(report)
        info_log.info(f"Received report status {response.status_code}")
    except json.JSONDecodeError as e:
        error_log.error(f"Error in JSON serialization: {e}")
        raise
    except MessageException as e:
        error_log.error(f"ShowUser: error making http request: {e}")
        raise


# Continue translating other functions like ShowClaim, GetWasm, etc.

if __name__ == "__main__":
    # Translate the main function logic
    pass
