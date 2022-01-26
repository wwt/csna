#!/opt/soar/bin/python
# -*- coding: utf-8 -*-
#
#      Copyright (c) 2021 - 2022  World Wide Technology
#      All rights reserved.
#
#      author: Joel W. King @joelwking - World Wide Technology
#
#      references:
#          https://kc.mcafee.com/resources/sites/MCAFEE/content/live/CORP_KNOWLEDGEBASE/78000/KB78712/en_US/CEF_White_Paper_20100722.pdf
#
#      export PH_AUTH_TOKEN=2adnymvMJMredactedHOM+xBGUNs1wEk=
#      export PH_SERVER=54.237.22.123
#
import time
from datetime import datetime
from datetime import timedelta
import os
import sys
import yaml
import argparse
#
#  Download from https://raw.githubusercontent.com/joelwking/Phantom-Cyber/master/REST_ingest/PhantomIngest.py
#
import PhantomIngest as ingest

TIME_SPAN = 60

p = ingest.PhantomIngest(os.getenv('PH_SERVER'), os.getenv('PH_AUTH_TOKEN'))

def get_fileobj(filepath=None):
    """ Get a file object, handling exceptions and returning False if the file cannot be opened
    """
    try:
        fileobject = open(filepath, 'r')
    except (IOError, OSError, TypeError) as e:
        return False

    return fileobject

def add_event(document, custom=False):
    """ Add a container and artifact(s) based on the YAML definition file.
    """

    try:
        document['container']
    except KeyError:
        print("missing required field 'container'")
        return False

    container = {}

    for key in ('name', 'description', 'label'):
        container[key] = document['container'].get(key, 'NONE')

    try:
        container_id = p.add_container(**container)
        print(f'Added container: {container_id}')
    except AssertionError as e:
        print("Any HTTP return code other than OK %s" % e)
        return False
    except Exception as e:
        print("Typically the phantom host did not respond, a connection error %s" % e)
        return False
    
    _artifact = {}

    for artifact in document['container'].get('artifacts'):
        for key in ('name', 'source_data_identifier'):
            _artifact[key] = artifact.get(key, 'NONE')
        cef = artifact.get('cef', dict())
        if custom:
            cef = add_defaults_for_custom_fields(cef)
        meta_data = artifact.get('meta_data', dict())
        try:
            artifact_id = p.add_artifact(container_id, cef, meta_data, **_artifact)
            print(f' |---  artifact: {artifact_id}')
        except (AssertionError, Exception) as e:
            print(f'Failure adding artifact: {e}')
        
        _artifact = {}

    return

def add_defaults_for_custom_fields(cef):
    """ If the string 'default' is the value for StartTime or deviceCustomDate1, calculate values
    """

    if cef['startTime'] == 'default':
        cef['startTime'] = int((time.time() - (60 * TIME_SPAN)) * 1000)  # milliseconds since epoch 

    if cef['deviceCustomDate1'] == 'default':
        current_time = datetime.utcnow()
        default_start_time = (current_time - timedelta(minutes=TIME_SPAN)).strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = datetime.strptime(default_start_time, '%Y-%m-%dT%H:%M:%SZ')
        cef['deviceCustomDate1'] = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return cef

def main():

    parser = argparse.ArgumentParser(prog='gen_events', description='Create events in Splunk> SOAR')
    parser.add_argument('-c', '--custom', dest='custom', help='update custom fields if not set', action='store_true', required=False)
    parser.add_argument('-f', '--file', dest='document', help='a YAML formatted input file', default=None, required=True)
    args = parser.parse_args()

    stream = get_fileobj(args.document)
    if stream:
        documents = yaml.safe_load_all(stream)
    else:
        print(f'...nothing to do!')
        sys.exit(1)

    for document in documents:
        add_event(document, custom=args.custom)

    stream.close()

if __name__ == '__main__':
    main()

