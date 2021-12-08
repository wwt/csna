Splunk SOAR (Splunk Phantom)
----------------------------
Notes for installing Splunk SOAR Community Edition

EC2 Instance
------------
Select from AWS [Marketplace](https://aws.amazon.com/marketplace/pp/prodview-4ac4q4lzrhh4a#pdp-overview) version 5.1.0 running t2.2xlarge 8 cpu 32 Gig, 768G disk.

Login
-----
After the instance has started you can login via:

```shell
ssh centos@54.237.22.196 -i customer_training.pem
```

Log in to the Splunk SOAR (On-premises) web interface:
https://docs.splunk.com/Documentation/SOARonprem/5.1.0/Install/Login

Initial install credentials are 'admin' and complete instance ID e.g. `i-00a6c83b6fa826feb` as the password. The password for the self-hosted version is `password` You should change the password following the initial login.

The current password is `ffd47c7827cb`.

After setting up the [development environment](https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/SetUpADevEnvironment) and creating the user 'phantom', you can
logoff and return by using:

```shell
ssh centos@54.237.22.196 -i customer_training.pem
su phantom
<enter the same password as the admin login>
cd /home/phantom
```

Alternately, you can go directly to the development user by entering:

```shell
ssh phantom@54.237.22.196 -i customer_training.pem 
```
and you will be put in `/home/phantom`.

You can see the installed app(s) directory (and user phantom has permissions) at:

`/opt/phantom/apps/*ciscosecure*`

VSCode Remote SSH
-----------------
You can use the VSCode Remote SSH development environment to connect to the AWS EC2 instance.

```
Host Splunk_SOAR
  User phantom
  HostName 54.237.22.196
  IdentityFile ~/.ssh/customer_training.pem
```
Once connected, the `phantom` user has access to `git` and `python3.6`.

App Development Architecture and App Wizzard
---------------------------------------------
Documentation for [Develop Apps for Splunk SOAR (On-premises)](https://docs.splunk.com/Documentation/SOARonprem/5.1.0/DevelopApps/Overview)

Sample Use Case
---------------
Example Python code to get the flows for a specific IP in Stealthwatch using the REST API.

The user must provide the Sealthwatch Management Console:

* userid
* password
* hostname / IP address
* Tenant ID

This code provides an example of authenticating to the API (using a Requests Session), returning a `XSRF token` for future requests.

To retrieve data, a start and end date and time must be calculated and a record limit specified (or a default value).

With the above information, a POST command is sent, and the program should expect a response code of 201 and wait for the results to be generated. 

Based on a search id returned, the program will need to query (every second) until the percent complete is 100.0% Returned is a list of flows in the content. 

https://github.com/CiscoDevNet/stealthwatch-enterprise-sample-scripts/blob/master/python/get_flows.py

API documentation: https://developer.cisco.com/docs/stealthwatch/