#!/usr/bin/env python

### This code is heavily inspired from https://gitorious.org/tomate
### And http://stackoverflow.com/questions/14208831/python-apt-pkg-to-obtain-individual-pkg-details

### Example configuration file
#
# icondir = '/home/imil/.icons/Faenza/status/scalable/'
# upgrade_icon = icondir + 'software-update-available-symbolic.svg'
# essential_icon = icondir + 'software-update-urgent-symbolic.svg'
# noop_icon = icondir + 'keyboard-brightness-symbolic.svg'
# working_icon = icondir + 'appointment-soon.svg'
#
# logdir = '/home/imil/log'

import pygtk
import gtk
import os
import gobject
import apt
import time
import signal
import sys
import logging
import pyinotify
from threading import Thread

pygtk.require('2.0')
gtk.gdk.threads_init()

configfile = os.path.expanduser("~") + '/.uptrc'

if os.path.isfile(configfile):
    exec(open(configfile).read())
else:
    sys.stderr.write('{0} is missing\n'.format(configfile))
    sys.exit(2)

# simple logging
if 'logdir' in globals() and os.path.isdir(logdir):
    logging.basicConfig(filename='{0}/upt.log'.format(logdir),
                        format='%(asctime)s - %(message)s',
                        level=logging.INFO)
else:
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.warn('missing logdir, logging to stdout')

class Chkupdate:
    def __init__(self):
        self.icon = gtk.status_icon_new_from_file(noop_icon)
        self.icon.set_tooltip("Idle")
        self.icon.set_visible(True)

        self.update_running = False

        self.notifier = None
        self.watchdir = '/var/lib/apt'

        self.tt_state = {
            'upgrade': 'Upgrades available',
            'essential': 'Urgent upgrades available',
            'noop': 'No upgrade available',
            'working': 'Operations in progress'
        }

    def quit(self):
        logging.info('stopping notifier thread')
        self.notifier.stop()
        logging.info('exiting')
        sys.exit(0)

    def set_state(self, state):
        icon = eval('{0}_icon'.format(state))
        self.icon.set_from_file(icon)
        self.icon.set_tooltip(self.tt_state[state])

    def aptchk(self):

        list_pkgs = []

        try:
            apt_cache = apt.Cache()
        except SystemError:
            return list_pkgs

        apt_cache.open()

        for package_name in apt_cache.keys():
            selected_package = apt_cache[package_name]

            if selected_package.is_upgradable:
                pkg = {
                        'name': selected_package.name,
                        'version' : selected_package.installed.version,
                        'candidate': selected_package.candidate.version,
                        'essential': selected_package.essential
                      }
                list_pkgs.append(pkg)

        return list_pkgs

    def update(self, ev=None):
        logging.info('entering update')
        if self.update_running is False:
            self.update_running = True
            self.set_state('working')
            lst = self.aptchk()
            if lst:  # packages to upgrade
                state = 'upgrade'
                for pkg in lst:
                    if pkg['essential'] is True:
                        state = 'essential'
            else:
                state ='noop'

            self.set_state(state)
            logging.info(self.tt_state[state])
        else:
            logging.info('update already running')

        self.update_running = False

    def timer_update(self):
        while True:
            self.update()
            time.sleep(3600)

    def main(self):
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        self.notifier = pyinotify.ThreadedNotifier(wm, self.update)
        wm.add_watch(self.watchdir, mask)
        self.notifier.start()

        t = Thread(target=self.timer_update)
        t.daemon = True
        t.start()

        gtk.main()

if __name__ == "__main__":
    app = Chkupdate()
    logging.info('starting upt')
    try:
        app.main()
    except KeyboardInterrupt:
        app.quit()
