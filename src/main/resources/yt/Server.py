#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


from youtrack.connection import Connection as YouTrack
import org.slf4j.Logger as Logger
import org.slf4j.LoggerFactory as LoggerFactory

class YtClient(object):

    def __init__(self, server, username, password):
        self.logger = LoggerFactory.getLogger("com.xebialabs.yourtrack.Server")
        if server is None:
            sys.exit("No server provided.")
        if username is not None:
            youtrackUsername = username
        else:
            youtrackUsername = server['username']
        if password is not None:
            youtrackPassword = password
        else:
            youtrackPassword = server['password']

        if server['token'] is not None:
            # authentication request with permanent token
            self.youtrack = YouTrack(server['url'], token=server['token'])
        else:
            # authentication with username and password
            self.youtrack = YouTrack(server['url'], login=youtrackUsername, password=youtrackPassword)

    def getIssue(self, issueId):
        return self.youtrack.getIssue(issueId)

    def getAllIssues(self, query, withFields):
        self.logger.debug("getAllIssues")
        self.logger.debug("Query = %s" % query)
        self.logger.debug("Fields = %s" % withFields)
        return self.youtrack.getAllIssues(filter=query, withFields=withFields)

    def updateIssuesByQuery(self, query, fieldsToUpdate, comment):
        command = ""
        for key in fieldsToUpdate:
            command += key + " " + fieldsToUpdate[key]
        foundIssues = self.youtrack.getAllIssues(filter=query, withFields=[])
        for issue in foundIssues:
            self.youtrack.executeCommand(issue['id'], command, comment)

    def getIssuesByQuery(self, query, fieldList=[]):
        self.logger.debug("getIssuesByQuery")
        return self.youtrack.getAllIssues(filter=query, withFields=[])
