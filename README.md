## upt, a simple update notifier

`upt` is a very simple update notifier that does nothing more (yet) than showing
an icon on [XFCE](http://www.xfce.org)'s (and probably GNOME 2) panel informing
if there are updates available for your `apt`-based system.

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

Feel free to modify `upt`'s notification icons as long as you give them the
same same:

  * `noop.svg` when no operation is needed
  * `upgrade.svg` when updated packages are available
  * `essential.svg` when essential packages updates are available
