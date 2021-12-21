# Define your constants here
XSRF_HEADER_NAME = 'X-XSRF-TOKEN'                          # Key name of the authentication token
BANNER = 'CSNA'                                            # Banner for debug output
TEST_CONNECTIVITY = '/test_connectivity'                   # Endpoint value indicating we are simply testing connectivity
TIME_SPAN = 60                                             # Default value used to calculate the end timestamp for returning flow records
SUCCESSFUL = (200, 201, 202, 203, 204, 205, 206)           # Client Request Successful
HTTPS = 'https://'                                         # Hypertext Transfer Protocol Secure (HTTPS)
COOKIE_EXPIRES = 20 - 1                                    # The cookie returned by Stealthwatch expires in 20 minutes
AUTHENTICATE = "/token/v2/authenticate"                    # login
LOGOUT = "/token"                                          # logout
GETDOMAINS = '/sw-reporting/v1/tenants'                    # returns list of domains (Tenants) configured  