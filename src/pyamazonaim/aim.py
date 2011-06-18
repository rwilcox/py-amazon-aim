import os, urllib2, string, inspect, re, StringIO, datetime
import base64
from xml.etree import ElementTree

__author__ = "Ryan Wilcox <rwilcox@wilcoxd.com>"
__copyright__ = "2009, Wilcox Development Solutions"
__license__ = "BSD/GPL"
__url__ = ""
__version__ = "0.1.0"


class Report(object):
    """
    Represents an inventory report requested from Amazon.
    Will eventually provide an OOP way to create reports and get statuses,
    as an alternative to the (more foundational and more frankly procedural) AmazonAIM object
    """
    
    def __init__(self, report_id = None, start=None, end=None):
        self.report_id = None
        self.start = start   # start time of the report
        self.end = end     # end time of the report
    
    def __repr__(self):
        return "aim.Report(report_id='%s', start=%s, end=%s) " % (self.report_id, self.start.__repr__(), self.end.__repr__())
    
    def __lt__(self, other):
        """Implement __lt__ to allow our object to be sorted"""
        return (self.start < other.start)
    
    @classmethod
    def get_all_reports(cls, connection, lite=True):
        """Return the user's current reports as Report objects"""
        raw_reports = connection.status_open_listings_report(lite)
        output = []
        for curr_raw in raw_reports:
            curr = Report()
            curr.set_attribute_from_html( "reportid", curr_raw["reportid"] )
            curr.set_attribute_from_html( "reportstarttime", curr_raw["reportstarttime"])
            curr.set_attribute_from_html( "reportendtime", curr_raw["reportendtime"] )
            output.append(curr)
        return output
    
    def _amazon_date_time_to_python_date_time(self, date_string):
        # example date string:
        #09-13-2009:10-11-31
        if date_string:
            date, time = date_string.split(":")
            month, day, year = date.split("-")
            hour, minute, second = time.split("-")
            return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        else:
            return None
    
    def set_attribute_from_html(self, attributeName, attributeValue):
        """meant to take raw input from Amazon's XML output and turn it into
        proper Python objects in this class"""
        if attributeName == "reportid":
            self.report_id = attributeValue
        if attributeName == "reportstarttime":
            self.start = self._amazon_date_time_to_python_date_time(attributeValue)
        if attributeName == "reportendtime":
            self.end = self._amazon_date_time_to_python_date_time(attributeValue)
        
    

class AmazonAIM(object):
    """
    Communicates with the Amazon API for Marketplace Sellers.
    See <http://forums.prospero.com/am-assocdevxml/messages?msg=7070.6> for what little documentation there is on this API.
    See also <http://www.amazonsellercommunity.com/forums/ann.jspa?annID=18> for additional documentation
    """
    
    xmlOutputRegex = re.compile(r'(.+?)=(.+?) ')
    def __init__(self, username, password):
        super(AmazonAIM, self).__init__()
        self.username = username
        self.password = password
    
    
    # _____________________________________________________________________________
    # PRIVATE METHODS HERE (Yes, order of methods reads kind of backwards...)
    # _____________________________________________________________________________
    def _connect( self, url, **extraParams ):
        req = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        req.add_header("Authorization", "Basic %s" % base64string)
        req.add_header("Content-Type", "text/xml")
        for key, value in extraParams.iteritems():
            req.add_header(key, value)
        handle = urllib2.urlopen(req)
        output = []
        for line in handle:
            #print line
            output.append(line)
        
        return "".join(output)
    
    
    def _report_statuses( self, report_name ):
        """report_statuses will get a list of all the current reports you have running on AIM"""
        
        url = "https://secure.amazon.com/exec/panama/seller-admin/manual-reports/get-report-status"
        output = self._connect(url, ReportName=report_name)
        return output
    
    
    # _____________________________________________________________________________
    # Methods that correspond almost exactly with Amazon Inventory Management APIs
    # _____________________________________________________________________________
    def generate_open_listings_lite_report(self):
        """open_listings_lite creates an open listings(lite) report on the server.
        You'll need to wait a while and ping the server with a status_open_listings_report(). Amazon's documentation says
        operations could take up from 30-45 minutes to complete"""
        
        url = "https://secure.amazon.com/exec/panama/seller-admin/manual-reports/generate-report-now"
        output = self._connect( url, ReportName="OpenListingsLite" )
        # because Amazon's XML output SUCKS we want to turn it into a dictionary here
        
        return output   # TODO: parsing here?
    
    
    def status_open_listings_report(self, lite=True):
        """get the status of any ongoing open listings report on the server.
        Returns a list of dictionaries of reportstarttime, reportendtime and reportid. The time dictionary value are (for now)
        in the format '08-30-2009:17-42-25'."""
        
        flavor = "OpenListingsLite"
        if not(lite):
            flavor = "OpenListings"
        output = self._report_statuses(flavor)
        new_output = []
        e = ElementTree.fromstring(output)
        
        for currChild in e.getchildren():
            this_item = {}
            for currMatch in self.xmlOutputRegex.finditer(currChild.text):
                this_item[currMatch.group(1)] = currMatch.group(2)
            new_output.append(this_item)
        return new_output
    
    
    def download_open_listings_report(self, report_id=None, lite=True, flat=False):
        """download the open listings report specified by the id parameter passed in.
        Additional parameters let you control the typo of report you requested (lite=True)(default) or not),
        And how you want your data outputted (as a list of dictionaries (flat=False)(default) or as
        just dictionaries where the keys are the ASIN numbers (which should be unique from product to product)(flat=True).
        
        Returns a list of {sku:..., quantity:..., price:..., asin:....} items if flat=False mode,
        a dictionary of {asin: {sku: ..., quantity: ..., price: ...} } if flat=True
        """
        flavor = "OpenListingsLite"
        if not(lite):
            flavor = "OpenListings"
        url = "https://secure.amazon.com/exec/panama/seller-admin/download/report"
        output = self._connect(url, ReportId=report_id)
        
        # output is a tab return delimited file
        # the first line is the header line, and the next lines are the items
        # EXCEPT it also includes header information repeated every so often (as if it was returning this information on a paginated basis)
        io = StringIO.StringIO(output)
        arrayOfDictionaries = []
        dictionaryOfItems = {}
        for currline in io:
            fields = currline.split("\t")
            # TODO: can this be in arbitrary order, or will it ALWAYS be this way? WD-rpw 08-30-2009
            sellerSKU = fields[0].strip()
            sellerQuantity = fields[1].strip()
            sellerPrice = fields[2].strip()
            itemASIN = fields[3].strip()
            if sellerSKU != "seller-sku":
                # it must be an item line (right!?)
                infoDict = dict(sku=sellerSKU, quantity=sellerQuantity, price=sellerPrice, asin=itemASIN)
                if flat:
                    dictionaryOfItems[itemASIN] = infoDict
                else:
                    arrayOfDictionaries.append(infoDict)
            
        if flat:
            return dictionaryOfItems
        else:
            return arrayOfDictionaries
    
    
    # _____________________________________________________________________________
    # Methods that provide an abstraction over the Amazon Inventory Management APIs
    # (abstraction or convenience, that is)
    # _____________________________________________________________________________
    def there_is_a_report_processing(self, lite=True):
        """a convenience method returns True, reportID if there's a report that we're waiting for Amazon to finish,
        False, None otherwise."""
        reports = self.status_open_listings_report(lite)
        
        # reports not finished yet will have a blank end time
        for curr_report in reports:
            if not(curr_report["reportendtime"]):  # blank == False in Python
                return [True, curr_report["reportid"]]
        
        return [False, None]
    
