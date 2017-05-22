# -*- coding: utf-8 -*-
#!/usr/bin/env python
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

import gtk, gobject
import datetime
#from locale import getlocale, format_string, LC_ALL, LC_TIME


class CellRendererDate(gtk.CellRendererText):
    __gtype_name__ = 'CellRendererDate'
    def __init__(self,dtf):
        gtk.CellRendererText.__init__(self)
        #print getlocale(LC_TIME)
        #self.date_format = '%d/%m/%y' # %y : année sur 2 digits / %Y sur 4 digits #LANG...is french format!!!
        self.date_format = dtf
        self.calendar_window = None
        self.calendrier = None

    def _create_calendar(self, treeview):
        self.calendar_window = gtk.Dialog(parent=treeview.get_toplevel())
        self.calendar_window.action_area.hide()
        self.calendar_window.set_decorated(False)
        self.calendar_window.set_property('skip-taskbar-hint', True)
        self.calendrier = gtk.Calendar()
        self.calendrier.display_options(gtk.CALENDAR_SHOW_DAY_NAMES | gtk.CALENDAR_SHOW_HEADING)
        self.calendrier.connect('day-selected-double-click', self._day_selected, None)
        self.calendrier.connect('key-press-event', self._day_selected)
        self.calendrier.connect('focus-out-event', self._selection_cancelled)
        self.calendar_window.set_transient_for(None) # cancel the modality of dialog
        self.calendar_window.vbox.pack_start(self.calendrier)
        # necessary for getting the (width, height) of calendar_window
        self.button = gtk.Button("Erase date")      #LANG
        self.button.connect("clicked", self.do_erase_date)
        self.button.show()
        self.calendrier.show()
        self.calendar_window.vbox.pack_start(self.button)
        self.calendar_window.realize()

    def do_start_editing(self, event, treeview, path, background_area, cell_area, flags):
        if not self.get_property('editable'):
            return
        if not self.calendar_window:
            self._create_calendar(treeview)

        # select cell's previously stored date if any exists - or today
        if self.get_property('text'): 
            date = datetime.datetime.strptime(self.get_property('text'), self.date_format)
        else:
            date = datetime.datetime.today()
            self.calendrier.freeze() # prevent flicker
            (year, month, day) = (date.year, date.month - 1, date.day) # datetime's month starts from one
            self.calendrier.select_month(int(month), int(year))
            self.calendrier.select_day(int(day))
            self.calendrier.thaw()

            # position the popup below the edited cell (and try hard to keep the popup within the toplevel window)
            (tree_x, tree_y) = treeview.get_bin_window().get_origin()
            (tree_w, tree_h) = treeview.window.get_geometry()[2:4]
            (calendar_w, calendar_h) = self.calendar_window.window.get_geometry()[2:4]
            x = tree_x + min(cell_area.x, tree_w - calendar_w + treeview.get_visible_rect().x)
            y = tree_y + min(cell_area.y, tree_h - calendar_h + treeview.get_visible_rect().y)
            self.calendar_window.move(x, y)
#RHE
        response = self.calendar_window.run()
        if response == gtk.RESPONSE_OK:
            (year, month, day) = self.calendrier.get_date()
            date = datetime.date(year, month + 1, day).strftime (self.date_format) # gtk.Calendar's month starts from zero
            self.emit('edited', path, date)
            self.calendar_window.hide()
        if response == -6:  #default value ???
            date = 0
            self.emit('edited', path, date)
            self.calendar_window.hide()
        return None # don't return any editable, our gtk.Dialog did the work already

    def do_erase_date(self, event):
        print "Erase date"      #LANG
        self.calendar_window.response(-99)
        return True
        
    def _day_selected(self, calendar, event):
        # event == None for day selected via doubleclick
        if not event or event.type == gtk.gdk.KEY_PRESS and gtk.gdk.keyval_name(event.keyval) == 'Return':
            self.calendar_window.response(gtk.RESPONSE_OK)
        return True

    def _selection_cancelled(self, calendar, event):
        self.calendar_window.response(gtk.RESPONSE_CANCEL)
        return True
