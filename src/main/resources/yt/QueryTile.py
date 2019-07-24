#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import com.xhaus.jyson.JysonCodec as json
import sys
import time
import traceback
from yt.Server import YtClient
import org.slf4j.Logger as Logger
import org.slf4j.LoggerFactory as LoggerFactory


logger = LoggerFactory.getLogger("com.xebialabs.QueryTile")
logger.debug("START")
if not server:
    logger.debug("YouTrack server ID must be provided")
    raise Exception("YouTrack server ID must be provided")

yt = YtClient(server, username, password)

data = None
status = None

def get_row_data(item):
    row_map = {}
    for column in detailsViewColumns:
        try:
            logger.debug("for column = %s" % column)
            logger.debug("row_map[%s] = %s" % (column, item[column]))
            row_map[column] = item[column]
        except:
            logger.debug("column %s is bad" % column)
    row_map['link'] = "%s/issue/%s" % (server['url'], item['id'])
    return row_map


logger.debug("getIssuesByQuery - %s" % (query))
results = yt.getIssuesByQuery(query)
logger.debug("results = %s" % results)
rows= []
logger.debug("START LOOP")
number = 0
for item in results:
    logger.debug("record = %s" % item)
    row = item['id']
    rec = {}
    for key in item:
        rec[key] = item[key]
    rows.append( get_row_data(rec) )
logger.debug("END LOOP")
data = rows
