# -*- coding: utf-8 -*-
#!/usr/bin/env python
# pascal v0-4-5

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
   print u"PyGtk 2.3.90 ou une version ultérieure est requise"
   raise SystemExit

def PaChooser(action='open', patype = "pa"):
        fname = None
        if action != 'open' and action != 'saveas':
            return None
        if action == 'open':
            dialog = gtk.FileChooserDialog("Ouvrir..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        if action == 'saveas':
            dialog = gtk.FileChooserDialog("Enregistrer sous...",
                                           None,
                                           gtk.FILE_CHOOSER_ACTION_SAVE,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        if patype == "pa":
            filter.set_name("Action Plans")
            filter.add_mime_type("action/pa")
            filter.add_pattern("*.pa")
            dialog.add_filter(filter)
        elif patype == "csv":
            filter.set_name("Exported Plans")
            filter.add_mime_type("action/csv")
            filter.add_pattern("*.csv")
            dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            fname=dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            fname = None
        dialog.destroy()
        return fname

def main():
    gtk.main()

if __name__ == "__main__":
    print PaChooser('saveas')
    main()
