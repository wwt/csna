Development Notes
-----------------
Notes and tips for using the remote development environment (via SSH) with VS Code.

To develop and app for Splunk SOAR, you need an instance of Splunk SOAR (Community Edition or licensed) and your target asset, CSNA/StealthWatch. Splunk SOAR can be installed in AWS EC2 from the marketplace on in a lab environment.

Splunk SOAR (Phantom) Community Edition
---------------------------------------
Installing Splunk SOAR Community Edition from AWS Marketplace.

EC2 Instance
------------
Select from AWS [Marketplace](https://aws.amazon.com/marketplace/pp/prodview-4ac4q4lzrhh4a#pdp-overview) version 5.1.0 and use a t2.2xlarge instnace with 8 cpu 32 Gig, 768G disk.

Login
-----
After starting the EC2 instance, login via SSH using the public key assigned to the instance.

```shell
ssh centos@54.237.22.196 -i customer_training.pem
```

Log in to the Splunk SOAR (On-premises) web interface:
https://docs.splunk.com/Documentation/SOARonprem/5.1.0/Install/Login

Initial install credentials are 'admin' and complete instance ID e.g. `i-00a6c83b6fa826feb` as the password. The password for the self-hosted version is `password` You should change the password following the initial login.

Set up development environment
------------------------------
Follow the instruction to set up  the [development environment](https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/SetUpADevEnvironment) and create the user 'phantom', you can logoff and return by using:

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
and you will be put in the home directory of the development user: `/home/phantom`.

Directories of interest
-----------------------------
The userid `phantom` has permissions to view the apps and log directories. The installed app(s) directory is at: `ls /opt/phantom/apps/*`. The log files are in `/var/log/phantom`. If you choose to install an app via the GUI, and the install fails, the log file `/var/log/phantom/app_install.log` provides additional information.

VSCode Remote SSH
-----------------
Use VSCode Remote SSH development environment to connect to the AWS EC2 instance (or a lab instance)

Instructions for configuring VS Code for a remote compute environment (Cloud compute, VM, etc.) are available at: https://gitlab.com/joelwking/vs_code_remote_compute - along with a Meetup session recording and slides available at: https://www.wwt.com/community/programmability-and-automation-meetup-group

A sample SSH configuration is a follows:
```
Host Splunk_SOAR
  User phantom
  HostName 54.237.22.196
  IdentityFile ~/.ssh/customer_training.pem
```

>Note: IdentifyFile is optional, if not specified, you will be prompted for the password.

Use the VSCode Remote Explorer SSH Target and connect to the remote Splunk SOAR instance. Open a terminal window, the user `phantom` has access to `git` and `python3.6`.

Guides for developing apps
--------------------------
Review and reference these URL for documenation on the API and app development.

 * [Develop Apps for Splunk SOAR (On-premises)](https://docs.splunk.com/Documentation/SOARonprem/latest/DevelopApps/Overview)

 * [Splunk SOAR app authoring API](https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/AppDevAPIRef)

How to set up the development environment with VSCode and remote SSH
--------------------------------------------------------------------
First open the remote SSH to the Splunk SOAR instance in VSCode. Using the terminal prompt, create a directory in your home directory `apps`

```
mkdir apps
```

Set your username and email address in the `git` configuration. Substitute your name and email address for the `user.name` and `user.email`.

```
git config --global user.name "Joel Example"
git config --global user.email joel.example@example.net
git config --global color.ui true
git config --global core.editor vim                  # Note esc + :q or esc + :q! to exit vim
```

Generate SSH key
----------------
Generate an SSH key and install it on your GitHub account.

```
ssh-keygen -t rsa -b 2048 -C "joel.example+phantom@example.net"
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

Clone the repository
--------------------
Assuming the repository is available (this repo may be moved to the WWT organization in the future) at `https://github.com/joelwking/csna.git`

Clone the repository using the SSH key generated previously.

```shell
GIT_SSH_COMMAND='ssh -i /home/phantom/.ssh/id_github' git clone git@github.com:joelwking/csna.git
```
Enter the cloned directory.

```shell
cd csna/phCiscoSecureNetworkAnalytics
```

Develop the app
---------------
Develop your app, and use `git add` / `git commit` to manage your changes. When you wish to push changes to the remote repository, `git push` using this command format.

```
GIT_SSH_COMMAND='ssh -i /home/phantom/.ssh/id_github' git push origin main
```

>Note: If you wish to maintain a local copy your your laptop, don't forget to `git pull` from the remote repository.

Utility program PHENV
---------------------

The program `phenv` is used to issue a number of subcommands to manage the installation. It is also used to execute Python apps using the correct python interpreter.

For help, `phenv --help` will show the commands.

```shell
[phantom@appdev ~]$ phenv 

Usage: /opt/phantom/bin/phenv command [args]
phenv will set the PATH and PYTHONPATH as neccessary to invoke python/pip for Splunk Phantom
Example: /opt/phantom/bin/phenv python /opt/phantom/bin/ibackup.pyc --setup

You can also use the "phenv <command>" to administrate certain aspects of Splunk Phantom.

```shell
/opt/phantom/bin/phenv set_preference --help
Run "/opt/phantom/bin/phenv help " to get a list of available commands
```

Testing interactively
---------------------
You can test your program without installing the application or using the web GUI by using the CLI. You need to create a `test.json` file to provide the configuration and parameters. Review the file `test_jsons/readme.md` for examples on how to create this input file.

```shell
cd csna/phCiscoSecureNetworkAnalytics
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

To get the absolute path of the Python interpreter:

```python
>>> import sys
>>> sys.executable
'/opt/phantom/usr/bin/python'
```

>Note: VSCode when running in debugging mode, will looks in your home directory `/home/phantom` for `.vscode/launch.json`, so you need to copy from `csna/.vscode/launch.json` to your home directory before running the debugger!

>Note: VSCode has some issues with the `main()` function of the program, as it attempts to connect to the `localhost` I added modifications in [commit](https://github.com/joelwking/csna/commit/a6107055eaf740a3e3022a63d9889240ec7857a5) to circumvent these issues, at least for now.

Create the tar file (optional)
------------------------------
To install the app, you need to create a tar file. Refer to the app installation in this link  https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/Connector
```
cd ~/apps/csna
tar -zcvf phCiscoSecureNetworkAnalytics.tgz phCiscoSecureNetworkAnalytics
```

Excluding files from the tar file (optional)
--------------------------------------------
Use `--exclude-from 'phCiscoSecureNetworkAnalytics/exclude_files.txt'` to exclude files from the tarball.

```shell
tar --exclude-from phCiscoSecureNetworkAnalytics/exclude_files.txt -zcvf phCiscoSecureNetworkAnalytics.tgz  phCiscoSecureNetworkAnalytics
```
The tar file can be downloaded from the remote instance to your laptop (to your Downloads directory perhaps) and import it into your Splunk SOAR web UI.

>Note: if the install fails in the GUI or the CLI, the log file `/var/log/phantom/app_install.log` can be used to determine the cause of the failure.

Compile and install the app from the CLI
----------------------------------------
Rather than simply creating a tar file, you can compile your app and install it locally. Compiling also lints the code, and checks the format of the JSON file. Refer to https://docs.splunk.com/Documentation/SOAR/current/DevelopApps/Tutorial#Compiling_and_installing_the_app for more information.

If you are developing your app and wish to install (publish) on the development instance, issue:

```shell
cd csna/phCiscoSecureNetworkAnalytics
phenv python /opt/phantom/bin/compile_app.pyc -i -g /home/phantom/app/csna/phCiscoSecureNetworkAnalytics/exclude_files.txt
```

>Note: specify the absolute path for the `-g IGNORE_FILE`.

The output of a successful install will appear as follows:

```shell
[phantom@appdev phCiscoSecureNetworkAnalytics]$ phenv python /opt/phantom/bin/compile_app.pyc -i -g /home/phantom/app/csna/phCiscoSecureNetworkAnalytics/exclude_files.txt 
cd'ing into ./
Will be ignoring: .git*, .vscode*, phCiscoSecureNetworkAnalytics/__pycache__, phCiscoSecureNetworkAnalytics/test_jsons/*
Validating App Json
    App json found at ./ciscosecurenetworkanalytics.json
  Validating App Json
  Validating actions
    test connectivity
      No further validation coded for "test connectivity" action
    retrieve flows
      Done
Compiling: ./__init__.py
Compiling: ./ciscosecurenetworkanalytics_consts.py
Compiling: ./ciscosecurenetworkanalytics_connector.py
Installing app...
  Creating tarball...
  ..//home/phantom/app/csna/phCiscoSecureNetworkAnalytics.tgz
  Calling installer...
  Success
Done
```

The compiler will create the tar file and leave it in your app home directory (e.g. `csna`) enabling you to include it in your remote GIT repository. Users can then download the tar file to their Splunk SOAR instance for use.

>Note: Verify your files have been ignored! If they have not, use the `tar` command to manually create the tar file before uploading to your Git remote!

Creating Test Data
------------------
To populate Splunk SOAR with test events to demonstrate your app, I wrote a Python class which uses the Splunk SOAR API to generate containers and artifacts.

The code is available at: https://github.com/joelwking/Phantom-Cyber/tree/master/REST_ingest

From the Splunk SOAR user interface (UI) naviate to Administration -> User Management -> Users and edit the user `automation`.  You need to show the token or set a new token.

```json
{
  "ph-auth-token": "*********",
  "server": "https://54.237.22.123"
}
```

Change the `Allowed IPs` to ***any*** or the IP address from where you are initiating the program.

From the developent account CLI, create two environment variables with your token and Splunk SOAR instance IP address.

```shell
export PH_AUTH_TOKEN=2adnymvMJMredactedHOM+xBGUNs1wEk=
export PH_SERVER=54.237.22.123
```

Download the code
-----------------
Create a directory and download the Python class. You can do this on your development account on your local laptop. 

```shell
mkdir artifact
cd artifact
curl https://raw.githubusercontent.com/joelwking/Phantom-Cyber/master/REST_ingest/PhantomIngest.py -o PhantomIngest.py
```

Create events
----------------------
Download and run this program to create events (containers and artifacts) in Splunk SOAR so the app can be run against an artifact.

```shell
phenv python
```
You can cut-n-paste the following into your Python interpreter or write your own program to generate events with data specific to your use case.  In this example, the IP address of `192.0.2.1` will be used as the `malicious_ip` for the app, so select an IP address that is represented in your Stealthwatch data.

```python
import PhantomIngest as ingest
import os
p = ingest.PhantomIngest(os.getenv('PH_SERVER'), os.getenv('PH_AUTH_TOKEN'))
kontainer = {'name': 'Voltaire', 'description': 'French Enlightenment writer, historian, and philosopher.', 'label': 'events'}
container_id = p.add_container(**kontainer)
art_i_fact = {"name": "François-Marie Arouet", "source_data_identifier": "IR_3458575"}
cef = {'sourceAddress': '192.0.2.1', 'sourcePort': '6553', 'sourceUserId': 'voltaire@example.net'}
meta_data = {}
artifact_id = p.add_artifact(container_id, cef, meta_data, **art_i_fact)
print(p.status_code, container_id, artifact_id)
```

Provided you have a status code of `200`, navigate to the Splunk SOAR UI and a new event should appear on the home screen.

Author
------
Joel W. King @joelwking