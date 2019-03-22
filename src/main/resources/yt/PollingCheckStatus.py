#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import time
import traceback
from yt.Server import YtClient

if issueId is None:
    sys.exit("No issue id provided.")

if pollInterval is None:
    sys.exit("No polling interval provided.")

yt = YtClient(server, username, password)

data = None
status = None

statusMatchFound = False
while not statusMatchFound:
    try:
        data = yt.getIssue(issueId)

        status = data[statusField]

        print "Found [%s] in YouTrack with status: [%s], looking for [%s].\n" % (data['id'], status, checkForStatus)
        if status == checkForStatus:
            statusMatchFound = True
        time.sleep(pollInterval)
    except Exception, e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        sys.exit("Error finding status for %s, error: %s" % (statusField, str(e)))
