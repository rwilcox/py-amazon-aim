"""
A sample script to show you how to use the PyAmazonAIM module
By Ryan Wilcox <rwilcox@wilcoxd.com>
"""

import os
import sys

START_REPORT = 0
REPORT_STATUS = 1
DOWNLOAD_REPORT = 2
CURRENTLY_WORKING_REPORT = 3

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
    if operation == CURRENTLY_WORKING_REPORT:
        output = connection.there_is_a_report_processing()
    if operation == REPORT_STATUS:
        output = connection.status_open_listings_report()
    if operation == DOWNLOAD_REPORT:
        output = connection.download_open_listings_report(id)
    return output


paramStr = sys.argv[1] if len(sys.argv) > 1 else ""
operation = START_REPORT
id = None
if paramStr == "status":
    operation = REPORT_STATUS
if paramStr == "current":
    operation = CURRENTLY_WORKING_REPORT
if paramStr == "download":
    operation == DOWNLOAD_REPORT
    id = sys.argv[2]

output = callAmazon(operation, id)
if operation == START_REPORT:
    print output
if operation == CURRENTLY_WORKING_REPORT:
    is_one_running, rid = operation
    if is_one_running:
        print "Report Id %s is currently running (save this ID so you can download the report later!!!!)" % (rid)
    else:
        print "No report currently working. Your report is probably finished!"
    print "The currently working "
if operation == REPORT_STATUS:
    # TODO: fill me in
    pass
if operation == DOWNLOAD_REPORT:
    # TODO: fill me in
    pass
