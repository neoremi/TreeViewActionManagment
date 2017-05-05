# -*- coding: utf-8 -*-
#!/usr/bin/env python

# There is no CellRenderer for entering a date via gtk.Calendar, we have to create own custom widget based on gtk.CellRendererText.
# Usually the CellRenderer creates onw gtk.Editable and returns it at the end of do_start_editing() method.
# This editable is then drawn inside the cell being edited and has to fit within it - which is not possible for a calendar (because of its size).
# We have to bypass all this "editable machinery", create own popup window (based on decoration-less, non-modal gtk.Dialog),
# properly position it (very tricky) below the cell being edited and handle the date entering.
# Being non-modal allows us to handle the focus-out event as cancel editing (user just clicks away from the calendar).

import gtk, gobject
import datetime


class CellRendererDate(gtk.CellRendererText):
    __gtype_name__ = 'CellRendererDate'
    def __init__(self):
        gtk.CellRendererText.__init__(self)
        self.date_format = '%d/%m/%y' # %y : année sur 2 digits / %Y sur 4 digits
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
        self.button = gtk.Button("Effacer la date")
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
        print response
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
        print "Supprimer la date"
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
