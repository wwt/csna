# csna
Cisco Secure Network Analytics (formerly Stealthwatch) app for Splunk SOAR (formerly Splunk Phantom)

Asset Configuration
-------------------
The asset definition requires these fields:

 * Userid
 * Password
 * Hostname / IP address
 * Tenant (Domain) display name

The Tenant (Domain) display name (displayName) is specified in the Management Console GUI and should be entered in the asset configuration. This enables creating an separate asset in Splunk SOAR for each Tenant (Domain). If you have a multi-domain system, You can create the same tag name for multiple assets and pass that tag to the `act()` function in playbooks. The action runs on all assets with that tag. 

App Actions
-----------
This app implements these actions.

test connectivity
-----------------
The `test connectivity` action is required of all apps. This action authenticates with the Management Console, verifying network reachability and a valid username and password. It does not validate the Tenant (Domain) exists on the Management Console. This validation step is a function of the `retrieve flows` action.

retrieve flows
---------------
The `retrieve flows` action uses the Stealthwatch Reporting - Version 2 API call to create flow searches and retrieve the searches' results. 

To retrieve data, a start and end date and time must be calculated and a record limit specified (or a default value). 

As an example, if the parameters specify:

 ``` 
 "start_time": "2022-01-05T15:30:0Z",
 "timespan": 60
 ```
The app calculates a flow filter with these values:

 ```
 "startDateTime": "2022-01-05T15:30:00Z",
 "endDateTime": "2022-01-05T16:30:00Z"
 ```

 If no values are specified for `start_time` and `timespan`, the `startDateTime` is 60 minutes from the current time, and the `endDateTime` is the current time. Effectively returning data from the past hour.

The flow search uses an IP address specified by the user to bound the search filter.

With the above information, a POST command is sent with the search filter in the body of the request. The app waits for the results to be generated and returns the `action_result.data` results (if any). Additionally `action_result.extra_data` includes the flow query id (`flow.query.id`) and the search filter (`flow.filter`) generated from the parameters specified, along with all configured Tenant display names and IDs. The Tenant ID (`tenantId`) is also included in the result data. 

References
----------
 * [Stealthwatch Enterprise REST API documentation](https://developer.cisco.com/docs/stealthwatch/)

 * [Update scripts to handle XSRF token introduced in 7.3.2](https://github.com/CiscoDevNet/stealthwatch-enterprise-sample-scripts/tree/handle-csrf-token/python)

 * [get the flows for a specific IP](https://github.com/CiscoDevNet/stealthwatch-enterprise-sample-scripts/blob/master/python/get_flows.py)

How to Information
------------------
In addition to the `DEVELOPMENT_NOTES.md` file, there is an internal WWT Stream channel with video recordings of the working sessions. The channel name is  **Splunk> SOAR**.

Author
------
Joel W. King @joelwking
