``PyAmazonAIM_API`` -- 	A Python implementation of the Amazon Inventory Management (AIM) API
==============================================================================================

A Python implementation of the Amazon Inventory Management API, which is not very well documented with sample code nor with libraries to wrap the pain away.


Amazon Inventory Management API is for Pro sellers (those that pay $40/month to Amazon in exchange for a number of extra benefits).

**ESSENTIALLY**: You only need the Amazon Inventory Management API if you need to know the SKU of an item (which the regular API doesn't seem to tell you anymore! - WD-rpw 08-30-2009), need the ability to reprice a seller's items, download their current orders, and manage rebates.

If you don't have to do any of those things, you probably need the regular Amazon Web Services Python libraries (like 
PyAWS: http://pypi.python.org/pypi/pyaws/0.2.1)


Amazon documentation for the A.I.M API is provided in the following places:

	* Word Document describing API: http://forums.prospero.com/am-assocdevxml/messages?msg=7070.6
	* PDF Document describing API: http://www.amazonsellercommunity.com/forums/ann.jspa?annID=18
	* A.I.M API Web Based Forum: http://www.amazonsellercommunity.com/forums/forum.jspa?forumID=30&start=0
	* Another web based forum: http://developer.amazonwebservices.com/connect/forum.jspa?forumID=6&start=0


PyAmazonAIM_API also tries to provide documentation where Amazon itself doesn't provide (much) documentation.

Vhile it was initially created to fill a client need (get SKUs for all their inventory items), as spare time (or patches!) permit I'll add the other capabilities too.

License
*******

This module is dual licensed as GPL/BSD license.


For Other Languages
===================

For Ruby see:

	* jcapote's amazon-aim (http://github.com/jcapote/amazon-aim/). I wrote my own partially because I needed the library in Python, and partially because I had some errors (that I couldn't quickly resolve) when I tried it the first time.
	* Peddler (http://snl.github.com/peddler/) I haven't tried this package, but it looks good
