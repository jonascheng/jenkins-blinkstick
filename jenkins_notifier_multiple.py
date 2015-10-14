#! /usr/bin/python
import re
import signal
import sys
import time
import requests
from threading import Event, Thread
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.requester import Requester
from blinkstick import blinkstick

# preset configuration
JENKINS_URL = 'https://jenkins.midvale.leedsdev.net/'
DISABLE_SSL_VERIFY = True

led = blinkstick.find_first()
current_time = lambda: int(time.time())
found_running_job = False
thread_status_stop = thread_status = None


def get_server_instance():
    jenkins_url = JENKINS_URL
    while True:
        try:
            if DISABLE_SSL_VERIFY == True:
                requests.packages.urllib3.disable_warnings()
                return Jenkins(jenkins_url,requester=Requester("","",baseurl=jenkins_url,ssl_verify=False))
            else:
                return Jenkins(jenkins_url)
        except ConnectionError:
            print ConnectionError


def signal_handler():
    global thread_status, thread_status_stop
    print "Going to exist the monitor"
    if thread_status and thread_status.isAlive():
        thread_status_stop.set()
        thread_status.join()
    led.turn_off()
    sys.exit(0)


def get_jobs(regex):
    p = re.compile(regex, re.IGNORECASE)
    filtered_jobs = []
    j = get_server_instance()
    print "Connecting to:", j
    jobs_list = j.get_jobs_list()
    for job_name in jobs_list:
        if p.match(job_name):
            job = j.get_job(job_name)
            filtered_jobs.append(job)
    return filtered_jobs


def get_running_job(jobs):
    for job in jobs:
        if job.is_running():
            return job
    return None


def show_status(status, stop_event):
    color = 'green' if status == 'SUCCESS' else 'red'
    print "Show status:", color
    led.blink(channel=0, name='blue', repeats=5, delay=300)
    led.set_color(channel=0, name=color)


def show_running_status():
    global thread_status_stop
    while not thread_status_stop.is_set():
        led.pulse(channel=0, name='blue')
        time.sleep(0.1)


def run_check(regex):
    global found_running_job, thread_status, thread_status_stop
    jobs = get_jobs(regex)
    print "Got jobs:", jobs

    running_job = get_running_job(jobs)

    if thread_status and thread_status.isAlive():
        thread_status_stop.set()
        thread_status.join()

    # found current running job
    if running_job:
        print 'Running Build: %s' % running_job.name
        found_running_job = running_job
        thread_status_stop = Event()
        thread_status = Thread(target=show_running_status)
        thread_status.start()
    # no running job, show the latest build status for last running job
    elif found_running_job:
        last_build = found_running_job.get_last_build()
        status = last_build.get_status()
        print("Last Build: {} #{}, status: {}".format(
            found_running_job.name, last_build.get_number(), last_build.get_status()))
        thread_status_stop = Event()
        thread_status = Thread(target=show_status, args=(status, thread_status_stop))
        thread_status.start()        
    # first time start checking, search the latest build status
    else:
        timestampe = 0.0
        for job in jobs:
            if job.is_enabled():
                last_build_timestamp = time.mktime(job.get_last_build().get_timestamp().timetuple())
                if last_build_timestamp > timestampe:
                    timestampe = last_build_timestamp
                    found_running_job = job
        if found_running_job:
            last_build = found_running_job.get_last_build();
            status = last_build.get_status()
            print("Last Build: {} #{}, status: {}".format(
                found_running_job.name, last_build.get_number(), last_build.get_status()))
            thread_status_stop = Event()
            thread_status = Thread(target=show_status, args=(status, thread_status_stop))
            thread_status.start()        
        else:
            print "!!!!! No Build to monitor !!!!!"
    time.sleep(1.0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    if led != None:
        led.turn_off()
        while True:
            run_check(sys.argv[1])
    else:
        print "!!!!! Not detect any BlinkStick !!!!!"
