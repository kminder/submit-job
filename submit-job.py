#!/usr/bin/python

import datetime
import getpass
import json
import requests  # sudo easy_install requests
import os
from string import Template
import sys


def print_usage():
    print "Usage: %s {job-file}" % __file__
    sys.exit(1)


def expand_cluster_name( params ):
    if 'CLUSTER_NAME' in params:
        param_name='CLUSTER_NAME'
        cluster_name = params[param_name]
    elif 'CLUSTER' in params:
        param_name='CLUSTER'
        cluster_name = params[param_name]
    else:
        param_name='CLUSTER'
        cluster_name = '${USER}-${FILE}-${DATE}-${TIME}'
    template = Template( cluster_name )
    cluster_name = template.substitute( params )
    params[param_name] = cluster_name
    return cluster_name


def run_job(job_name, job_params):
    p = job_params.copy()
    u = p['URL']
    n = getpass.getuser()
    n = n.replace(".", "-")
    p['USER'] = n
    p['DATE'] = datetime.datetime.now().strftime('%y%m%d')
    p['TIME'] = datetime.datetime.now().strftime('%H%M')
    p['FILE'] = job_name
    c = expand_cluster_name( p )
    print "Cluster: %s, Profile: %s" % (c, job_name)
    print json.dumps(p, indent=4, sort_keys=True)
    print "Cluster: %s, Profile: %s" % (c, job_name)
    del p['URL']
    del p['USER']
    del p['DATE']
    del p['TIME']
    del p['FILE']
    if 'METHOD' in p:
        m = p['METHOD']
        del p['METHOD']
    else:
        m = 'GET'
    if m == 'POST':
        print "POST"
        r = requests.post(u, data=p)
    else:
        r = requests.get(u, params=p)
    print "Status: %s" % r.status_code
    print r.text


def load_params(file_name):
    stream = open(file_name).read()
    job_params = json.loads(stream)
    return job_params


if not len(sys.argv) == 2:
    print_usage()

file_name = sys.argv[1]
job_name = os.path.splitext(os.path.basename(file_name))[0]
job_params = load_params(file_name)
run_job(job_name, job_params)
