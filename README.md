# jenkins-blinkstick
A python script for monitoring several builds on a Jenkins CI server. The script uses a Blinkstick Pro to show the status lights.

## light status
* Heartbeat Blue indicates there is a Running job
* Green indicates the latest build is Successful
* Red indicates the latest build is Failed

## setup instructions

### OSX
* Install libusb with homebrew  
`sudo brew install libusb`
* Install pip  
`sudo easy_install pip`
* Install the BlinkStick Python package  
`sudo pip install blinkstick`

### Raspberry Pi
* Install pip (Python package management software)  
`sudo apt-get install python-pip`
* Install the BlinkStick Python package  
`sudo pip install blinkstick`
* Install Upstart if you would like the script auto-start  
`sudo apt-get install upstart`  
`# You will be asked to type 'Yes, do as I say!'`  
`# You may see an error about initctl being unable to connect, which will be fixed after a reboot`
* Reboot the RaspberryPi  
`sudo shutdown -r now`
Once the Raspberry Pi reboots Upstart should be installed. Upstart configuration files are placed in /etc/init.  
You can either use the sample Upstart configuration that comes with the Git repository, or you can use this example (place in /etc/init/jenkins.conf)  
`sudo nano /etc/init/jenkins.conf`  
Paste in the following code  
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
Press <kbd>Ctrl</kbd>+<kbd>X</kbd> then <kbd>y</kbd> to save.
* After creating the Upstart script, you should be able to start by running  
`sudo initctl start jenkins`

## References
* BlinkStick Python interface to control devices connected to the computer
  https://github.com/arvydas/blinkstick-python

