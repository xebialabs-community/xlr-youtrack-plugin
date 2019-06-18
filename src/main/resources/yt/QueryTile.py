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
logger.error("START")
if not server:
    logger.error("YouTrack server ID must be provided")
    raise Exception("YouTrack server ID must be provided")

yt = YtClient(server, username, password)

data = None
status = None

def get_row_data(item):
    row_map = {}
    for column in detailsViewColumns:
        try:
            logger.error("for column = %s" % column)
            logger.error("row_map[%s] = %s" % (column, item[column]))
            row_map[column] = item[column]
        except:
            logger.error("column %s is bad" % column)
    row_map['link'] = "%s/issue/%s" % (server['url'], item['id'])
    return row_map


logger.error("getIssuesByQuery - %s" % (query))
results = yt.getIssuesByQuery(query)
logger.error("results = %s" % results)
logger.error("results type = %s" % type(results))
logger.error("results length = %s" % len(results))
rows= []
logger.error("START LOOP")
number = 0
for item in results:
    logger.error("record = %s" % item)
    row = item['id']
    rec = {}
    for key in item:
        rec[key] = item[key]
    logger.error("BEFORE get_row_data: %s = %s" % ( row, rec))
    #rows[row] = get_row_data(rec)
    rows.append( get_row_data(rec) )
    logger.error("AFTER get_row_data: %s = %s" % ( row, rows))
logger.error("END LOOP")
data = rows
