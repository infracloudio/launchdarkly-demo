"""
Utility Functions
"""
import socket
import logging

def get_ld_non_human_user(request=None):
    """
    Representation of a non human "user" for use with LaunchDarkly
    ref https://docs.launchdarkly.com/sdk/features/user-config#python 
    """
    if request:
        request_ip = request.remote_addr
    else:
        request_ip = None
    user = {
        "key": socket.gethostname(),
        "ip": request_ip,
        "email": 'local@machine.com',
        "custom": {
            "type": "machine"
        }
    }
    logging.debug(user)
    return user

