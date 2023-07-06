import json
import os


def read_config():

    global shipping_mail, step_app

    #   Read JSON config file
    json_file_fullpath = os.path.join("./configs","config.json")
    with open(json_file_fullpath, "r") as f:
        config = json.load(f)

    ## Call config and excel's sheets detail & Excel's file directory
    shipping_mail = config['mail_cf']

    ## Call config of a MS Graph API
    Azure_app = config['Azure_App']

__all__ = ['read_config']

