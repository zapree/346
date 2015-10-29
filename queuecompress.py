#!/usr/bin/env python

"""
Receives messages via AWS SQS 'compressqueue' queue. Runs forever,
so you will have to use ^C to kill it.

NOTE: make sure you have a ~/.boto file containing
your AWS credentials.
"""

import boto.sqs
from boto.sqs.message import Message
import time

__author__ = 'Eugene'

conn = boto.sqs.connect_to_region("us-west-2")
q = boto.sqs.connection.SQSConnection.lookup('compressqueue')
if q is None:
    q = conn.create_queue('compressqueue', 30) # 30-second message visibility

for i in range(0,10):
    m = Message()
    m.set_body("Message %d" % i)
    q.write(m)
