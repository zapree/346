#!/usr/bin/env python

"""
Receives messages via AWS SQS 'compressqueue' queue. Runs forever,
so you will have to use ^C to kill it.

NOTE: make sure you have a ~/.boto file containing
your AWS credentials.
"""

import boto.sqs
import time

__author__ = 'Eugene'

conn = boto.sqs.connect_to_region("us-west-2")
q = conn.create_queue('compressqueue', 30) # 30-second message visibility
if q is None:
    print "could not create or connect to queue"


else:
    while True:
        m = q.read(wait_time_seconds = 3) # wait up to 3 seconds for message
        if m is None:
            print "NO MESSAGE"
        else:
            print m.get_body()
            time.sleep(1)
            q.delete_message(m)