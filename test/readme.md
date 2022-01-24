Generating Splunk> SOAR events
------------------------------
These instructions provide a means to create (test) data, events (containers and artifacts) from Python code running in a Docker container. While Docker is not installed on the Splunk> SOAR server, you can install Docker Desktop on a laptop and create events for testing the Cisco Secure Network Analytics (Stealthwatch) app.

Clone the repository
--------------------
Clone this repository and enter the cloned (`csna`) directory. As an example:

```shell
~/Documents/WWT/projects/phantom_cyber/csna %
```

Build the image
---------------
Issue the command to build the image.

```shell
docker build -t joelwking.phantom:1.0 .
```

After a successful build, list the image.

```shell
~/Documents/WWT/projects/phantom_cyber/csna % docker image ls joelwking.phantom:1.0
REPOSITORY          TAG       IMAGE ID       CREATED              SIZE
joelwking.phantom   1.0       926acd7d2d30   About a minute ago   288MB
```

Run the image
-------------
Run the image and enter the container. You will need to specify the hostname / IP address of your Splunk> SOAR instance along with the API key for the `automation` user on Phantom. Refer to Administration-> User Management-> Users -> automation. Verify the value of `Allowed IPs` is any or your laptop IP address is specified.

```shell
docker run -it joelwking.phantom:1.0 /bin/bash
root@0188ebc1d878:/code#
```

Enter the test directory
------------------------
You will need to specify the hostname / IP address of your Splunk> SOAR instance along with the API key for the `automation` user on Phantom. Refer to Administration-> User Management-> Users -> automation. Verify the value of `Allowed IPs` is any or your laptop IP address is specified.

Specify these values as environment variables and activate the virtual environment

```shell
export PH_AUTH_TOKEN=0uX9KHEZr27gYredactedbk4pG3DB7kCbk=
export PH_SERVER=198.19.20.175
source /opt/soar/bin/activate
cd test
```

There is a sample YAML input file in the test directory. Review it.

```yaml
root@0188ebc1d878:/code/test# cat input.yml
---
container:
  name: 'Voltaire'
  description: 'French Enlightenment writer, historian, and philosopher.'
  label: events
  artifacts:
    - name: DEMO99
      source_data_identifier: "IR_3458575"
      meta_data:
        quote: "Judge of a man by his questions rather than by his answers."
      cef:
        sourceAddress: '10.10.101.24'
        sourcePort: 6553
        sourceUserId: administrator
        deviceCustomNumber1: 2000
        deviceCustomNumber1Label: 'record_limit'
        deviceCustomNumber2: 250
        deviceCustomNumber2Label: timespan
        startTime: default
        deviceCustomDate1: default
```

>Note: if you specify the keyword `default` for `startTime` or `deviceCustomDate1` the program will calculate these values for you. Otherwise, specify milliseconds from EPOCH time and ISO8601 respectively and use the `-c` switch at program execution time.

Examine the help file
---------------------
Use the `-h` argument to view help.

```
(soar) root@0188ebc1d878:/code/test# python gen_events.py -h
usage: gen_events [-h] [-c] -f DOCUMENT

Create events in Splunk> SOAR

optional arguments:
  -h, --help            show this help message and exit
  -c, --custom          update custom fields if not set
  -f DOCUMENT, --file DOCUMENT
                        a YAML formatted input file
```

Run the program
---------------
Execute the program from the command line, using the sample input.

```shell
soar) root@0188ebc1d878:/code/test# python gen_events.py -c -f input.yml
Added container: 24
 |---  artifact: 24
```

Logon the Splunk> SOAR GUI and examine the newly created event (container and artifact). The event ID in the GUI is the container ID returned from the program. After selecting that event, select the ARTIFACT tab, the artifact ID matches the artifact ID from the program.

Map a file into the container
-----------------------------
We can use an input file from our laptop and map the file (volume) into the container. We can also create multiple artifacts for the event. For example, assume this file is in `Downloads/multi.yml`. It will create two artifacts associated with the event in Splunk> SOAR.

```yaml
---
container:
  name: MULTI
  description: 'French Enlightenment writer, historian, and philosopher.'
  label: events
  artifacts:
    - name: DEMO99
      source_data_identifier: "IR_3458575"
      meta_data:
        quote: "Judge of a man by his questions rather than by his answers."
      cef:
        sourceAddress: '10.10.101.24'
        sourcePort: 6553
        sourceUserId: administrator
        deviceCustomNumber1: 2000
        deviceCustomNumber1Label: 'record_limit'
        deviceCustomNumber2: 250
        deviceCustomNumber2Label: timespan
        startTime: default
        deviceCustomDate1: default

    - name: DEMO98
      source_data_identifier: "IR_3458575"
      meta_data:
        quote: "the quick brown fox"
      cef:
        sourceAddress: '198.19.30.36'
        sourcePort: 6553
        sourceUserId: administrator
        deviceCustomNumber1: 2000
        deviceCustomNumber1Label: 'record_limit'
        deviceCustomNumber2: 250
        deviceCustomNumber2Label: timespan
        startTime: 1639457164
        deviceCustomDate1: '2022-01-24T19:46:04Z'
```

```shell
docker run -v /Users/kingjoe/Downloads/multi.yml:/code/test/multi.yml:ro -it joelwking.phantom:1.0 /bin/bash
```
>Note: don't forget to set your virtual environment and environment variables!

```shell
(soar) root@d9a7fb91e345:/code/test# python gen_events.py -c -f multi.yml
Added container: 26
 |---  artifact: 27
 |---  artifact: 28
```

Examine the event ID 26 and the two artifacts 27 and 28.

Author
------
Joel W. King @joelwking