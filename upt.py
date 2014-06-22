#!/usr/bin/env python

### This code is heavily inspired from https://gitorious.org/tomate
### And http://stackoverflow.com/questions/14208831/python-apt-pkg-to-obtain-individual-pkg-details

import pygtk
import gtk
import os
import gobject
import apt
import pyinotify

pygtk.require('2.0')
gtk.gdk.threads_init()

class Chkupdate:
    def __init__(self):
        icondir = self.icon_directory()
        self.icon = gtk.status_icon_new_from_file(icondir + "noop.svg")
        self.icon.set_tooltip("Idle")
        self.icon.set_visible(True)

        self.update_running = False

    def set_state(self, state):
        self.icon.set_from_file(self.icon_directory() + state + ".svg")
        self.icon.set_tooltip(state)

    def icon_directory(self):
        return os.path.dirname(os.path.realpath(__file__)) + os.path.sep

    def aptchk(self):
        apt_cache = apt.Cache() #High level

        apt_cache.open()

        list_pkgs = []

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
        print('entering update')
        if self.update_running is False:
            self.update_running = True
            lst = self.aptchk()
            if lst:  # packages to upgrade
                state = 'upgrade'
                for pkg in lst:
                    if pkg['essential'] is True:
                        state = 'essential'
                self.set_state(state)
            else:
                self.set_state('noop')
                print('nothing new')

        self.update_running = False

    def main(self):
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        notifier = pyinotify.ThreadedNotifier(wm, self.update)
        wm.add_watch('/var/lib/apt', mask)
        notifier.start()

        self.update()

        gtk.main()

if __name__ == "__main__":
    app = Chkupdate()
    app.main()
