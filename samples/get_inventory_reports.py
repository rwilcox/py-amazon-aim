"""
A sample script to show you how to use the PyAmazonAIM module
By Ryan Wilcox <rwilcox@wilcoxd.com>
"""

import os
import sys
import samples_common_utils as utils

START_REPORT = 0
REPORT_STATUS = 1
DOWNLOAD_REPORT = 2
CURRENTLY_WORKING_REPORT = 3
DOWNLOAD_REPORT_FLAT = 4
MOST_RECENT_REPORT = 5

try:
    from pyamazonaim.aim import *
except ImportError:
    # might be trying it from a dev version....
    aimpath = os.path.abspath(  os.path.join( os.path.dirname(__file__), "..", "src" )  )
    print aimpath
    sys.path.insert(0, aimpath)
    from pyamazonaim.aim import *
    



def callAmazon(operation=None, report_id=None):
    """Performs operations on the Amazon API"""
    uname, passw = utils.get_username_password()
    connection = AmazonAIM(uname, passw)
    output = None
    
    if operation == START_REPORT:
        output = connection.generate_open_listings_lite_report()
    if operation == CURRENTLY_WORKING_REPORT:
        output = connection.there_is_a_report_processing()
    if operation == REPORT_STATUS:
        output = connection.status_open_listings_report()
    if operation == DOWNLOAD_REPORT:
        output = connection.download_open_listings_report(report_id)
    if operation == DOWNLOAD_REPORT_FLAT:
        output = connection.download_open_listings_report(report_id, flat=True)
    return output

def main(paramStr):
    operation = START_REPORT
    report_id = None
    if paramStr == "status":
        operation = REPORT_STATUS
    if paramStr == "current":
        operation = CURRENTLY_WORKING_REPORT
    if paramStr == "recent":
        operation = MOST_RECENT_REPORT
    if paramStr == "download":
        operation = DOWNLOAD_REPORT
        report_id = sys.argv[2]
    if paramStr == "download_flat":
        operation = DOWNLOAD_REPORT_FLAT
        report_id = sys.argv[2]
    if (paramStr == "help") or (paramStr == "--help"):
        print """
        To use the Amazon Inventory Management API to get inventory reports, you must call this script the following way
        $ python get_inventory_reports.py    # creates a new process Amazon Server side
        $ python get_inventory_reports.py status
           OR
        $ python get_inventory_reports.py current
        # gets the report id of the report you created in step 1. The report may take up to 30 minutes to finish,
        # so run this command, go off and do something else, then run it again, and repeat
        # until you see that no report is currently working.
        # anyway, export REPORT_ID=(the report ID from the output from this command)
        #
        # If you do NOT get a report id back then it's possible (for sellers with a low inventory count)
        # that Amazon was able to process the request IMMEDIATELY, and the report is done by the time we start looking for reports with no end date
        # in that case, use:
        $ python get_inventory_reports recent
        # which will return the report id for the MOST recent report
        
        
        $ python download $REPORT_ID   # which will give you the report amazon generated for you
           OR
        $ python download_flat $REPORT_ID  # which gives you the report sorted all out by ASIN#
        
        (the source code is an excellent place to figure out what actual Amazon A.I.M or (py-amazon-aim)
        web service calls these parameters translate too)
        """
        return
    
    output = callAmazon(operation, report_id)
    if operation == START_REPORT:
        print output
    if operation == CURRENTLY_WORKING_REPORT:
        is_one_running, rid = output
        if is_one_running:
            print "Report Id %s is currently running (save this ID so you can download the report later!!!!)" % (rid)
        else:
            print "No report currently working. Your report is probably finished!"
        
    if operation == MOST_RECENT_REPORT:
        # TODO
        pass
    
    if operation == REPORT_STATUS:
        for curr_report in output:
            if curr_report["reportendtime"]:
                print "Report ID: %s. started on: %s, finished processing on %s" % ( curr_report["reportid"], curr_report["reportstarttime"], curr_report["reportendtime"] )
            else:
                # it is blank AKA in process
                print "** CURRENTLY WORKING Report ID: %s. started on: %s" % ( curr_report["reportid"], curr_report["reportstarttime"] )
        
    if operation == DOWNLOAD_REPORT:
        # TODO: fill me in
        pass
    
    if operation == DOWNLOAD_REPORT_FLAT:
        for curr_asin, curr_value in output.iteritems():
            print "%s is currently priced at: %s" % ( curr_asin, curr_value["price"] )


if __name__ == '__main__':
    paramStr = sys.argv[1] if len(sys.argv) > 1 else ""
    main(paramStr)

