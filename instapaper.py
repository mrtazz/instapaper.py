#!/usr/bin/env python
# encoding: utf-8
"""
    instapaper.com cli client
"""

import urllib
import urllib2
import re
import sys
import os
from optparse import OptionParser
from getpass import getpass

VERSION = "0.1.0"

class Instapaper:
    """ This class provides the structure for the connection object """

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.authurl = "https://www.instapaper.com/api/authenticate"
        self.addurl = "https://www.instapaper.com/api/add"

    def add_item(self, url, title=""):
        """ Method to add a new item to a instapaper account
            Returns 0 on success and -1 if something went wrong
        """
        parameters = {'username' : self.user,'password' : self.password,
                      'url' : url, 'title' : title}
        headerdata = urllib.urlencode(parameters)
        try:
            request = urllib2.Request(self.addurl, headerdata)
            response = urllib2.urlopen(request).read()
            if (int(response) == 201):
                return 0
            elif (int(response) == 403):
                return -2
            elif (int(response) == 500):
                return -3
            else:
                return -1
        except IOError:
            return -1

def main():
    """
        main method
    """
    return_values = {
                        -1: "Something went wrong.",
                        -2: "Wrong username/password.",
                        -3: "Service unavailable."
                    }

    # initialize parser
    usage = "usage: %prog [-u USER] [-p PASSWORD] [-t TITLE] url"
    parser = OptionParser(usage, version="%prog "+VERSION)
    parser.add_option("-u", "--user", action="store", dest="user",
                      metavar="USER", help="instapaper username")
    parser.add_option("-p", "--password", action="store", dest="password",
                      metavar="USER", help="instapaper password")
    parser.add_option("-t", "--title", action="store", dest="title",
                      metavar="TITLE", help="title of the link to add")

    (options, args) = parser.parse_args()

    if not options.title:
        title = ""
    else:
        title = options.title
    if not len(args) > 0:
        parser.error("What do you want to read later?")

    if not options.user:
        # auth regex
        login = re.compile("(.+?):(.+)")
        try:
            config = open(os.path.expanduser("~") + "/.instapaperrc")
            for line in config:
                matches = login.match(line)
                if matches:
                    user = matches.group(1).strip()
                    password = matches.group(2).strip()
        except IOError:
            parser.error("No login information present.")
            sys.exit(-1)
    else:
        user = options.user
        # make sure all parameters are present
        if not options.password:
            password = getpass()
        else:
            password = options.password

    inst = Instapaper(user, password)
    result = inst.add_item(args[0], title)
    print return_values.get(result)

if __name__ == "__main__":
    main()
