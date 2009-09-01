import os, urllib2, string, inspect, re, StringIO
import base64
from xml.etree import ElementTree

__author__ = "Ryan Wilcox <rwilcox@wilcoxd.com>"
__copyright__ = "2009, Wilcox Development Solutions"
__license__ = "BSD/GPL"
__url__ = ""
__version__ = "0.1.0"


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
        Returns a dictionary of reportstarttime, reportendtime and reportid. The time dictionary value are (for now)
        in the format '08-30-2009:17-42-25'."""
        
        flavor = "OpenListingsLite"
        if not(lite):
            flavor = "OpenListings"
        output = self._report_statuses(flavor)
        newOutput = {}
        e = ElementTree.fromstring(output)
        
        # TODO: make this so it can handle more than 1 report going on.
        for currChild in e.getchildren():
            for currMatch in self.xmlOutputRegex.finditer(currChild.text):
                newOutput[currMatch.group(1)] = currMatch.group(2)
        return newOutput
        #return output  # TODO: parsing here?
    
    
    def download_open_listings_report(self, id=None, lite=True):
        """download the open listings report specified by the id parameter passed in.
        Returns a list of {sku:..., quantity:..., price:..., asin:....} items
        """
        flavor = "OpenListingsLite"
        if not(lite):
            flavor = "OpenListings"
        url = "https://secure.amazon.com/exec/panama/seller-admin/download/report"
        output = self._connect(url, ReportId=id)
        
        # output is a tab return delimited file
        # the first line is the header line, and the next lines are the items
        # EXCEPT it also includes header information repeated every so often (as if it was returning this information on a paginated basis)
        io = StringIO.StringIO(output)
        arrayOfDictionaries = []
        for currline in io:
            fields = currline.split("\t")
            # TODO: can this be in arbitrary order, or will it ALWAYS be this way? WD-rpw 08-30-2009
            sellerSKU = fields[0]
            sellerQuantity = fields[1]
            sellerPrice = fields[2]
            itemASIN = fields[3]
            if sellerSKU != "seller-sku":
                # it must be an item line (right!?)
                arrayOfDictionaries.append( dict(sku=sellerSKU, quantity=sellerQuantity, price=sellerPrice, asin=itemASIN) )
            
        
        return arrayOfDictionaries
    
        
    
