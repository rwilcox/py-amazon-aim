"""Holds common code used in all the samples in this folder"""\

import os

def get_username_password():
    """Gets the username and password from (somewhere that can't be checked into VCS)"""
    username = os.environ["AMAZON_USERNAME"]
    password = os.environ["AMAZON_PASSWORD"]
    return username, password
