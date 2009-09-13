import os
import sys
import operator

import samples_common_utils as utils

try:
    from pyamazonaim.aim import *
except ImportError:
    # might be trying it from a dev version....
    aimpath = os.path.abspath(  os.path.join( os.path.dirname(__file__), "..", "src" )  )
    print aimpath
    sys.path.insert(0, aimpath)
    from pyamazonaim.aim import *


__author__ = "Ryan Wilcox <rwilcox@wilcoxd.com>"
__copyright__ = "2009, Wilcox Development Solutions"
__license__ = "GPL/BSD"
__url__ = "http://github.com/rwilcox/py-amazon-aim"
__version__ = "1.0"


"""This example is to show how to use the OOP oriented aim.Report API.

This API is in the middle of being written, so this sample will include more
foundational APIs as we write higher abstraction code.
"""


def main(paramStr):
    uname, passw = utils.get_username_password()
    connection = AmazonAIM(uname, passw)
    if paramStr == "":
        output = connection.generate_open_listings_lite_report()
        print "created report, now rerun this command with a 'reports' parameter"
    else:
        # check to see if we're still waiting for a report...
        # (note: this is inefficient for example purposes. WD-rpw 09-13-2009)
        is_one_running, rid = connection.there_is_a_report_processing()
        if is_one_running:
            print "A report is still running, the RID is %s" % rid
        else:
            print "all done with the report requested"
            # now get all the current reports
            # and sort them so that the oldest report is first
            reports = Report.get_all_reports(connection)
            for report in reports:
                print "%s: started: on %s, ended on %s" % ( report.report_id, report.start.ctime(), report.end.ctime() )
            
            reports.sort( key=operator.attrgetter("start") )
            # sort will sort ASCENDING. Which, with dates, means that the oldest is at the top
            # which is GREAT for our purposes!
            print "the oldest report was..."
            report = reports[0]
            print "%s: started: on %s, ended on %s" % ( report.report_id, report.start.ctime(), report.end.ctime() )
        


if __name__ == '__main__':
    paramStr = sys.argv[1] if len(sys.argv) > 1 else ""
    if paramStr == "help":
        print """"First, run this command with no parameters. Then run this command with a get parameters
        to get the reports"""
        exit
    else:
        main(paramStr)
