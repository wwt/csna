# Define your constants here
XSRF_HEADER_NAME = 'X-XSRF-TOKEN'                          # Key name of the authentication token
XSRF_COOKIE_NAME = 'XSRF-TOKEN'                                 # Name of key in the cookie
REQUEST_HEADERS = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}
BANNER = 'CSNA'                                            # Banner for debug output
TEST_CONNECTIVITY = '/test_connectivity'                   # Endpoint value indicating we are simply testing connectivity
TIME_SPAN = 60                                             # Default value used to calculate the end timestamp for returning flow records
DEFAULT_RECORD_LIMIT = 2000                                # Default number of flow records to return
SUCCESSFUL = (200, 201, 202, 203, 204, 205, 206)           # Client Request Successful
ACCEPTED = 201                                             # Flow Query is accepted
HTTPS = 'https://'                                         # Hypertext Transfer Protocol Secure (HTTPS)
COOKIE_EXPIRES = 20 - 1                                    # The cookie returned by Stealthwatch expires in 20 minutes
AUTHENTICATE = "/token/v2/authenticate"                    # login
LOGOUT = "/token"                                          # logout
GET_DOMAINS = '/sw-reporting/v1/tenants'                   # returns list of domains (Tenants) configured
WAIT_FOR_FLOW_RESULTS = 1                                  # Time in seconds to wait for results
GET_FLOW_STATUS = '/sw-reporting/v2/tenants/{}/flows/queries/{}'  # Get the status of the initiated flow query
GET_FLOW_RESULTS = GET_FLOW_STATUS + '/results'            # Returns the flow query results
INITIATE_FLOW_QUERY = '/sw-reporting/v2/tenants/{}/flows/queries'
FILTER_TEMPLATE = {
                    "startDateTime": "{0}",
                    "endDateTime": "{1}",
                    "recordLimit": "{2}",
                    "subject": {
                        "ipAddresses": {
                            "includes": ["{3}"],
                            "excludes": []
                        },
                        "hostGroups": {
                            "includes": [],
                            "excludes": []
                        },
                        "username": {
                            "includes": [],
                            "excludes": []
                        },
                        "macAddress": {
                            "includes": [],
                            "excludes": []
                        }
                    },
                    "peer": {
                        "ipAddresses": {
                            "includes": [],
                            "excludes": []
                        },
                        "hostGroups": {
                            "includes": [],
                            "excludes": []
                        },
                        "username": {
                            "includes": [],
                            "excludes": []
                        },
                        "macAddress": {
                            "includes": [],
                            "excludes": []
                        }
                    },
                    "flow": {
                        "tcpUdpPorts": {
                            "includes": [],
                            "excludes": []
                        },
                        "applications": {
                            "includes": [],
                            "excludes": []
                        },
                        "flowDirection": "BOTH",
                        "byteCount": [],
                        "packetCount": [],
                        "payload": {
                            "includes": [],
                            "excludes": []
                        },
                        "flowDataSource": [],
                        "protocol": [],
                        "includeInterfaceData": False
                    }
                }
