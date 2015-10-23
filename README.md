# jenkins-blinkstick
A python script for monitoring several builds on a Jenkins CI server. The script uses a Blinkstick Pro to show the status lights.

## light status
* Heartbeat Blue indicates there is a Running job
* Green indicates the latest build is Successful
* Red indicates the latest build is Failed

## setup instructions

### OSX
* Install libusb with homebrew:<br/>
`sudo brew install libusb`
* Install pip<br/>
`sudo easy_install pip`
* Install the BlinkStick Python package<br/>
`sudo pip install blinkstick`

### Raspberry Pi
* Install pip (Python package management software):
`sudo apt-get install python-pip`
* Install the BlinkStick Python package<br/>
`sudo pip install blinkstick`
* Install Upstart if you would like the script autostart<br/>
`sudo apt-get install upstart`
* Create the Upstart config file<br/>
`sudo nano /etc/init/jenkins.conf`
* Paste in the following code
```bash
#author "Jonas Cheng"
#description "Upstart Script to run Jenkins Notifier as a service on Ubuntu/Debian"

#set username for the process. Should probably be what you use for logging in
setuid pi
setgid pi

start on runlevel [2345]
stop on runlevel [016]

respawn

#set command line to autostart
exec sudo python ~/jenkins-blinkstick/jenkins_notifier_multiple.py tellus

```
* Press <kbd>Ctrl</kbd>+<kbd>X</kbd> then <kbd>y</kbd> to save.

## References
* BlinkStick Python interface to control devices connected to the computer
  https://github.com/arvydas/blinkstick-python

