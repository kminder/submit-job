#!/usr/bin/python

import datetime
import getpass
import json
import requests  # sudo easy_install requests
import os
import sys


def print_usage():
    print "Usage: %s {job-file}" % __file__
    sys.exit(1)


def run_job(job_name, job_params):
    p = job_params.copy()
    u = p['URL']
    n = getpass.getuser()
    n = n.replace(".", "-")
    t = datetime.datetime.now().strftime('%y%m%d-%H%M')
    c = "%s_%s" % (n, t)
    p['CLUSTER'] = c
    print "Cluster: %s, Profile: %s" % (c, job_name)
    print json.dumps(p, indent=4, sort_keys=True)
    print "Cluster: %s, Profile: %s" % (c, job_name)
    del p['URL']
    r = requests.get(u, params=p)
    print "Status: %s" % r.status_code


def load_params(file_name):
    stream = open(file_name).read()
    job_params = json.loads(stream)
    return job_params


if not len(sys.argv) == 2:
    print "len %d" % len(sys.argv)
    print_usage()

file_name = sys.argv[1]
job_name = os.path.splitext(os.path.basename(file_name))[0]
job_params = load_params(file_name)
run_job(job_name, job_params)
