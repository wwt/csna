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

>Note: IdentifyFile is optional, if not specified, you will be prompted for the password.

Once connected, the `phantom` user has access to `git` and `python3.6`.

App Development Architecture and App Wizzard
---------------------------------------------
Documentation for [Develop Apps for Splunk SOAR (On-premises)](https://docs.splunk.com/Documentation/SOARonprem/5.1.0/DevelopApps/Overview)


Phantom API Documentation
-------------------------
Splunk SOAR app authoring API
https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/AppDevAPIRef


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

How to set up the development environment with VSCode and remote SSH
--------------------------------------------------------------------

First open the remote SSH to the phantom server in VSCode.

From your terminal prompt, create a directory in your home directory `apps`

```
mkdir apps
```

Set your username and email address in the get configuration.

```
git config --global user.name "Joel W. King"
git config --global user.email joel.king@wwt.com
git config --global color.ui true
git config --global core.editor vim                  # Note esc + :q or esc + :q! to exit vim
```

Generate an SSH key and install it on your GitHub account.

```
ssh-keygen -t rsa -b 2048 -C "joel.king+phantom@wwt.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/phantom/.ssh/id_rsa): /home/phantom/.ssh/id_github
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/phantom/.ssh/id_github.
Your public key has been saved in /home/phantom/.ssh/id_github.pub.
```

View the key and copy and paste it into your account, https://github.com/settings/keys

```
cat /home/phantom/.ssh/id_github.pub
```
Assuming the repository is available (this repo will be moved to the WWT organization in the future) at `https://github.com/joelwking/csna.git`

```
GIT_SSH_COMMAND='ssh -i /home/phantom/.ssh/id_github' git clone git@github.com:joelwking/csna.git
cd csna/phCisco\ Secure\ Network\ Analytics/
```

***INSERT EXECUTING INSTRUCTIONS HERE***


After making your changes:

```
GIT_SSH_COMMAND='ssh -i /home/phantom/.ssh/id_github' git push origin main
```


Utility progrm PHENV
--------------------

The program `phenv` is used to issue a number of subcommands to manage the installation. It is also used to execute Python apps using the correct python interpreteter.

For help, `phenv --help` will show the commands.

```shell
[phantom@appdev ~]$ phenv 

Usage: /opt/phantom/bin/phenv command [args]
phenv will set the PATH and PYTHONPATH as neccessary to invoke python/pip for Splunk Phantom
Example: /opt/phantom/bin/phenv python /opt/phantom/bin/ibackup.pyc --setup

You can also use the "phenv <command>" to administrate certain aspects of Splunk Phantom
Example: /opt/phantom/bin/phenv set_preference --help
Run "/opt/phantom/bin/phenv help " to get a list of available commands
```

Testing interactively
---------------------

You can test your program without installing the application or using the web GUI by the following:

```
phenv python ./ciscosecurenetworkanalytics_connector.py -u admin -p adminpswd test_jsons/test.json
```

Remote Debugging with VS Code
-----------------------------

You will need to use `phenv` to determine the Python interpreter and PYTHONPATH to configure your `.vscode/launch.json` for debugging.

Rather than look at the source code of `phenv`, just run python from it, and check what path and executable is being used.

```python
[phantom@appdev csna]$ phenv python
Python 3.6.13+ (heads/3.6-dirty:a64de63, Mar 26 2021, 15:25:25) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.getenv('PYTHONPATH')
'/opt/phantom/www:/opt/phantom/lib3:/opt/phantom/pycommon3:/opt/phantom/www:/opt/phantom/lib:/opt/phantom/pycommon:/opt/phantom/www:/opt/phantom/lib:/opt/phantom/pycommon:/opt/phantom/www:/opt/phantom/lib:/opt/phantom/pycommon:/opt/phantom/www:/opt/phantom/lib:/opt/phantom/pycommon:'
>>> 
```
To get the full path of the interpreter:

```python
>>> import sys
>>> sys.executable
'/opt/phantom/usr/bin/python'
```

>Note: VSCode when running in debugging mode, will look in your home directory `/home/phantom` for `.vscode/launch.json`, so you need to copy from `csna/.vscode/launch.json` to your home directory before running the debugger.

>Note: VSCode has some issues with the `main()` function of the program, as it attempts to connect to the `localhost` I added modifications in [commit](https://github.com/joelwking/csna/commit/a6107055eaf740a3e3022a63d9889240ec7857a5) to circumvent these issues, at least for now.


Create the tar file
-------------------
See App installation in this link  https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/Connector
```
cd ~/apps/csna
tar -zcvf ciscosecurenetworkanalytics.tgz 'phCisco Secure Network Analytics'
```

>Note: use `--exclude-from 'phCisco Secure Network Analytics/exclude_files.txt'` to exclude files from the tarball.

```
tar --exclude-from 'phCisco Secure Network Analytics/exclude_files.txt' -zcvf ciscosecurenetworkanalytics.tgz 'phCisco Secure Network Analytics'
```

Then download the tar file (to your Downloads directory perhaps) and import it into your Splunk SOAR web UI.