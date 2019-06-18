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

if query is None:
    sys.exit("No query provided.")

if pollInterval is None:
    sys.exit("No polling interval provided.")

yt = YtClient(server, username, password)

data = None
status = None

allIssuesStatusMet = False
while not allIssuesStatusMet:
    try:
        foundIssues = youtrack.getAllIssues(query, withFields=[statusField])

        print "Found [%s] issues for query [%s] in YouTrack.\n" % (len(foundIssues), query)

        issuesWithDifferentStatus = list(filter(lambda (d): d[statusField] != checkForStatus,foundIssues))

        print "Found [%s] issues with status other than [%s] in YouTrack.\n" % (len(issuesWithDifferentStatus), checkForStatus)

        if len(issuesWithDifferentStatus) == 0:
            print "All issues found have the desired state [%s]: %s" % (checkForStatus, str(foundIssues))
            allIssuesStatusMet = True

        time.sleep(pollInterval)
    except Exception, e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        sys.exit("Error finding status for %s, error: %s" % (statusField, str(e)))
