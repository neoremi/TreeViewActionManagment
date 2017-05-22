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


import pygtk
from gtk._gtk import TreeSelection, Statusbar
#import cellrendrerdate
from cellrendrerdate import CellRendererDate    #customized renderer for date management
#from paparams import ParamsTab
from paparams import *   # include constant definition
from pacommon import *   # include common functions
#from duplicity.path import Path
pygtk.require('2.0')
import gtk, gobject
#import time
#from string import strip
import ConfigParser #manage init files

import os.path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app_win = None
#app_win.curPA           current file index in the list of open files
#app_win.maxPA           index of the last open file
#app_win.initFile        ini file name
#app_win.table           the app_win windows displays a table
#app_win.menu_main       menubar
#app_win.accel_group     accelerator group
#app_win.notebook        notebook that displays data of loaded files
#app_win.FileOpen[curpa]                     model
#app_win.FileOpen[curpa].Store.tree_store    tree store containing data of the loaded file
#app_win.FileOpen[curpa].PAFile              loeaded file name

icon_file = "../img/RHE.png"

actions = gtk.ActionGroup("General")

def menu_toolbar_create():
        app_win.menu_main = gtk.MenuBar()
        menu_file = gtk.Menu()    
        menu_item_file = gtk.MenuItem('File')   #LANG
        menu_item_file.set_submenu(menu_file)

#        actions.quit = gtk.Action("Quit", "Quitter", "Quit Application", gtk.STOCK_QUIT)
        actions.quit = gtk.Action("Quit", "Quit", "Quit Application", gtk.STOCK_QUIT)   #LANG
        actions.quit.connect ("activate", quit_dlg)
        actions.add_action(actions.quit)
        menuItem_quit = actions.quit.create_menu_item()
        menuItem_quit.add_accelerator("activate", app_win.accel_group, ord("Q"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menuItem_quit)

        #Normally, we'd also catch the "clicked" signal on each of the menu items
        # and setup a callback for it, but it's omitted here to save space.
#        actions.opn = gtk.Action("Open", "Ouvrir", "Open a structure", None)
        actions.opn = gtk.Action("Open", "Open", "Open a structure", None)  #LANG
        actions.opn.connect ("activate", fct_open, "Open a file")   #LANG
        actions.add_action(actions.opn)
        menuItem_opn = actions.opn.create_menu_item()
        menuItem_opn.add_accelerator("activate", app_win.accel_group, ord("O"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menuItem_opn)

#        actions.save = gtk.Action("Save", "Enregistrer", "Save as data file", gtk.STOCK_SAVE)
        actions.save = gtk.Action("Save", "Save", "Save as data file", gtk.STOCK_SAVE)   #LANG
        actions.save.connect ("activate", save)
        actions.add_action(actions.save)
        menu_item_save = actions.save.create_menu_item()
        menu_item_save.add_accelerator("activate", app_win.accel_group, ord("S"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menu_item_save)
    
#        actions.saveAs = gtk.Action("Save as...", "Enregistrer sous...", "Save as data file", gtk.STOCK_SAVE)
        actions.saveAs = gtk.Action("Save as...", "Save as...", "Save as data file", gtk.STOCK_SAVE)    #LANG
        actions.saveAs.connect ("activate", saveas)
        actions.add_action(actions.saveAs)
        menu_item_saveAs = actions.saveAs.create_menu_item()
#        menu_item_saveAs.add_accelerator("activate", app_win.accel_group, ord("S"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menu_item_saveAs)
    
#        actions.savec = gtk.Action("Savec", "Enregistrer et fermer", "Save as data file and close", gtk.STOCK_SAVE)
        actions.savec = gtk.Action("Savec", "Save and close", "Save as data file and close", gtk.STOCK_SAVE) #LANG
        actions.savec.connect ("activate", saveandclose)
        actions.add_action(actions.savec)
        menu_item_save = actions.savec.create_menu_item()
        menu_item_save.add_accelerator("activate", app_win.accel_group, ord("R"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menu_item_save)
    
#        actions.nosave = gtk.Action("noSave", "Fermer sans enregistrer", "Close without save files", gtk.STOCK_SAVE)
        actions.nosave = gtk.Action("noSave", "Close without save", "Close without save files", gtk.STOCK_SAVE) #LANG
        actions.nosave.connect ("activate", simplyclose)
        actions.add_action(actions.nosave)
        menu_item_nosave = actions.nosave.create_menu_item()
        menu_item_nosave.add_accelerator("activate", app_win.accel_group, ord("T"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menu_item_nosave)
    
        actions.imp = gtk.Action("Import", "Import", "Convert CSV to PA file", None)    #LANG
        actions.imp.connect ("activate", fct_import, "Import")
        actions.add_action(actions.imp)
        menuItem_imp = actions.imp.create_menu_item()
        menuItem_imp.add_accelerator("activate", app_win.accel_group, ord("I"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menuItem_imp)

#        actions.exp = gtk.Action("Export", "Exporter", "Save a structure", None)
        actions.exp = gtk.Action("Export", "Export", "Save a structure", None)  #LANG
        actions.exp.connect ("activate", fct_export, app_win.curPA)
        actions.add_action(actions.exp)
        menuItem_exp = actions.exp.create_menu_item()
        menuItem_exp.add_accelerator("activate", app_win.accel_group, ord("E"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_file.append(menuItem_exp)

        menu_params = gtk.Menu()
        menu_item_struct = gtk.MenuItem("Structure")    #LANG
        menu_item_struct.set_submenu(menu_params)

#        actions.Struct = gtk.Action("Setting", "Paramètres", "Structure setting", None)
        actions.Struct = gtk.Action("Setting", "Settings", "Structure setting", None)   #LANG
        actions.Struct.connect ("activate", struct_setting)
        actions.add_action(actions.Struct)
        menu_item_conf = actions.Struct.create_menu_item()
        menu_item_conf.add_accelerator("activate", app_win.accel_group, ord("P"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_params.append(menu_item_conf)

#        actions.ReNew = gtk.Action("New", "Nouvelles données", "Create a new file with the same structure", None)
        actions.ReNew = gtk.Action("New", "New data", "Create a new file with the same structure", None)    #LANG
        actions.ReNew.connect ("activate", fct_renew)
        actions.add_action(actions.ReNew)
        menu_item_renew = actions.ReNew.create_menu_item()
        menu_item_renew.add_accelerator("activate", app_win.accel_group, ord("N"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_params.append(menu_item_renew)

#        actions.New = gtk.Action("Renew", "Nouvelle structure", "Create a new file with the same structure", None)
        actions.New = gtk.Action("Renew", "New structure", "Create a new file with the same structure", None)   #LANG
        actions.New.connect ("activate", fct_new)
        actions.add_action(actions.New)
        menu_item_new = actions.New.create_menu_item()
        menu_item_new.add_accelerator("activate", app_win.accel_group, ord("B"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_params.append(menu_item_new)

#        actions.Glob = gtk.Action("Glob", "Paramètres de l'application", "Define application parameters", None)
        actions.Glob = gtk.Action("Glob", "Application settings", "Define application settings", None)     #LANG
        actions.Glob.connect ("activate", fct_glob)
        actions.add_action(actions.Glob)
        menu_item_glob = actions.Glob.create_menu_item()
        menu_item_glob.add_accelerator("activate", app_win.accel_group, ord("G"), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        menu_params.append(menu_item_glob)

        # And finally we append the menu-item to the menu-bar
        app_win.menu_main.append(menu_item_file)
        app_win.menu_main.append(menu_item_struct)
        app_win.menu_main.show()

def fct_glob(widget, event=None):
    ParamsGlob()
    apply_ini()
    
def fct_renew(widget, event=None):
    """'Save structure as' function : Save as without data"""
    print "Create an empty file with the same structure"    #LANG
    if app_win.curPA > -1:
        saveas(widget, event, False)
    else:
        buf = "Data reset requires an activated plan."  #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)

def fct_new(widget, event=None):
    print "Create a new plan structure"     #LANG
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    Config = ConfigParser.ConfigParser()
    rdf = []
    rdf = Config.read(app_win.initFile)   # Return list of successfully read files
    if rdf != []:
        lastStruct = Config.get(SEC_INI_OPEN, "struct01")
        if lastStruct == "" :
            set_default_ini_config(Config, app_win.dico)
            lastStruct = INIFILE
        if OpenDataFile(lastStruct,app_win.maxPA):  #data loading
            DataToNotebook(app_win.maxPA-1, app_win.maxPA-1)
#    ParamsTab(extcall=True)
    struct_setting(widget)
    
def fct_open(widget, string, fPA=None):
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    if fPA == None:
        file_dialog = gtk.FileChooserDialog(("Open..."), app_win, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))   #LANG
        file_dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.add_mime_type("pa")
        filter.add_pattern("*.pa")
        file_dialog.add_filter(filter)
        file_dialog.set_filename("test.pa")
        response = file_dialog.run()
        if response == gtk.RESPONSE_OK:
            fPA = file_dialog.get_filename()
            if OpenDataFile(fPA,app_win.maxPA):  #data loading
                DataToNotebook(app_win.maxPA-1, app_win.maxPA-1)
                buf = "Openning file '%s'" % file_dialog.get_filename()  #LANG
                app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
        file_dialog.destroy()
    else:
        if OpenDataFile(fPA,app_win.maxPA):  #data loading
            DataToNotebook(app_win.maxPA-1, app_win.maxPA-1)
        
def fct_import(widget, string, fPA=None):
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    paName = CSVTopa(PaChooser("open", "csv"))
    if paName != None:
        if OpenDataFile(paName,app_win.maxPA):  #data loading
            DataToNotebook(app_win.maxPA-1, app_win.maxPA-1)
            buf = "Import and open '%s'" % paName    #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)

def fct_export(widget, curpa):
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    if app_win.curPA <0 :
        buf = "There is no file to export"   #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
        return True
    #savePA(app_win.FileOpen[curpa].Store.tree_store, app_win.FileOpen[curpa], app_win.FileOpen[curpa].PAFile)
    paToCSV(app_win.FileOpen[curpa].PAFile)

def struct_setting(widget, event=None):
    """Open structure management interface of the current file. If no file is open or new structure required, a default structure will be create."""
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    if app_win.curPA>-1:
        # save data file before access to settings without confirm
        app_win.curPA = app_win.notebook.get_current_page()    # store current PA    
        save(None, False)
        modfile = app_win.FileOpen[app_win.curPA].PAFile
        ParamsTab(modfile, extcall=True)
        # close file
        simplyclose(None, confirm=False)
        # reload file and settings modifications or load new structure
        if modfile == "" or modfile == INIFILE:
            Config = ConfigParser.ConfigParser()
            rdf = []
            rdf = Config.read(INIFILE)
            modfile = Config.get(SEC_INI_OPEN, ITM_LASTSTRUCT)
        if OpenDataFile(modfile,app_win.maxPA):  #data loading
            TestDataStruct()
            DataToNotebook(app_win.maxPA - 1, app_win.maxPA - 1)
            buf = "Reload file '%s'" % modfile  #LANG
            print buf
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            writeIni(app_win.FileOpen[app_win.curPA],app_win.initFile, app_win.dico,struct="")

    else:
        buf = "Setting requires an active plan."   #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)

class StatusPA:
    #function to add a message to the stack
    def push_item(self, widget, ctx, mess):
        self.count = self.count + 1
        self.status_bar.push(ctx, mess)
        return

    #function to remove the last pushed message
    def pop_item(self, widget, ctx):
        self.status_bar.pop(ctx)
        return

    def __init__(self):
        self.count = 1
        self.vbox = gtk.VBox(False, 1)
        self.vbox.show()
          
        self.status_bar = gtk.Statusbar()      
        self.vbox.pack_start(self.status_bar, True, True, 0)
        self.status_bar.show()
        self.context_id = self.status_bar.get_context_id("PA")  #context id definition for status bar FIFO
        
class BarreOutil:
    # Exit event treatment
    def delete_event(self, widget, event=None):
        gtk.main_quit()
        return False
    
    #adding functions
       
    def add_action(self,widget=None,event=None,code=None,data=None, curpa=None):
        if curpa == None:   # if addition is request by button (not by file loading)
            app_win.curPA = app_win.notebook.get_current_page()
            curpa=app_win.curPA
        if curpa <0:
            buf = "You have to load a .pa file or define a structure before adding elements"   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            return
        app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
        #print "add_action / curpa = %s" % curpa
        model = app_win.FileOpen[curpa].Store.tree_store
        fmodel = app_win.FileOpen[curpa]
        if self.inc_auto_id(curpa) == False:
            buf = "One more node can't be added because of id limitation"   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            return
        # id of the new node is chosen or automatically determined
        if code == None:
            newnode = fmodel.newnode    #empty node structure for the loaded structure
        else:
            pass
        #If id is chosen, non-existence is requested
        #Node is added at level 1 after last position
        if code != None:
            match_iter = self.search(model, model.iter_children(None),self.match_func, (fmodel.idpos, data[fmodel.idpos+INTDATACOUNT]))
            if match_iter:
                buf = "WARNING : The node %s already exists! It can't be added." % data[fmodel.idpos]   #LANG
                app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
                print buf
                return    
        # Look for last node at the fist level
        prevNode = None
        tvnode = model.get_iter_first()
        while tvnode:
            prevNode = tvnode
            tvnode = model.iter_next(prevNode)
        if code == None:
            newnode[fmodel.idpos] = str(fmodel.IDmax)   # set an id for the node
            tvnode = model.append(None,newnode)
        else:
            # new node building from structure
            newnode = []
#            newnode.append(data[fmodel.idpos])
            for fld in range(fmodel.fieldsCount):
                if fmodel.fieldsStruct[fld][FLDNAT] == "bool":   # boolean values to translate
                    if data[fld+INTDATACOUNT] == "False":
                        newnode.append(False)
                    else:
                        newnode.append(True)
                else :
                    newnode.append(data[fld+INTDATACOUNT])
            tvnode = model.append(match_iter,newnode)

    def add_next(self,widget,event=None,curpa=None):
        """Add an action at the same level"""
        if curpa == None:   # if addition is request by button (not by file loading)
            app_win.curPA = app_win.notebook.get_current_page()
            curpa=app_win.curPA
        if curpa <0:
            buf = "You have to load a .pa file or define a structure before adding elements"   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            return
        app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)
        model = app_win.FileOpen[curpa].Store.tree_store
        fmodel = app_win.FileOpen[curpa]
        newnode = fmodel.newnode
        if self.inc_auto_id(curpa) == False:
            buf = "One more node can't be added because of id limitation"   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            return
        
        TreeSelection = fmodel.Display.view.get_selection()
        tm,tvnode = TreeSelection.get_selected()
        if tvnode:
            newnode[fmodel.idpos] = str(fmodel.IDmax)
            tvnode = model.insert_after(None,tvnode,newnode)

    def add_detail(self,widget=None,event=None,code=None,data=None,curpa=None):
        "Add an action to detail a 'master' action"
        if curpa == None:   # if addition is request by button (not by file loading)
            app_win.curPA = app_win.notebook.get_current_page()
            curpa=app_win.curPA
        if curpa <0:
            buf = "You have to load a .pa file or define a structure before adding elements"   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            return
        app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)
        model = app_win.FileOpen[curpa].Store.tree_store
        fmodel = app_win.FileOpen[curpa]
        if self.inc_auto_id(curpa) == False:
            buf = "One more node can't be added because of id limitation"   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            return
        if code != None:
            #print "looking for %s" % data[fmodel.idpos+INTDATACOUNT]
            match_iter = self.search(model, model.iter_children(None),self.match_func, (fmodel.idpos, data[fmodel.idpos+INTDATACOUNT]))
            if match_iter:
                buf = "WARNING : The node %s already exists! It can't be added." % data[fmodel.idpos]   #LANG
                app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
                print buf
                return    
            match_mother = self.search(model, model.iter_children(None),self.match_func, (fmodel.idpos, data[MOTHERPOS]))
            if match_mother:
                newnode = []
                for fld in range(fmodel.fieldsCount):
                    if data[fld+INTDATACOUNT] == "False" and fmodel.fieldsStruct[fld][FLDNAT] == "bool":
                        newnode.append(False)
                    else :
                        newnode.append(data[fld+INTDATACOUNT])
                tvnode = model.append(match_mother,newnode)
            else:
                buf = "WARNING : Mother node %s hasn't be found!" % data[MOTHERPOS]     #LANG
                app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
                print buf
        else:
            TreeSelection = fmodel.Display.view.get_selection()
            tm,tvnode = TreeSelection.get_selected()
            if tvnode:
                newnode = fmodel.newnode
                newnode[fmodel.idpos] = str(fmodel.IDmax)
                tvnode = model.append(tvnode,newnode)

    def inc_auto_id(self,curpa=0):
        """Find next available ID, return False if roof is reached"""
        model = app_win.FileOpen[curpa].Store.tree_store
        fmodel = app_win.FileOpen[curpa]
        if fmodel.IDmax < fmodel.IDroof:
            #Test availability of the default next code
            while app_win.Barre.search(model, model.iter_children(None),app_win.Barre.match_func, (fmodel.idpos, str(fmodel.IDmax))):
                fmodel.IDmax +=1
        else:
            return False
        return True
    
    def suppr_node(self,widget,event=None,curpa=None):
        """Action deletion"""
        app_win.curPA = app_win.notebook.get_current_page()
        curpa=app_win.curPA
        if curpa <0:
            buf = "You have to load a .pa file or define a structure before adding elements"   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            return
        app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)
        model = app_win.FileOpen[curpa].Store.tree_store
        fmodel = app_win.FileOpen[curpa]
        TreeSelection = fmodel.Display.view.get_selection()
        tm,tvnode = TreeSelection.get_selected()
        if tvnode:
            tvnode = model.remove(tvnode)

    def match_func(self, model, tvnode, data):
        """Function that compares the value of a column between two nodes"""
        col, k = data # data is a tuple including column and value searched
#        value = model.get_value(tvnode, col)
        value = model.get_value(tvnode, 0)
        return value == k

    def search(self,model, tvnode, fonc_rech, data):
        """Search a field value in a branch of the treeview using a compare function"""
#        print "Searching in %s of %s" % (model,data)
        while tvnode :
            if fonc_rech(model, tvnode, data):
                return tvnode
            result = self.search(model, model.iter_children(tvnode), fonc_rech, data)
            if result: return result
            tvnode = model.iter_next(tvnode)
        return None

    def select_ID(self,widget,saisie,curpa=0):
        model = app_win.FileOpen[curpa].Store.tree_store
        fmodel = app_win.FileOpen[curpa]
        selID = saisie.get_text()
        #print "Selection of the item %s" % selID
        match_iter = self.search(model, model.iter_children(None),self.match_func, (TT, selID))
        #print match_iter    
        TreeSelection = fmodel.Display.view.get_selection()
        TreeSelection.select_iter(match_iter)
        
    def radio_event(self, widget, toolbar):
        """radio buttons management"""
        if self.button1.get_active():
            pass
            #print "radio button 1 activated"
        elif self.button2.get_active():
            pass
            #print "radio button 2 activated"

    def toggle_event(self, widget, toolbar):
        """toggle button management"""
        pass
        #print "toggle done"

    def __init__(self):
        # Si on considère la barre indépendante dans une fenêtre (dialog)
        # Création d'une nouvelle fenêtre (type dia            data = ""log)
        #dialog = gtk.Dialog()
        #dialog.set_title("Gestion de plan d'action")
        #dialog.set_size_request(700, 250)
        #dialog.set_resizable(True)

        # Connexion du signal au traitement de clôture
        #dialog.connect("delete_event", self.delete_event)

        # la barre d'outil est mise dans une handle box pour pouvoir être détachée de la fenêtre
        self.handlebox = gtk.HandleBox()
        #dialog.vbox.pack_start(handlebox, False, False, 5)

        #création d'une boîte à outil horizontale
        self.toolbar = gtk.Toolbar()
        self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        # avec des boutons composés de texte et d'image
        self.toolbar.set_style(gtk.TOOLBAR_BOTH)
        self.toolbar.set_border_width(5)
        self.handlebox.add(self.toolbar)

        # Create main adding button
        iconw = gtk.Image() # icon widget
        iconw.set_from_file("../img/add1.xpm")
        add1_button = self.toolbar.append_item(
            "Append",           # button label	        #LANG
            "Add a first level element", # this button's tooltip    #LANG
            "Private",         # tooltip private info
            iconw,             # icon widget
            self.add_action,    # signal
            app_win.curPA)   # rank of open object

        # Create adding after selected element button
        iconw = gtk.Image() # icon widget
        iconw.set_from_file("../img/add.xpm")
        addPlus_button = self.toolbar.append_item(
            "Add after",           # button label        #LANG
            "Add next element", # this button's tooltip    #LANG
            "Private",         # tooltip private info
            iconw,             # icon widget
            self.add_next,0) # signal

        # Create adding detail element button
        iconw = gtk.Image() # icon widget
        iconw.set_from_file("../img/add2.xpm")
        addDetail_button = self.toolbar.append_item(
            "Detail",           # button label    #LANG
            "Add a detail element", # this button's tooltip    #LANG
            "Private",         # tooltip private info
            iconw,             # icon widget
            self.add_detail,0) # signal

        # Create delete element button
        iconw = gtk.Image() # icon widget
        iconw.set_from_file("../img/suppr.xpm")
        suppr_button = self.toolbar.append_item(
            "Delete",           # button label    #LANG
            "Delete selected element", # this button's tooltip    #LANG
            "Private",         # tooltip private info
            iconw,             # icon widget
            self.suppr_node) # signal
        self.toolbar.append_space() # ajout d'un espace après le bouton

#        # radio button...
#        iconw = gtk.Image() # icon widget
#        iconw.set_from_file("gtk.xpm")
#        button1 = self.toolbar.append_element(
#            gtk.TOOLBAR_CHILD_RADIOBUTTON, # element type
#            None,                          # widget
#            "Radio 1",                        # label
#            "Premier bouton radio",       # tooltip
#            "Private",                     # tooltip private string
#            iconw,                         # icon
#            self.radio_event,              # signal
#            self.toolbar)                       # data for signal
#        self.button1 = button1

#        # boutons radio suivant
#        iconw = gtk.Image() # icon widget
#        iconw.set_from_file("gtk.xpm")
#        button2 = self.toolbar.append_element(
#            gtk.TOOLBAR_CHILD_RADIOBUTTON,
#            button1,
#            "Radio 2",
#            "Deuxième bouton radio",
#            "Private",
#            iconw,
#            self.radio_event,
#            self.toolbar)
#        self.toolbar.append_space()
#        self.button2 = button2

#        button1.set_active(True)

#        # bouton on/off
#        iconw = gtk.Image() # icon widget
#        iconw.set_from_file("gtk.xpm")
#        buttonOnOff = self.toolbar.append_element(
#            gtk.TOOLBAR_CHILD_TOGGLEBUTTON,
#            None,
#            "Bascule",
#            "Bouton ON/OFF",
#            "Private",
#            iconw,
#            self.toggle_event,
#            self.toolbar)
#        self.toolbar.append_space()
#        #toggle bouton à false par défaut            data = ""
#        #buttonOnOff.set_active(False)
        
#        buttonOnOff.connect("clicked", app_win.Status.push_item, app_win.Status.context_id,"on/off")  # test status bar

#        # pour intégrer un widget à une barre d'outils, il suffit de l'ajouter avec l'infobulle appropriée
#        saisie = gtk.Entry()
#        saisie.set_max_length(5)
#        self.toolbar.append_widget(saisie,  "Recherche d'un ID", "Private")
#        saisie.connect("activate",self.select_ID,saisie)

#        # la création ne s'est pas faite dans la boîte à outil, il faut donc l'afficher séparément
#        saisie.show()

        # affichage du tout.
        self.toolbar.show()
        self.handlebox.show()
        #dialog.show()

class InfoModel:
    """ Management of data to display """
    def __init__(self,fmodel):
        """ gtk.TreeStore definition and loading """
        # Dynamic TreeStore structure buiding
        self.modelCol=[]
        for col in range(fmodel.fieldsCount):
            self.modelCol.append(dicoType[fmodel.fieldsStruct[col][1]])
        self.tree_store = gtk.TreeStore(*self.modelCol)
        return
    def get_model(self):
        """ Get the model to connect with the view"""
        if self.tree_store:
            return self.tree_store 
        else:
            return None
        
class DisplayModel:
    """ Data display """
    def make_view( self, curpa=0 ):
        """ Building a view to display treeview """
        model = app_win.FileOpen[curpa].Store.tree_store
        fmodel = app_win.FileOpen[curpa]
#        self.view = gtk.TreeView( app_win.FileOpen[curpa].Store.get_model() )
        self.view = gtk.TreeView( model )
        self.renderer = []
        self.column = []
        #treeview renderer configuration
        for col in range(fmodel.fieldsCount):
            if fmodel.fieldsStruct[col][FLDNAT] == "str":   # if the renderer display is a string
                if fmodel.fieldsStruct[col][FLDTYP] == "str":
                    self.renderer.append(gtk.CellRendererText())
                elif fmodel.fieldsStruct[col][FLDTYP] == "date":
                    self.renderer.append(CellRendererDate(app_win.dico["date_format"]))
                elif fmodel.fieldsStruct[col][FLDTYP] == "combolist":
                    self.renderer.append(gtk.CellRendererCombo())
                    self.renderer[col].set_property('has-entry', False)     # use other value is not allowed 
                    self.renderer[col].set_property('text-column', 0)   #column in the data source model to get the strings from
                    chlist = fmodel.fieldsStruct[col][CHLIST]
#                    loadPA(fmodel, 3, chlist)
                    loadPA(curpa, 3, chlist)
                    combomodel = gtk.ListStore(str)
                    for itm in range(fmodel.choicelist[chlist][0]):
                        combomodel.append([fmodel.choicelist[chlist][itm+1]])
                    self.renderer[col].set_property('model', combomodel)
                if fmodel.fieldsStruct[col][FLDMOD] == "mod":   # if the field can be modified
                    self.renderer[col].set_property( 'editable', True )
                else:
                    self.renderer[col].set_property( 'editable', False )
            elif fmodel.fieldsStruct[col][FLDNAT] == "bool":    # if the renderer display is a boolean
                if fmodel.fieldsStruct[col][FLDTYP] == "check":
                    self.renderer.append(gtk.CellRendererToggle())
                if fmodel.fieldsStruct[col][FLDMOD] == "mod":
                    self.renderer[col].set_property( 'activatable', True )
                else:
                    self.renderer[col].set_property( 'activatable', False )

        for col in range(fmodel.fieldsCount):
            if fmodel.fieldsStruct[col][FLDNAT] == "str":   # if the renderer display is a string
                # connexion to the edition functiondata[fld+3]
                if fmodel.fieldsStruct[col][EDFCT] != "":
                    self.renderer[col].connect( 'edited', getattr(self, fmodel.fieldsStruct[col][EDFCT]), (model,col))
            elif fmodel.fieldsStruct[col][FLDNAT] == "bool":    # if the renderer display is a boolean
                self.renderer[col].connect( 'toggled', getattr(self, fmodel.fieldsStruct[col][EDFCT]), (model,col))

        # infomodel columns connexion to treeview columns.
        for col in range(fmodel.fieldsCount):
            if fmodel.fieldsStruct[col][FLDNAT] == "str":
                self.column.append(gtk.TreeViewColumn(fmodel.fieldsStruct[col][TT], self.renderer[col], text=col))
            elif fmodel.fieldsStruct[col][FLDNAT] == "bool":
                self.column.append(gtk.TreeViewColumn(fmodel.fieldsStruct[col][TT], self.renderer[col]))
                #Case à cocher rendue active
                self.column[col].add_attribute( self.renderer[col], "active", col)

            self.view.append_column( self.column[col] )
        
        # define hidden columns
        for col in range(fmodel.fieldsCount):
            if fmodel.fieldsStruct[col][VISIB] == 'False':
                self.column[col].set_visible(False)
           
        # Treeview Drag and drop set available to move items in the tree
        self.view.set_reorderable(True)
        return self.view

    def col_edited_cb( self, cell, path, new_text, data ):
        """Modification management (Connect new data in the treeview)."""
        #print "Changement de '%s' en '%s'" % (model[path][col], new_text)
        model,col = data
        model[path][col] = new_text
        return

    def col_date_edited_cb( self, cell, path, new_text, data ):
        """Date input management."""
        model,col = data
        if new_text == "0":
            model[path][col] = ""
        else:
            model[path][col] = new_text            
        return

    def col_toggled_cb( self, cell, path, data ):
        """Save swing of the checkbox..."""
        model,col = data
        model[path][col] = not model[path][col]
        return

    def col_edited_lb( self, cell, path, choix, data ):
        """Save item choice in the combobox."""
        model,col = data
        model[path][col] = choix
        return

class FileModel:
    def __init__(self):
        """ Structure """
        self.PAname = "<data structure name>"   # name of action plan
        self.PAFile = ""    # action plan file path
        self.fieldsCount = 0    # number of field
        self.fieldsStruct = []
        self.choicelist = {}
        self.newnode = []
        self.IDPA = ""      # action plan id (owner of actions)
        self.IDmin = 0      # lower id used
        self.IDmax = 0      # upper id used
        self.IDroof = 0     # upper authorized id
        self.Store = None
        self.Display = None
        self.idpos = 0      # id position in data structure

    def destroy_cb(self, *kw):
        """ Destroy callback for application closing """
        writeIni(app_win.FileOpen[app_win.curPA],app_win.initFile,app_win.dico)
        gtk.main_quit()
        return

    def run(self):
        """ called for run GTK event manager """
        gtk.main()
        return    

def apply_ini():
    structOK,ErrMess =  structPAControl(app_win.initFile,"ini") # verify init file structure
    if structOK:
        loadIni(app_win.initFile, app_win.dico)
        app_win.set_title(app_win.dico["appliname"])
    else:
        buf = "File 'pascal.ini' : " + ErrMess  #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)

def loadPA(filepos, loadstep, section=None):
    fmodel=app_win.FileOpen[filepos]
    ctrlOK,ErrMess = structPAControl(fmodel.PAFile)
    if ctrlOK == False:
        buf = "Format control : error message : %s" % ErrMess    #LANG
        print buf
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
    
    if ctrlOK == True:
        Config = ConfigParser.ConfigParser()
        Config.read(fmodel.PAFile)
#        if Config.has_section(SEC_STRUCT) and Config.has_section(SEC_DATA) and Config.has_section(SEC_PARAMS):
        if True:
            # Read number of columns
            # Read each column structure
            # Read name of column
            #print Config.sections()    #Read section names
            #print Config.options(SEC_DATA)    #Read data section keys
            if loadstep == 1:   # load structure
                fmodel.PAname = Config.get(SEC_PARAMS,ITM_NAME)
                fmodel.IDPA = Config.get(SEC_PARAMS,ITM_IDPA)
                fmodel.IDmin = int(Config.get(SEC_PARAMS,ITM_IDMIN))
                fmodel.IDmax = int(Config.get(SEC_PARAMS,ITM_IDMAX))
                fmodel.IDroof = int(Config.get(SEC_PARAMS,ITM_IDROOF))
                fmodel.fieldsCount = int(Config.get(SEC_STRUCT,ITM_NBCOL))
                fmodel.idpos = int(Config.get(SEC_STRUCT,ITM_IDPOS))
                for fld in range(fmodel.fieldsCount):
                    fmodel.fieldsStruct.append(Config.get(SEC_STRUCT,"col"+str(fld)).split(";"))
                    # default new node content
                    if fmodel.fieldsStruct[fld][FLDNAT] == "str":
                        fmodel.newnode.append("")
                    elif fmodel.fieldsStruct[fld][FLDNAT] == "bool":
                        fmodel.newnode.append(False)
            if loadstep == 2:   #load data of nodes in the file info model
                for opt in Config.options(SEC_DATA):
                    dnode = Config.get(SEC_DATA, opt).split(";")
                    if dnode[MOTHERPOS] == "0":
#                        print "add action"
                        app_win.Barre.add_action(code=opt, data=dnode, curpa=app_win.maxPA-1)
                    else:
#                        print "add detail %s" % opt
                        app_win.Barre.add_detail(code=opt, data=dnode, curpa=app_win.maxPA-1)
            if loadstep == 3:   #load other data
                if Config.has_section(section) == False:
                    return None
                valuecount = int(Config.get(section,ITM_COUNT))
                if valuecount > 0:
                    fmodel.choicelist[section] = [valuecount]
                for itm in range(valuecount):
                    fmodel.choicelist[section].append(Config.get(section,"item"+str(itm+1)))
        else :
            for s in [SEC_STRUCT,SEC_DATA,SEC_PARAMS]:
                if Config.has_section(s) == False:
                    print "%s section missing" % s  #LANG

def saveBranch(model, fmodel, tvnode, Config):
    """Branch of the treewiew saving function"""
    while tvnode :
        #save current node
        dnode=[]
        for col in range(fmodel.fieldsCount):
            if col == 0:
                # 1st data = mother's ID
                mother = model.iter_parent(tvnode)
                if mother:
                    dnode.append(str(model.get(mother, col)[0]))
                else:
                    dnode.append(str(0))
                # 2nd data : sort order (not used)
                dnode.append(str(0))
            dnode.append(str(model.get(tvnode, col)[0]))
        data = ";".join(dnode)
        #print data
        Config.set(SEC_DATA, str(model.get(tvnode, 0)[0]), data)
        #save the treeview branch
        result = saveBranch(model, fmodel, model.iter_children(tvnode), Config)
        #if result: return result
        tvnode = model.iter_next(tvnode)
    return None

def savePA(model, fmodel, fPA, fPADest=None, saveData=True):
        app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
        print "fPA :"
        print fPA
        if fPADest == None:
            fPADest = fPA
        tvnode = []
        Config = ConfigParser.ConfigParser()
        rdf = Config.read(fPA)
        if rdf == []:
            buf = fPA + " can't be reloaded"    #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            print buf
            # data in memory should be saveas here...
            #
            #
            return
        if Config.has_section(SEC_STRUCT) and Config.has_section(SEC_DATA) and Config.has_section(SEC_PARAMS):
            #reset Config structure
            for opt in Config.options(SEC_STRUCT):
                Config.remove_option(SEC_STRUCT, opt)
            #reset Config data
            for opt in Config.options(SEC_DATA):
                Config.remove_option(SEC_DATA, opt)
        
        #save instance parameters
        Config.set(SEC_PARAMS, ITM_NAME, fmodel.PAname)
        Config.set(SEC_PARAMS, ITM_IDPA, fmodel.IDPA)
        Config.set(SEC_PARAMS, ITM_IDMIN, fmodel.IDmin)
        Config.set(SEC_PARAMS, ITM_IDMAX, fmodel.IDmax)
        Config.set(SEC_PARAMS, ITM_IDROOF, fmodel.IDroof)
        
        #save structure
        Config.set(SEC_STRUCT, ITM_NBCOL, fmodel.fieldsCount)
        Config.set(SEC_STRUCT, ITM_IDPOS, fmodel.idpos)

        lstc = len(fmodel.choicelist)
        #RHE case of more than one choicelist (in settings...............................
        #=======================================================================
        # for k,v in fmodel.choicelist.items():
        #     Config.set(str(k), "itemcount", str(v[0]))
        #     for i in range(v[0]):
        #         Config.set(str(k), "item"+str(i+1), v[i+1])
        #=======================================================================

        for col in range(fmodel.fieldsCount):
            data = ";".join(fmodel.fieldsStruct[col])
            Config.set(SEC_STRUCT, "col"+str(col), data)

        #add nodes in Config
        if saveData == True:
            tvnode = model.get_iter_first()
            saveBranch(model, fmodel, tvnode, Config)
        else:
            Config.remove_section(SEC_DATA)
            Config.add_section(SEC_DATA)
            Config.set(SEC_PARAMS, ITM_IDMAX, fmodel.IDmin)
        fp = open(fPADest,"w")
        print "fPADest :"
        print fPADest
        Config.write(fp)
        fp.close()
        buf = "Save file as '%s'" % fPADest   #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
        
        if fPA != fPADest:
            # close starting plan
            simplyclose(None, confirm=False)
            # reload saved plan
            print "Loading %s" % fPADest  #LANG
            fct_open(None, "Import", fPADest)
            pass

def save(widget, event=None):
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    if app_win.curPA <0 :
        buf = "There is no file to save"   #LANG
    else :
        buf = "Saving %s" % app_win.FileOpen[app_win.curPA].PAFile   #LANG
        savePA(app_win.FileOpen[app_win.curPA].Store.tree_store, app_win.FileOpen[app_win.curPA], app_win.FileOpen[app_win.curPA].PAFile)
    print buf
    app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)

def saveas(widget, event=None, saveData=True):
    """Save plan as .pa"""
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)
    if app_win.curPA <0 :
        buf = "There is no file to save"   #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
        return True
    file_dialog = gtk.FileChooserDialog(("Enregistrer sous..."), app_win, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    file_dialog.set_default_response(gtk.RESPONSE_OK)
    filter = gtk.FileFilter()
    filter.add_mime_type("pascal")
    filter.add_pattern("*.pa")
    file_dialog.add_filter(filter)
    file_dialog.set_filename(app_win.FileOpen[app_win.curPA].PAFile)
    
    response = file_dialog.run()
    if response == gtk.RESPONSE_OK:
        new_name = file_dialog.get_filename()
        # verify target file is not open
        for i in range(app_win.maxPA):
            if app_win.curPA != i and app_win.FileOpen[i].PAFile == new_name:
                print "Saving not allowed : file %s is already open" % new_name   #LANG
                file_dialog.destroy()
                return False
        print "Saving %s" % new_name     #LANG
        savePA(app_win.FileOpen[app_win.curPA].Store.tree_store, app_win.FileOpen[app_win.curPA], app_win.FileOpen[app_win.curPA].PAFile, new_name, saveData)
    file_dialog.destroy()
    return True
    
def saveandclose(widget, event=None):
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    app_win.curPA = app_win.notebook.get_current_page()
    if app_win.curPA <0 :
        buf = "There is no file to save"   #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
        return True
    savePA(app_win.FileOpen[app_win.curPA].Store.tree_store, app_win.FileOpen[app_win.curPA], app_win.FileOpen[app_win.curPA].PAFile)
    if app_win.maxPA ==0:
        writeIni(app_win.FileOpen[0], app_win.initFile, app_win.dico)
    del app_win.FileOpen[app_win.curPA]
    app_win.maxPA -=1
    app_win.notebook.remove_page(app_win.curPA)
    app_win.curPA = app_win.notebook.get_current_page()

def simplyclose(widget, event=None, confirm=True):
    #confirm intent to close without saving data
    app_win.Status.pop_item(app_win.Status.status_bar,app_win.Status.context_id)    #empty status stack
    if app_win.curPA <0 :
        buf = "There is no file to close"   #LANG
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
        return True
    response = gtk.RESPONSE_OK
    if confirm == True:
        label = gtk.Label("Do you really want to close this plan without saving ?")  #LANG
        confirm_dialog = gtk.Dialog(title="Confirmation", flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))   #LANG
        label.show()
        response = confirm_dialog.run()
    if response == gtk.RESPONSE_OK:
        app_win.curPA = app_win.notebook.get_current_page()
        if app_win.maxPA ==0:
            writeIni(app_win.FileOpen[0], app_win.initFile, app_win.dico)
        del app_win.FileOpen[app_win.curPA]
        app_win.maxPA -=1
        app_win.notebook.remove_page(app_win.curPA)
        app_win.curPA = app_win.notebook.get_current_page()
    if confirm == True:
        confirm_dialog.destroy()
    
def change_pa(self, page, page_num):
    """Store current PA """
    #print "initial sheet : %s" % app_win.notebook.get_current_page()
    #print "new sheet : %s" % page_num
    app_win.curPA = page_num
    
def destroy_cb(self, *kw):
    """ Destroy callback for application closing """
    if app_win.maxPA > 0:
        writeIni(app_win.FileOpen[app_win.curPA],app_win.initFile, app_win.dico)
        #print "save settings in %s" % fichIni
    gtk.main_quit()
    return

def quit_dlg(widget, event=None):
    if app_win.curPA > -1:
        # there is a current open action plan file...
        writeIni(app_win.FileOpen[app_win.curPA],app_win.initFile, app_win.dico)
    else:
        #...or not
        writeIni(None,app_win.initFile, app_win.dico)        
    gtk.main_quit()

def TestDataStruct():
    print "Structure :"
    for nomodel in range(app_win.maxPA):
        print "File %s" % str(nomodel+1)    #LANG
        print app_win.FileOpen[nomodel].PAFile
        print app_win.FileOpen[nomodel].Store
        model = app_win.FileOpen[nomodel].Store.tree_store
        tvnode = model.iter_children(None)
        try:
            print model.get_value(tvnode, 0)
        except:
            pass
        
def OpenDataFile(datafile, filepos=0):
#    print "OpenDataFile %s" % datafile+" position "+str(filepos)
    ctrlOK,ErrMess = structPAControl(datafile)
    if ctrlOK == False:
        buf = "Format control : error message : %s" % ErrMess   #LANG
        print buf
        app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
        return False
    # control if the file is already open
    for i in range(app_win.maxPA):
        if datafile == app_win.FileOpen[i].PAFile:
            buf = "File %s is already open" % datafile    #LANG
            print buf
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)
            return False
    FModel = FileModel()
    app_win.FileOpen.append(FModel)             #add a data model to the application
    app_win.maxPA += 1
    app_win.FileOpen[filepos].PAFile = datafile
    loadPA(filepos,1)                           #load data structure stored in the chosen file
    app_win.FileOpen[filepos].Store = InfoModel(app_win.FileOpen[filepos])    #create the data store
    app_win.FileOpen[filepos].Display = DisplayModel()                          #create the display model
    loadPA(filepos,2)                           #load data stored in the chosen file
    return True
    
def DataToNotebook(filepos, ntbkpos):
    label = gtk.Label(app_win.FileOpen[filepos].PAname)
    app_win.FileOpen[filepos].scrolled_window = gtk.ScrolledWindow()
    app_win.FileOpen[filepos].scrolled_window.set_border_width(5)
        # the policy is one of POLICY AUTOMATIC, or POLICY_ALWAYS.
        # POLICY_AUTOMATIC will automatically decide whether you need scrollbars, whereas POLICY_ALWAYS will always leave the scrollbars there
        # The first one is the horizontal scrollbar, the second, the vertical.
    app_win.FileOpen[filepos].scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    app_win.FileOpen[filepos].scrolled_window.add_with_viewport(app_win.FileOpen[filepos].Display.make_view(filepos))
    tvnode = app_win.FileOpen[filepos].Store.tree_store.get_iter_first()
    
    app_win.FileOpen[filepos].scrolled_window.show()
#    notebook.insert_page(scrolled_window, label, ntbkpos) #third arg is position
    app_win.notebook.append_page(app_win.FileOpen[filepos].scrolled_window, label)
    app_win.show_all()
    app_win.curPA=filepos
    app_win.notebook.set_current_page(filepos)

def main():
    global app_win
    app_win = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
    app_win.connect("destroy", destroy_cb)
#    app_win.set_default_size(800, 600) 
    app_win.set_size_request(1000, 600) # window size at openning time
    try:
        app_win.set_icon_from_file(icon_file)
    except:
        print "icon not found at", icon_file    #LANG
    app_win.accel_group = gtk.AccelGroup() # shortcut group
    app_win.add_accel_group(app_win.accel_group)
    app_win.table = gtk.Table(1,4,False)    # menu + action buttons + notebook + statusbar
    app_win.add(app_win.table)

    app_win.initFile = INIFILE
    app_win.dico = {}
    app_win.curPA = -1  # current action plan index
    app_win.maxPA = 0   # number of action plan loaded
    app_win.FileOpen=[]
    app_win.dico["lastFile"] = ""
    app_win.dico["appliname"] = ""
    app_win.dico["version_appli"] = PASCAL_VER
    app_win.dico["version_param"] = PASCAL_PARAM_VER
    app_win.Status = StatusPA() #create statusbar

    apply_ini()  #load ini file and set configuration
    #===========================================================================
    # err,messerr = loadIni(app_win.initFile)
    # app_win.Status = StatusPA() #create statusbar
    # app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,messerr)
    # if err[0] == "E":
    #     return None # ini file hasn't been loaded
    # app_win.set_title(app_win.appliName)
    #===========================================================================
    #print "Last file opened : %s" % FModel.PAFile

    menu_toolbar_create() # create menu
    app_win.Barre = BarreOutil()  #create toolbar
    app_win.notebook = gtk.Notebook()
    app_win.notebook.set_tab_pos(gtk.POS_TOP) # POS_BOTTOM / POS_LEFT / POS_RIGHT
    app_win.notebook.connect("switch-page",change_pa)
    app_win.table.attach(app_win.notebook, 0,1,2,3)
    app_win.notebook.show()
    #notebook.insert_page(checkbutton, label, 1) #third arg is position
    #notebook.append / prepend (child,label)
    #notebook.remove(page_num)
    
    if app_win.dico["lastFile"] != "":
        if OpenDataFile(app_win.dico["lastFile"],0):  #data loading
            DataToNotebook(0, 0)
            buf = "Loading file '%s'" % app_win.FileOpen[0].PAFile   #LANG
            app_win.Status.push_item(app_win.Status.status_bar,app_win.Status.context_id,buf)

    app_win.table.attach(app_win.menu_main, 0,1,0,1,yoptions=gtk.FILL)
    app_win.table.attach(app_win.Barre.handlebox, 0,1,1,2,yoptions=gtk.FILL)
    app_win.table.attach(app_win.Status.vbox, 0,1,3,4,yoptions=gtk.FILL)

    app_win.show_all()

    # load gtk_main event manager
    gtk.main()

if __name__ == '__main__': main()
