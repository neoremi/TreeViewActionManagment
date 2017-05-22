# -*- coding: utf-8 -*-
#!/usr/bin/env python
# pascal v0-4-5
#
# Copyright 2017 Régis Hégo
#
# This file is part of Pascal.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
   print u"PyGtk 2.3.90 or higher version is required"  #LANG
   raise SystemExit

def PaChooser(action='open', patype = "pa"):
        fname = None
        if action != 'open' and action != 'saveas':
            return None
        if action == 'open':
            dialog = gtk.FileChooserDialog("Open..",    #LANG
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        if action == 'saveas':
            dialog = gtk.FileChooserDialog("Save as...",    #LANG
                                           None,
                                           gtk.FILE_CHOOSER_ACTION_SAVE,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        if patype == "pa":
            filter.set_name("Action Plans")     #LANG
            filter.add_mime_type("action/pa")
            filter.add_pattern("*.pa")
            dialog.add_filter(filter)
        elif patype == "csv":
            filter.set_name("Exported Plans")   #LANG
            filter.add_mime_type("action/csv")
            filter.add_pattern("*.csv")
            dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All files")    #LANG
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            fname=dialog.get_filename()
            if len(fname.split('.')) ==1:
                fname=dialog.get_filename() + "." + patype
        elif response == gtk.RESPONSE_CANCEL:
            fname = None
        dialog.destroy()
        return fname

def main():
    gtk.main()

if __name__ == "__main__":
    print PaChooser('saveas')
    main()
