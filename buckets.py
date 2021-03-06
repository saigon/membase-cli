#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  listservers class

  This class implements methods that will list servers within a
  membase cluster

"""

import pprint
from membase_info import usage
import restclient

rest_cmds = {
    'bucket-list': '/pools/default/buckets',
    'bucket-flush': '/pools/default/buckets/',
    'bucket-delete': '/pools/default/buckets/',
    'bucket-create': '/pools/default/buckets/',
    }
methods = {
    'bucket-list': 'GET',
    'bucket-delete': 'DELETE',
    'bucket-create': 'POST',
    'bucket-flush': 'POST',
    'bucket-stats': 'GET',
    }


class Buckets:

    def __init__(self):
        """
      constructor
    """
        # defaults
        self.debug = False
        self.verbose = False
        self.rest_cmd = rest_cmds['bucket-list']
        self.method = 'GET'

    def runCmd(
        self,
        cmd,
        server,
        port,
        user,
        password,
        opts,
        ):

        # defaults

        bucketname = ''
        cachesize = ''
        standard_result = ''
        self.user = user
        self.password = password

        # set standard opts

        output= 'default'
        for (o, a) in opts:
            if o == '-b' or o == '--buckets':
                bucketname = a
            if o == '-d' or o == '--debug':
                self.debug = True
            if o in  ('-o', '--output'):
                output = a
            if o == '-s' or o == '--size':
                cachesize = a
            if o == '-v' or o == '--verbose':
                self.verbose = True

        self.rest_cmd = rest_cmds[cmd]

        # instantiate a rest client

        rest = restclient.RestClient(server,
                                     port,
                                     {'debug':self.debug})

        # get the parameters straight

        if cmd in ('bucket-delete', 'bucket-create', 'bucket-flush'):
            if len(bucketname):
                rest.setParam('name', bucketname)
            if len(cachesize):
                rest.setParam('cacheSize', cachesize)
            self.rest_cmd = self.rest_cmd + bucketname
            if cmd == 'bucket-flush':
                self.rest_cmd = self.rest_cmd + '/controller/doFlush'

        opts = {'error_msg':"Unable to obtain bucket list"}
        data = rest.restCmd(methods[cmd],
                                self.rest_cmd,
                                self.user,
                                self.password,
                                opts)

        if methods[cmd] == 'GET':
            if output == 'json':
                print data
            else:
                json = rest.getJson(data)
                if self.verbose:
                    print 'List of buckets within the server %s:%s' \
                        % (server, port)
                for bucket in json:
                    print '%s' % bucket['name']
        else:
            if output == 'json':
                print rest.jsonMessage(data)
            else:
                print data

    # debug
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(json)
