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

App Development Architecture and App Wizzard
---------------------------------------------
Documentation for [Develop Apps for Splunk SOAR (On-premises)](https://docs.splunk.com/Documentation/SOARonprem/5.1.0/DevelopApps/Overview)

