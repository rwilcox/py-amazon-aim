"""
A sample script to show you how to use the PyAmazonAIM module
By Ryan Wilcox <rwilcox@wilcoxd.com>
"""

import os
import sys

START_REPORT = 0
REPORT_STATUS = 1
DOWNLOAD_REPORT = 2

try:
    from pyamazonaim.aim import *
except ImportError:
    # might be trying it from a dev version....
    aimpath = os.path.abspath(  os.path.join( os.path.dirname(__file__), "..", "src" )  )
    print aimpath
    sys.path.insert(0, aimpath)
    from pyamazonaim.aim import *
    


def get_username_password():
    """Gets the username and password from (somewhere that can't be checked into VCS)"""
    username = os.environ["AMAZON_USERNAME"]
    password = os.environ["AMAZON_PASSWORD"]
    return username, password

def callAmazon(operation=None, id=None):
    """Performs operations on the Amazon API"""
    uname, passw = get_username_password()
    connection = AmazonAIM(uname, passw)
    output = None
    
    if operation == START_REPORT:
        output = connection.generate_open_listings_lite_report()
    if operation == REPORT_STATUS:
        output = connection.status_open_listings_report()
    if operation == DOWNLOAD_REPORT:
        output = connection.download_open_listings_report(id)
    return output

#print sys.argv

paramStr = sys.argv[1] if len(sys.argv) > 1 else ""
operation = 0
id = None
if paramStr == "status":
    operation = REPORT_STATUS
if paramStr == "download":
    operation == DOWNLOAD_REPORT
    id = sys.argv[2]

callAmazon(operation, id)
