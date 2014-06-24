## upt, a simple update notifier

`upt` is a very simple update notifier that does nothing more (yet) than showing
an icon on [XFCE](http://www.xfce.org), GNOME 2 and awesome (+probably others)
panels informing if there are updates available for your `apt`-based system.

The very reason of this software to exist is the disappearance of an *XFCE*
compatible update notifier since *debian/jessie*, due to
yet-another-gnome3-mess.

In order for `upt` to work, you'll have to install a very basic `cron` job,
i.e.:

    */60	*	*	*	*	/usr/bin/apt-get -qq update

to the `root` user so the `apt` database is updated.

`upt` needs the following *python* modules:

  * `pygtk`
  * `apt`
  * `pyinotify`

Simply put :

    # apt-get install python-gtk2 python-apt python-pyinotify

`upt` configuration file is rather straightforward:

    icondir = '/home/imil/.icons/Faenza/status/scalable/'
    update_icon = icondir + 'software-update-available-symbolic.svg'
    essential_icon = icondir + 'software-update-urgent-symbolic.svg'
    noop_icon = icondir + 'keyboard-brightness-symbolic.svg'
    working_icon = icondir + 'appointment-soon.svg'
    
    logfile = '/home/imil/log/upt.log'

Do I really need to explain those? :)
