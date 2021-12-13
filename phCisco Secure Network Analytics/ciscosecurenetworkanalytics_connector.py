#!/opt/phantom/usr/bin/python
# -*- coding: utf-8 -*-
#
#      Copyright (c) 2021 World Wide Technology
#      All rights reserved.
#
#      author: Joel W. King @joelwking - World Wide Technology 
#
# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Usage of the consts file is recommended
from ciscosecurenetworkanalytics_consts import *

# System related imports
import requests
import json
import time
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class CiscoSecureNetworkAnalyticsConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(CiscoSecureNetworkAnalyticsConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

        # Contains the requests session object
        self._api_session = None

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Empty response and no information in the header"
            ), None
        )

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, error_text)

        message = message.replace(u'{', '{{').replace(u'}', '}}')
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))
                ), None
            )

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace(u'{', '{{').replace(u'}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace('{', '{{').replace('}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _logout(self):
        """ Logout of the session with the Management Console

        Args:
            none
        """

        self._api_session = self._api_session.close()    # close the session and return None to the _api_session
        return

    def _login(self, config):
        """ Create a Requests Session with the Management Console, authenticate and
            store the Cookie for subsequent API calls.

        Args:
            config (dict): values from the app configuration description
        """
        self.api_session = requests.Session()
        url = self._base_url + "/token/v2/authenticate"
        login_request_data = {
            "username": config['smc_username'],
            "password": config['smc_password']
             }
        try:
            r = self.api_session.request("POST", url, verify=config.get('verify_server_cert', False), data=login_request_data)
        except requests.exceptions.ConnectionError as e:
            return 504  # Gateway Time-Out - likely the Management Console is unreachable 

        if r.status_code == r.OK:
            for cookie in r.cookies:
                if cookie.name == XSRF_HEADER_NAME:
                    self.api_session.headers.update({XSRF_HEADER_NAME: cookie.value})
                    break
        return r.status_code

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()    # config has your credentials and the hostname of the Management Console

        resp_json = None
        
        url = self._base_url + endpoint

        if not self._api_session:
            ret_val = self._login(config)
            if ret_val != 200:
                return RetVal(
                    action_result.set_status(
                        phantom.APP_ERROR, "Unable to connect to Management Controller: {0} {1}".format(ret_val, url)
                    ), resp_json
                )
        if endpoint == TEST_CONNECTIVITY:
            return self._process_response(ret_val, action_result)

        # TODO  Do the REST CALL HERE

        return self._process_response(ret_val, action_result)

    def _handle_test_connectivity(self, param):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        self.save_progress("Connecting to Management Console")
        # make rest call
        ret_val, response = self._make_rest_call(TEST_CONNECTIVITY, action_result, params=None, headers=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_retrieve_flows(self, param):
        """
        Retrieve flows from Management Console

        Args:
            param ([type]): [description]
        """
        action_result = self.add_action_result(ActionResult(dict(param)))
        return action_result.set_status(phantom.APP_ERROR, "Action not yet implemented")

    def _calculate_timestamp(self, param):
        """
        Calculate the timestamp based on the user input from the GUI.
        If the start_time is not specified, use the current Zulu time minus time_span.
        If the time_span is not specified, use 60 minutes.
        
        Returns a tuple of the start and end time in ISO8601 format
        """
        
        time_span = param.get('time_span', TIME_SPAN)

        current_time = datetime.utcnow()
        default_start_time = (current_time - timedelta(minutes=time_span)).strftime('%Y-%m-%dT%H:%M:%SZ')
        start_time = param.get('start_time', default_start_time)

        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
        except (ValueError, TypeError) as e:
            self.save_progress("Invalid time format: {} using default".format(e))
            start_time = default_start_time
        #
        #  Now we have determined the start time, calculate the end time
        #
        end_time = (start_time + timedelta(minutes=time_span))
        
        #  Convert to ISO8601 format and return
        return (start_time.strftime('%Y-%m-%dT%H:%M:%SZ'), 
                end_time.strftime('%Y-%m-%dT%H:%M:%SZ'))

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test connectivity':
            ret_val = self._handle_test_connectivity(param)
        if action_id == 'retrieve flows':
            ret_val = self._handle_retrieve_flows(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """
        self.debug_print("{} INITIALIZE {}".format(BANNER, time.asctime()))

        self._base_url = "https://" + config['smc_host']

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        # If there was no state available, the variable will be None, save_state requires a dictionary, not NoneType!
        if self._state:
            self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import argparse

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)
    argparser.add_argument('-d', '--debug', help='used when executing in debug mode with VSCode', type=bool, default=False, required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = CiscoSecureNetworkAnalyticsConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page {}".format(login_url))
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            # When running under the VSCODE debugger we need to set the session_id to None, and not fail
            if args.debug:
                session_id = None
            else:
                exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = CiscoSecureNetworkAnalyticsConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == '__main__':
    main()
