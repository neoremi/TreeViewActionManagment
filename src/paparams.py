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
pygtk.require('2.0')
import gtk
import gtk.gdk
from pachooser import PaChooser
import ConfigParser #manage init files
from pacommon import *   # include common functions
import datetime     # for date format testing

PASCAL_PARAM_VER = "0.4.5"

class ParamsTab:
    TARGETS = [
        ('MY_TREE_MODEL_ROW', gtk.TARGET_SAME_WIDGET, 0),
        ('text/plain', 0, 1),
        ('TEXT', 0, 2),
        ('STRING', 0, 3),
        ('STRING', 0, 4),
        ('STRING', 0, 5),
        ('STRING', 0, 6),
        ('STRING', 0, 7),
        ]

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        self.window.destroy()
        #gtk.main_quit()
        return False

#    def make_pb(self, tvcolumn, cell, model, iter):
#        stock = model.get_value(iter, 1)
#        pb = self.treeview.render_icon(stock, gtk.ICON_SIZE_MENU, None)
#        cell.set_property('pixbuf', pb)
#        return

    def chg_txt_simple( self, cell, path, new_text, data ):
        """Default edit function not used"""
        model,col = data
        model[path][col] = new_text
        return

    def chg_champ( self, cell, path, new_text, data ):
        model,col = data
        model[path][col] = new_text
        return

    def chg_nature( self, cell, path, new_text, data ):
        model,col = data
        model[path][col] = new_text
        self.def_list_types(path, model, new_text, True)
        model[path][EDFCT] = self.def_edit_function(model[path][FLDNAT], model[path][FLDTYP], model[path][FLDMOD])
        if new_text == "str" :
            self.changes[int(path)][2] = "str"
        if new_text == "bool" :
            self.changes[int(path)][2] = "check"
    
    def chg_type( self, cell, path, new_text, data ):
        model,col = data
        model[path][col] = new_text
        model[path][EDFCT] = self.def_edit_function(model[path][FLDNAT], model[path][FLDTYP], model[path][FLDMOD])
        self.changes[int(path)][2] = new_text
        #print self.changes
    
    def chg_modif( self, cell, path, data ):
        """Define function to be called for data modification"""
        model,col = data
        model[path][col] = not model[path][col]
        if col == 3:
            model[path][EDFCT] = self.def_edit_function(model[path][FLDNAT], model[path][FLDTYP], model[path][FLDMOD])
    
    def chg_list( self, cell, path, new_text, data ):
        model,col = data
        model[path][col] = new_text
    
    def def_list_types(self, path, model, naturefld, setdef):
        """Refresh list of item in the type choicelist according to nature of the field"""
        self.combomodel2.clear()
        if naturefld == 'str':
            self.combomodel2.append(["str"])
            self.combomodel2.append(["date"])
            self.combomodel2.append(["combolist"])
            if setdef == True:
                model[path][FLDTYP] = "str"
        elif naturefld == 'bool':
            self.combomodel2.append(["check"])
            if setdef == True:
                model[path][FLDTYP] = "check"
    
    def def_edit_function(self, naturefld, typefld, ismod):
        if ismod == False:
            return ""
        if naturefld == "str":
            if typefld == "str":
                return "col_edited_cb"
            elif typefld == "date":
                return "col_date_edited_cb"
            elif typefld == "combolist":
                return "col_edited_lb"
        elif naturefld == "bool":
            return "col_toggled_cb"
    
    def row_selection(self ,treev):
        """Function called when a field is selected in the view : type choicelist update"""
        trees=treev.get_selection()
        (model, siter) = trees.get_selected()
        path = model.get_path(siter)
        self.def_list_types(path, model, model[path][FLDNAT], False)
        self.combomodel3.clear()
        if model[path][FLDTYP] == "combolist":
            for k in range(self.nbchoicelist):
                self.combomodel3.append(["list"+str(k+1)])
#            for k,v in self.choicelist.items():
#                self.combomodel3.append([k])
        
    def load_pa_struct(self, model):
        if self.filename != None:
            rdf = []
            rdf = self.Config.read(self.filename)
            if rdf != []:
                if self.Config.has_section(SEC_STRUCT) and self.Config.has_section(SEC_PARAMS):
                    self.fieldsCount = int(self.Config.get(SEC_STRUCT,ITM_NBCOL))
                    self.nbchoicelist = int(self.Config.get(SEC_PARAMS,ITM_NBCHXLST))
                    self.PAName = self.Config.get(SEC_PARAMS,ITM_NAME)
                    self.idpa = self.Config.get(SEC_PARAMS,ITM_IDPA)
                    self.idmin = self.Config.get(SEC_PARAMS,ITM_IDMIN)
                    self.idmax = self.Config.get(SEC_PARAMS,ITM_IDMAX)
                    self.idroof = self.Config.get(SEC_PARAMS,ITM_IDROOF)
                    # test data existence
                    if self.Config.options(SEC_DATA) != []:
                        self.has_data = True
                        self.changes = []
                    for fld in range(self.fieldsCount):
                        self.fieldsStruct.append(self.Config.get(SEC_STRUCT,"col"+str(fld)).split(";"))
                        model.append([self.fieldsStruct[fld][TT], self.fieldsStruct[fld][FLDNAT], self.fieldsStruct[fld][FLDTYP], self.fieldsStruct[fld][FLDMOD] != 'cst', self.fieldsStruct[fld][VISIB] != 'False',self.fieldsStruct[fld][EDFCT],self.fieldsStruct[fld][CHLIST]])
                        self.changes.append([fld,self.fieldsStruct[fld][FLDTYP],self.fieldsStruct[fld][FLDTYP],""])
                else :
                    print "File structure is not compatible with the %s version of the application" % PASCAL_PARAM_VER  #LANG
            else:
                self.fieldsCount = 1
                self.add_field(self.liststore)
                self.nbchoicelist = 0
                self.PAName = "<title>"     #LANG
                self.idpa = "IDPAx"
                self.idmin = "1"
                self.idmax = "1"
                self.idroof = "999"
                # save a default ini file
                writeIni(None, INIFILE, self.dicoP)
        if self.filename == INIFILE:
            # modifier la structure
            if self.Config.has_section(SEC_INI_OPEN):
                self.Config.remove_section(SEC_INI_OPEN)
            if self.Config.has_section(SEC_INI_OTHER):
                self.Config.remove_section(SEC_INI_OTHER)
            # enregistrer sous...
        for lst in range(self.nbchoicelist):
            if self.Config.has_section("list"+str(lst+1)) == True:
                valuecount = int(self.Config.get("list"+str(lst+1),ITM_COUNT))
                if valuecount > 0:
                    self.choicelist["list"+str(lst+1)] = [valuecount]
                for itm in range(valuecount):
                    self.choicelist["list"+str(lst+1)].append(self.Config.get("list"+str(lst+1),"item"+str(itm+1)))
        
    def save_pa_struct(self, model, fname, newfile=True):
        print "save_pa_struct %s" % fname
        self.reload_lists(fname)
        if self.Config.has_section(SEC_PARAMS) == False:
            self.Config.add_section(SEC_PARAMS)
        self.Config.set(SEC_PARAMS,ITM_NAME,self.PAName)
        self.Config.set(SEC_PARAMS,ITM_IDPA,self.idpa)
        self.Config.set(SEC_PARAMS,ITM_IDMIN,self.idmin)
        self.Config.set(SEC_PARAMS,ITM_IDMAX,self.idmax)
        self.Config.set(SEC_PARAMS,ITM_IDROOF,self.idroof)
        self.Config.set(SEC_PARAMS,ITM_NBCHXLST,self.nbchoicelist)
        if self.Config.has_section(SEC_STRUCT) == False:
            self.Config.add_section(SEC_STRUCT)
        self.Config.set(SEC_STRUCT,ITM_NBCOL,str(self.fieldsCount)) 
        if self.Config.has_section(SEC_DATA) == False:
            self.Config.add_section(SEC_DATA)
        tvnode = model.get_iter_first()
        for fld in range(self.fieldsCount):
            dnode=[]
            for col in range(7):
                dnode.append(str(model.get(tvnode, col)[0]))
            if dnode[FLDMOD] == "True" :
                dnode[FLDMOD] = "mod"
            else:
                dnode[FLDMOD] = "cst"
            data = ";".join(dnode)
            self.Config.set(SEC_STRUCT, "col"+str(fld), data)
            if fld < self.fieldsCount:
                tvnode = model.iter_next(tvnode)
        # modify data
        if self.has_data == True:
            print "Data Existence..."   #LANG
            dnode = []
            for opt in self.Config.options(SEC_DATA): #for every data item
                dnode = self.Config.get(SEC_DATA, opt).split(";")
#                print "dnode = %s" % dnode
#                print "changes = %s" % self.changes
                dnode0 = []
                for i in range(len(dnode)): #copy initial data
                    dnode0.append(dnode[i])
                for fld in range(len(self.changes)):
                    if  self.changes[fld][3] == "-" :
                        pass
                    if  self.changes[fld][3] == "" :
                        dnode[int(self.changes[fld][0])+2] = dnode0[fld+2]
                        #print dnode
#                        print "changes[i] = %s" % self.changes[fld]

                        if self.changes[fld][1] != self.changes[fld][2]:
                            #print "converting data to %s" % self.changes[fld][2]    #LANG
                            if self.changes[fld][2] == "str":
                                if self.changes[fld][1] == "check":
                                    if dnode0[self.changes[fld][0]+2] == "False":
                                        dnode[fld+2] = "no"    #LANG
                                    else:
                                        dnode[fld+2] = "yes"    #LANG
                            elif self.changes[fld][2] == "date":
                                if self.changes[fld][1] != "check":
                                    # if data has a date format convert it or erase it
                                    try:
                                        datetime.datetime.strptime(dnode0[self.changes[fld][0]+2], '%d/%m/%y')  #LANG french date format!!!
                                        dnode[fld+2] = dnode0[self.changes[fld][0]+2]
                                    except:
                                        dnode[fld+2] = ""
                                else:
                                    dnode[fld+2] = ""   # data is lost
                                    
                                pass
                                #if not(dnode0[self.changes[fld][0]+2].isdate):  #error (use regex?)
                                #    dnode[fld+2] = None
                            elif self.changes[fld][2] == "combolist":
                                print "conversion to combolist not implemented" #LANG
                                tvnode = model.get_iter_first()
                                if fld > 0:
                                    for fld2 in range(fld):
                                        tvnode = model.iter_next(tvnode)
                                if model.get(tvnode, CHLIST) == ('',):  # if the field structure refers to a list
                                    pass
                                else:
                                    pass
                                # 0. test if the field was a choicelist before
                                # 1. collect values
                                # 2. build a new list
                                # 3. connect the list to the field
                                pass
                            elif self.changes[fld][2] == "check":
                                if dnode0[self.changes[fld][0]+2] == "" or dnode0[self.changes[fld][0]+2].upper() == "NO":  #LANG
                                    dnode[fld+2] = "False"
                                else :
                                    dnode[fld+2] = "True"
                    if  self.changes[fld][3] == "+" :
                        dnode.append("")
                        dnode[int(self.changes[fld][0])+2] = ""
                        if self.changes[fld][2] == "check":
                            dnode[int(self.changes[fld][0])+2] = "False"
                for i in range(len(self.changes)):
                    if  self.changes[i][3] == "-" :
                        del(dnode[len(dnode)-1])
                #####
                data = ";".join(dnode)
                self.Config.set(SEC_DATA, opt, data)

        #save data
        if newfile == True or fname == "":
            fname = PaChooser('saveas')
        if fname == None:
            return
        fp = open(fname,"w") # consider new file case
        self.Config.write(fp)
        fp.close()
        #save fname in ini file
        self.ConfigI = ConfigParser.ConfigParser()
        rdf = self.ConfigI.read(INIFILE)   #Return list of successfully read files
        if rdf != [] and self.ConfigI.has_section(SEC_INI_OPEN) == True:
            self.ConfigI.set(SEC_INI_OPEN,ITM_LASTSTRUCT,fname)
            cfgfile = open(INIFILE,'w')
            self.ConfigI.write(cfgfile)
            print "Save structure name in ini file" #LANG
            cfgfile.close()

    def save_params(self, widget=None, model=None, extcall=False, fname=None):
        """Save action plan settings"""
        tvnode = model.get_iter_first()
        while tvnode :
            if model.get(tvnode,FLDTYP,CHLIST) == ('combolist',''):
                label = gtk.Label("Structure include choicelist field that doesn't refer to an existing list of choices. Please modify your structure!") #LANG
                confirm_dialog = gtk.Dialog(title="Warning !", flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK))   #LANG
                confirm_dialog.set_default_response(gtk.RESPONSE_OK)
                confirm_dialog.vbox.pack_start(label, True, True, 5)
                label.show()
                response = confirm_dialog.run()
                if response == gtk.RESPONSE_OK:
                    confirm_dialog.destroy()
                    return
            tvnode = model.iter_next(tvnode)

        newfile = not(extcall) or fname == INIFILE
        self.save_pa_struct(model, self.filename, newfile) 
        self.window.destroy()
        
    def remove_a_field(self, model, tree):
        """Remove a field configuration in the model"""
        # get selected column
        TreeSelection = tree.get_selection()
        tm,tvnode = TreeSelection.get_selected()
        if tvnode:
            #delete selected column
            rgfld = int(model.get_path(tvnode)[0])
            for fld in range(rgfld):
                if self.changes[fld][3] == "-":
                    rgfld +=1
            self.changes[rgfld][3] = "-"
            for fld in range(len(self.changes)):
                if int(self.changes[fld][0]) > int(self.changes[rgfld][0]):
                    self.changes[fld][0] = int(self.changes[fld][0])-1
            self.changes[rgfld][0] = "9999"
            tvnode = model.remove(tvnode)
        
    def remove_field(self, widget=None,model=None,tree=None):
        """Removing field treatment"""
        if self.fieldsCount > 1:    # we can't remove the last field
            if self.has_data :
                label = gtk.Label("File includes data. Do you confirm colunm deletion ?") #LANG
                confirm_dialog = gtk.Dialog(title="Confirmation", flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))   #LANG
                confirm_dialog.set_default_response(gtk.RESPONSE_OK)
                confirm_dialog.vbox.pack_start(label, True, True, 5)
                label.show()
                response = confirm_dialog.run()
                if response == gtk.RESPONSE_OK:
                    self.remove_a_field(model, tree)
                    self.fieldsCount -= 1
                confirm_dialog.destroy()
            else:
                self.remove_a_field(model, tree)
                self.fieldsCount -= 1
        else:
            print "There must be at last one field" #LANG
            pass
        
    def add_field(self, model):
        """Add a field with default format in the model"""
        model.append(['<field>', 'str', 'str', False, True,'',''])  #LANG
    
    def add_new_field(self, widget=None,model=None):
        """Adding field treatment"""
        self.add_field(model)
        if self.has_data == True:
            print "Adding a field in a structure with data. A default field type is added" #LANG
            self.changes.append([self.fieldsCount,'str','str',"+"])
        self.fieldsCount += 1
        
    def cancel_param(self, widget=None):
        """Abort configuration treatment"""
        self.window.destroy()
        
    def chg_title(self, widget, entry):
        self.PAName = entry.get_text()
    
    def chg_idpa(self, widget, entry):
        self.idpa = entry.get_text()
    
    def chg_idmini(self, widget, entry):
        tmp = entry.get_text()
        entry.set_text(''.join([i for i in tmp if i in '0123456789']))
        tmp = entry.get_text()
        if tmp == "":
            entry.set_text(self.idmin)
        tmp = entry.get_text()
        val = int(tmp)
        if val > int(self.idmax) :
            entry.set_text(self.idmin)
        else:
            self.idmin = tmp
   
    def chg_idmaxi(self, widget, entry):
        tmp = entry.get_text()
        entry.set_text(''.join([i for i in tmp if i in '0123456789']))
        tmp = entry.get_text()
        if tmp == "":
            entry.set_text(self.idmax)
        tmp = entry.get_text()
        val = int(tmp)
        if val < int(self.idmin) or val > int(self.idroof) :
            entry.set_text(self.idmax)
        else:
            self.idmax = tmp
    
    def chg_idroof(self, widget, entry):
        tmp = entry.get_text()
        entry.set_text(''.join([i for i in tmp if i in '0123456789']))
        tmp = entry.get_text()
        if tmp == "":
            entry.set_text(self.idroof)
        tmp = entry.get_text()
        val = int(tmp)
        if val < int(self.idmax) :
            entry.set_text(self.idroof)
        else:
            self.idroof = tmp
    
    def add_list_choice(self, widget, fname):
        print "Add a choicelist"    #LANG
        button = gtk.Button("list"+str(self.nbchoicelist+1))
        button.connect("clicked", self.def_choice,self.nbchoicelist+1)
        self.nbchoicelist += 1
        button.show()
        self.vLstBoxlst.pack_start(button,False,False,0)
        # save a default new list in the file
        Config = ConfigParser.ConfigParser()
        Config.read(fname)
        Config.set(SEC_PARAMS,'nbchoicelist',self.nbchoicelist)
        Config.add_section("list"+str(self.nbchoicelist))
        Config.set("list"+str(self.nbchoicelist),'itemcount',"1")
        Config.set("list"+str(self.nbchoicelist),'item1',"")
        fp = open(fname,"w") 
        Config.write(fp)
        fp.close()

    def def_choice(self, widget, lst):
        ListTab(self.filename, "list"+str(lst), self.choicelist)
        self.reload_lists(self.filename)
    
    def reload_lists(self, fname):
        self.ConfigL.read(fname)
        nbl = int(self.ConfigL.get(SEC_PARAMS, ITM_NBCHXLST))
        self.Config.set(SEC_PARAMS, ITM_NBCHXLST, nbl)
        for nlst in range(nbl):
            nomlst = "list" + str(nlst+1)
            if self.Config.has_section(nomlst) == False:
                self.Config.add_section(nomlst)
            nbitm = int(self.ConfigL.get(nomlst, ITM_COUNT))
            self.Config.set(nomlst,'itemcount',nbitm)
            for lst in range(nbitm):
                self.Config.set(nomlst, "item"+str(lst+1), self.ConfigL.get(nomlst, "item"+str(lst+1))) 
        
    def drag_data_get_data(self, treeview, context, selection, target_id, etime):
        treeselection = treeview.get_selection()
        model, iter = treeselection.get_selected()
        self.dragpos = self.liststore.get_path(iter)[0]
        data = ""
        for col in range(6):
            data += str(model.get_value(iter, col))+";"
        data += model.get_value(iter, 6)
        selection.set(selection.target, 8, data)

    def drag_data_received_data(self, treeview, context, x, y, selection, info, etime):
        model = treeview.get_model()
        data = selection.data
        drop_info = treeview.get_dest_row_at_pos(x, y)
        datadrop = data.split(";")
        if datadrop[3] == 'False':
            datadrop[3] = False
        else:
            datadrop[3] = True
        if datadrop[4] == 'False':
            datadrop[4] = False
        else:
            datadrop[4] = True
        init = []
        #save old position
        for fld in range(self.fieldsCount):
            init.append(self.changes[fld])
        self.changes = []
        if drop_info:
            path, position = drop_info
            self.droppos = path[0]
            iterc = model.get_iter(path)
            data2 = model.get_value(iterc, 0)
            if position != gtk.TREE_VIEW_DROP_AFTER:
#            if (position == gtk.TREE_VIEW_DROP_BEFORE or position == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE):
                model.insert_before(iterc, datadrop)
            else:
                model.insert_after(iterc, datadrop)
                self.droppos +=1
            # calculate reordered positions
            if self.dragpos >= self.droppos :
                for fld in range(self.fieldsCount):
                    if  fld < self.droppos :
                        self.changes.append(init[fld])
                    if fld == self.droppos :
                        self.changes.append(init[self.dragpos])
                    if  fld > self.droppos and fld <= self.dragpos :
                        self.changes.append(init[fld - 1])
                    if  fld > self.droppos and fld > self.dragpos :
                        self.changes.append(init[fld])
            if self.dragpos < self.droppos :
                for fld in range(self.fieldsCount):
                    if  fld < self.dragpos :
                        self.changes.append(init[fld])
                    else :
                        if fld < self.droppos-1 :
                            self.changes.append(init[fld + 1])
                        if fld == self.droppos-1 :
                            self.changes.append(init[self.dragpos])
                        if  fld >= self.droppos :
                            self.changes.append(init[fld])
        else:
            model.append(datadrop)
            for fld in range(self.fieldsCount):
                if  fld < self.dragpos :
                    self.changes.append(init[fld])
                else :
                    if fld < self.fieldsCount-1 :
                        self.changes.append(init[fld + 1])
                    else:
                        self.changes.append(init[self.dragpos])
        if context.action == gtk.gdk.ACTION_MOVE:
            context.finish(True, True, etime)
        return

    def __init__(self,fname = None, extcall = False):
        #case 1 : call by PASCAL with a loaded current .pa file 
        #case 2 : call by PASCAL without a loaded current .pa file or new structure demand
        #case 3 : call by settings application with effective file choice
        #case 4 : call by settings application without effective file choice
        self.Config = ConfigParser.ConfigParser()
        self.ConfigL = ConfigParser.ConfigParser()
        self.fieldsStruct = []
        self.fieldsCount = 0
        self.choicelist = {}
        self.nbchoicelist = 0
        self.PAName = ""
        self.idpa = ""
        self.idmin = 1
        self.idmax = 1
        self.idroof = 999
        self.filename = fname
        self.dicoP = {}
        self.dicoP["version_param"] = PASCAL_PARAM_VER
        self.has_data = False
        self.changes = []
        self.dragpos = 0
        self.droppos = 0

        if extcall == False:
            self.filename = PaChooser() #open a file or not
        # if no file is selected ini file is a template
        if self.filename == None:
            self.filename = INIFILE
            
        # Create a new window
#        self.window = gtk.Dialog(title=u"Paramétrage des données", parent=None, flags=gtk.DIALOG_MODAL,
#                                  buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        self.window = gtk.Dialog(title=u"Data Settings", parent=None, flags=gtk.DIALOG_MODAL, buttons=None)   #LANG
        self.window.set_default_response(gtk.RESPONSE_OK)
        self.window.set_border_width(0)
        self.window.set_size_request(650, 400)

        self.window.connect("delete_event", self.delete_event)

        # create a liststore with up and down button, field label, nature, type, modification available,...
        self.liststore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, gobject.TYPE_STRING)
        # create the TreeView using liststore
        self.treeview = gtk.TreeView(self.liststore)
        
        #self.window.vbox.pack_start(self.treeview, True, True, 0)
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(5)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scrolled_window.add_with_viewport(self.treeview)
        self.treeview.show()

        # title edition
        label = gtk.Label("Title : ")       #LANG
        label.set_alignment(1,0)
        entrytitle = gtk.Entry()
        entrytitle.set_max_length(50)
#        entrytitle.connect("activate", self.chg_title, entrytitle)
        entrytitle.connect("changed", self.chg_title, entrytitle)
        # action plan id edition
        entryidpa = gtk.Entry()
        entryidpa.set_max_length(50)
        entryidpa.connect("changed", self.chg_idpa, entryidpa)
        table = gtk.Table(2, 4, False)
        table.attach(label, 0, 1, 0, 1)
        table.attach(entrytitle, 1, 2, 0, 1)
        label = gtk.Label("Plan Identifier : ")     #LANG
        label.set_alignment(1,0)
        table.attach(label, 0, 1, 1, 2)
        table.attach(entryidpa, 1, 2, 1, 2)
        label = gtk.Label("Minimum ID : ")         #LANG
        label.set_alignment(1,0)
        table.attach(label, 0, 1, 2, 3)
        entrymini = gtk.Entry()
        entrymini.set_max_length(6)
        entrymini.set_tooltip_text("Value that must be lower than maximum ID")     #LANG
        entrymini.connect("changed", self.chg_idmini, entrymini)
        table.attach(entrymini, 1, 2, 2, 3)
        label = gtk.Label("Maximum ID : ")          #LANG
        label.set_alignment(1,0)
        table.attach(label, 0, 1, 3, 4)
        entrymaxi = gtk.Entry()
        entrymaxi.set_max_length(6)
        entrymaxi.set_tooltip_text("Value that must be between Minimum ID and Roof ID") #LANG
        entrymaxi.connect("changed", self.chg_idmaxi, entrymaxi)
        table.attach(entrymaxi, 1, 2, 3, 4)
        label = gtk.Label("Roof ID : ")     #LANG
        label.set_alignment(1,0)
        table.attach(label, 0, 1, 4, 5)
        entryroof = gtk.Entry()
        entryroof.set_max_length(6)
        entryroof.set_tooltip_text("Value that must be higher than Maximum ID") #LANG
        entryroof.connect("changed", self.chg_idroof, entryroof)
        table.attach(entryroof, 1, 2, 4, 5)
        frame = gtk.Frame("Tools Settings")  #LANG
        frame.add(table)
        
        hboxgenandlists = gtk.HBox(False, 0)
        hboxgenandlists.pack_start(frame,False,False,5)
        frame = gtk.Frame("Lists")  #LANG
        hboxgenandlists.pack_start(frame,False,False,5)
        vLstBox = gtk.VBox(False,0)
        frame.add(vLstBox)
        vLstBoxbt = gtk.VBox(False,0)
        self.vLstBoxlst = gtk.VBox(False,0)
        vLstBox.pack_start(self.vLstBoxlst)
        vLstBox.pack_end(vLstBoxbt)
        entrytitle.show()
        entryidpa.show()
        hboxgenandlists.show()
        
        self.window.vbox.pack_start(hboxgenandlists, False, False, 0)  #first part of the window (general parameters)
        # The dialog window is created with a vbox packed into it.
        self.window.vbox.pack_start(self.scrolled_window, True, True, 0)   #second part of the window (field structure)
        self.scrolled_window.show()
        
#        self.load_pa_struct(self.liststore, self.filename)
        self.load_pa_struct(self.liststore)
        entrytitle.set_text(self.PAName)
        entryidpa.set_text(self.idpa)
        entrymini.set_text(str(self.idmin))
        entrymaxi.set_text(str(self.idmax))
        entryroof.set_text(str(self.idroof))

        # Add one button per choicelist
        for nblst in range(self.nbchoicelist):
            button = gtk.Button("list"+str(nblst+1))
#            button.connect("clicked", self.def_choice,nblst+1, self.filename)
            button.connect("clicked", self.def_choice,nblst+1)
            button.show()
            self.vLstBoxlst.pack_start(button,False,False,0)
        button = gtk.Button("Add")  #LANG
        button.connect("clicked", self.add_list_choice, self.filename)
        button.show()
        vLstBoxbt.pack_start(button,False,False,0)
            
        # create a CellRenderers to render the data
        self.renderer = []
        self.renderer.append(gtk.CellRendererText())    # edit name of the field

        self.renderer.append(gtk.CellRendererCombo())   # edit if field is string or boolean
        self.renderer[1].set_property('has-entry', False)     # use other value is not allowed 
        self.renderer[1].set_property('text-column', 0)   #column in the data source model to get the data
        combomodel1 = gtk.ListStore(str)
        combomodel1.append(["str"])
        combomodel1.append(["bool"])
        self.renderer[1].set_property('model', combomodel1)

        self.renderer.append(gtk.CellRendererCombo())   # edit type of field (simple string, date, choicelist,...
        self.renderer[2].set_property('has-entry', False)
        self.renderer[2].set_property('text-column', 0)
        self.combomodel2 = gtk.ListStore(str)
        #=======================================================================
        # self.combomodel2.append(["str"])
        # self.combomodel2.append(["date"])
        # self.combomodel2.append(["combolist"])
        # self.combomodel2.append(["check"])
        #=======================================================================
        self.renderer[2].set_property('model', self.combomodel2)
        self.renderer.append(gtk.CellRendererToggle())  # edit modificatable status
        self.renderer.append(gtk.CellRendererToggle())  # edit visible status
        self.renderer.append(gtk.CellRendererText())    # edit edit function name of the field
        self.renderer.append(gtk.CellRendererCombo())   # edit choicelist name
        self.renderer[6].set_property('has-entry', False)
        self.renderer[6].set_property('text-column', 0)
        self.combomodel3 = gtk.ListStore(str)
        self.renderer[6].set_property('model', self.combomodel3)
        #self.renderer.append(CellRendererDate())
        #self.renderer.append(gtk.CellRendererCombo())
        self.renderer[0].set_property( 'editable', True ) #field name modification
        self.renderer[1].set_property( 'editable', True )
        self.renderer[2].set_property( 'editable', True )
        self.renderer[3].set_property( 'activatable', True )
        self.renderer[4].set_property( 'activatable', True )
        self.renderer[5].set_property( 'editable', False )
        self.renderer[6].set_property( 'editable', True )
        
        self.renderer[0].connect( 'edited', getattr(self, 'chg_champ'), (self.liststore,0))
        self.renderer[1].connect( 'edited', getattr(self, 'chg_nature'), (self.liststore,1))
        self.renderer[2].connect( 'edited', getattr(self, 'chg_type'), (self.liststore,2))
        self.renderer[3].connect( 'toggled', getattr(self, 'chg_modif'), (self.liststore,3))
        self.renderer[4].connect( 'toggled', getattr(self, 'chg_modif'), (self.liststore,4))
        self.renderer[6].connect( 'edited', getattr(self, 'chg_list'), (self.liststore,6))
        self.column = []
        # create the TreeViewColumns to display the data
        self.column.append(gtk.TreeViewColumn('Field', self.renderer[0], text=0))   #LANG
        self.column.append(gtk.TreeViewColumn('Nature', self.renderer[1], text=1))  #LANG
        self.column.append(gtk.TreeViewColumn('Type', self.renderer[2], text=2))    #LANG
        self.column.append(gtk.TreeViewColumn('Modifiable', self.renderer[3]))      #LANG
        self.column[3].add_attribute( self.renderer[3], "active", 3)
        self.column.append(gtk.TreeViewColumn('Visible', self.renderer[4]))         #LANG
        self.column[4].add_attribute( self.renderer[4], "active", 4)
        self.column.append(gtk.TreeViewColumn("Edit Function", self.renderer[5], text=5))  #LANG
        self.column.append(gtk.TreeViewColumn('Choicelist', self.renderer[6], text=6))      #LANG

         # add columns to treeview
        self.treeview.append_column(self.column[0])
        self.treeview.append_column(self.column[1])
        self.treeview.append_column(self.column[2])
        self.treeview.append_column(self.column[3])
        self.treeview.append_column(self.column[4])
        self.treeview.append_column(self.column[5])
        self.treeview.append_column(self.column[6])

        self.treeview.set_search_column(0)   # make treeview searchable
        self.column[0].set_sort_column_id(0) # Allow sorting on the column
        self.treeview.set_reorderable(True)  # Allow drag and drop reordering of rows
        
        self.treeview.connect("cursor-changed", self.row_selection)
        #self.treeselection = self.treeview.get_selection()
        #self.treeselection.set_mode(gtk.SELECTION_SINGLE)
        #self.treeselection.set_select_function(self.row_selection)
        self.treeview.enable_model_drag_source( gtk.gdk.BUTTON1_MASK, self.TARGETS, gtk.gdk.ACTION_DEFAULT|gtk.gdk.ACTION_MOVE)
        self.treeview.enable_model_drag_dest(self.TARGETS, gtk.gdk.ACTION_DEFAULT)
        self.treeview.connect("drag_data_get", self.drag_data_get_data)
        self.treeview.connect("drag_data_received", self.drag_data_received_data)

        self.add_button = gtk.Button("Add")     #LANG
        self.add_button.connect("clicked", self.add_new_field,self.liststore)
        self.add_button.show()
        self.rem_button = gtk.Button("Erase")   #LANG
        self.rem_button.connect("clicked", self.remove_field,self.liststore,self.treeview)
        self.rem_button.show()
        self.cancel_button = gtk.Button("Cancel")   #LANG
        self.cancel_button.connect("clicked", self.cancel_param)
        self.cancel_button.show()
        self.save_button = gtk.Button("Save")   #LANG
        # direct save if we modify the structure of an existing file which is not pascal.ini
#        newfile = not(extcall) or fname == INIFILE
        self.save_button.connect("clicked", self.save_params,self.liststore, extcall, self.filename)
        self.save_button.show()

        self.btbox=gtk.HBox(False,0)
        self.btbox.pack_start(self.add_button,True,False,0)
        self.btbox.pack_start(self.rem_button,True,False,0)
        self.btbox.pack_start(self.cancel_button,True,False,0)
        self.btbox.pack_start(self.save_button,True,False,0)
        self.btbox.show()
#        self.window.vbox.add(self.btbox)
        self.window.vbox.pack_start(self.btbox,False,False,0)  # third part of the window (command buttons)

        self.window.show_all()

        response = self.window.run()

class ListTab:
    def __init__(self, fname, listname, choicelist):
        """Choicelist management dialog box"""
        self.wndList = gtk.Dialog(title=u"List : "+listname, parent=None, flags=gtk.DIALOG_MODAL, buttons=None)     #LANG
        self.wndList.set_border_width(0)
        self.wndList.set_size_request(300, 200)
        self.wndList.show_all()
        hbox = gtk.HBox(False, 5)
        self.wndList.vbox.pack_start(hbox,False,False,0)
        listlist = gtk.ListStore(str)
        Config = ConfigParser.ConfigParser()
        if fname != None:
            Config.read(fname)
            for itm in range(int(Config.get(listname,ITM_COUNT))):
                listlist.append([Config.get(listname,"item"+str(itm+1))])
        #=======================================================================
        # for itm in range(choicelist[listname][0]):
        #     listlist.append([choicelist[listname][itm+1]])
        #=======================================================================
        self.view = gtk.TreeView( listlist )
        self.view.set_reorderable(True)
        itemrenderer = gtk.CellRendererText()
        itemrenderer.connect( 'edited', self.item_edited, (listlist,0))
        itemrenderer.set_property( 'editable', True )

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(5)
        scrolled_window.set_size_request(50,200)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scrolled_window.add_with_viewport(self.view)
        tvcolumn = gtk.TreeViewColumn('Item')
        tvcolumn.pack_start(itemrenderer, True)
        tvcolumn.set_attributes(itemrenderer, text=0)
        self.view.append_column(tvcolumn)

        hbox.pack_start(scrolled_window)
        vboxbt = gtk.VBox(False,5)
        hbox.pack_start(vboxbt)
        button = gtk.Button("Add")      #LANG
        button.connect("clicked", self.add_item, listlist)
        button.show()
        vboxbt.pack_start(button,False,False,0)
        button = gtk.Button("Erase")    #LANG
        button.connect("clicked", self.remove_an_item,listlist,self.view)
        button.show()
        vboxbt.pack_start(button,False,False,0)
        button = gtk.Button("Save")  #LANG
        button.connect("clicked", self.save_list,listlist,self.view, fname, listname)
        button.show()
        vboxbt.pack_start(button,False,False,0)
        self.wndList.show_all()
        response = self.wndList.run()      # external call routine is stopped until this window is closed
    
    def delete_event(self, widget, event, data=None):
        self.wndList.destroy()
        #gtk.main_quit()
        return False

#    def make_pb(self, tvcolumn, cell, model, iter):
#        stock = model.get_value(iter, 1)
#        pb = self.treeview.render_icon(stock, gtk.ICON_SIZE_MENU, None)
#        cell.set_property('pixbuf', pb)
#        return

    def item_edited( self, cell, path, new_text, data ):
        """Edit function of an item."""
        model,col = data
        model[path][col] = new_text

    def add_item(self, widget, model):
        """Add a field with default format in the model"""
        model.append(['<choice>'])   #LANG
    
    def remove_an_item(self, widget, model, tree):
        """Remove an item in the model"""
        # get selected column
        TreeSelection = tree.get_selection()
        tm,tvnode = TreeSelection.get_selected()
        if tvnode:
            #delete selected column
            tvnode = model.remove(tvnode)
        
    def save_list(self, widget, model, tree, fname, listname):
        """Save choicelist structure"""
        dnode=[]
        nbitem = 0
        print "save list %s" % listname     #LANG
        print "...in %s " % fname           #LANG
        if fname != None :
            Config = ConfigParser.ConfigParser()
            Config.read(fname)
            # control section existence
            if Config.has_section(listname) == False:
                Config.add_section(listname)
            # for each item record a value
            nbitem = 0
            tvnode = model.get_iter_first()
            while tvnode :
                dnode.append(str(model.get(tvnode, 0)[0]))
                nbitem +=1
                tvnode = model.iter_next(tvnode)
            for it in range(nbitem):
                Config.set(listname,'item'+str(it+1),dnode[it])
            Config.set(listname,ITM_COUNT,nbitem)
        fp = open(fname,"w") # consider new file case
        Config.write(fp)
        fp.close()
        self.wndList.destroy()

class ParamsGlob:
    def __init__(self, extcall = False):
        """Application parameters management dialog box"""
        self.wndPGlob = gtk.Dialog(title=u"Application Settings", parent=None, flags=gtk.DIALOG_MODAL, buttons=None)    #LANG
        self.wndPGlob.set_border_width(0)
        self.wndPGlob.set_size_request(350, 80)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(0)
        scrolled_window.set_size_request(350,50)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.wndPGlob.vbox.pack_start(scrolled_window,False,False,0)

        table = gtk.Table(2, 2, False)
        # title edition
        label = gtk.Label("Application Name : ")    #LANG
        label.set_alignment(1,0)
        entrytitle = gtk.Entry()
        entrytitle.set_max_length(50)
        entrytitle.connect("changed", self.chg_appname, entrytitle)
        table.attach(label, 0, 1, 0, 1)
        table.attach(entrytitle, 1, 2, 0, 1)

        label = gtk.Label("Application Version : ") #LANG
        label.set_alignment(1,0)
        labelv = gtk.Label(PASCAL_VER)
        labelv.set_alignment(1,0)
        table.attach(label, 0, 1, 1, 2)
        table.attach(labelv, 1, 2, 1, 2)

        scrolled_window.add_with_viewport(table)

        hbt = gtk.HBox(False,0)
        scrolled_window.add_with_viewport(hbt)

        button = gtk.Button("Save")     #LANG
        button.connect("clicked", self.saveglob)
        button.show()
        hbt.pack_end(button,False,False,0)
        button = gtk.Button("Cancel")   #LANG
        button.connect("clicked", self.cancelglob)
        button.show()
        hbt.pack_end(button,False,False,0)
        self.wndPGlob.vbox.pack_start(hbt,False,False,0)
        self.wndPGlob.show_all()
        
        #data loading
        self.wndPGlob.dico = {}
        self.wndPGlob.dico["lastFile"] = ""
        self.wndPGlob.dico["appliName"] = ""
        loadIni(INIFILE, self.wndPGlob.dico)
        entrytitle.set_text(self.wndPGlob.dico["appliname"])
        response = self.wndPGlob.run()      # external call routine is stopped until this window is closed
        
            
    def saveglob(self, widget, extcall=False):
        """Save global parameters in ini file"""
        Config = ConfigParser.ConfigParser()
        if self.application_name =="":
            buf = "You have to choose an effective application name"   #LANG
            print buf
            self.application_name = "Action Plan Manager"    #LANG"
        rdf = Config.read(INIFILE)   #Return list of successfully read files
        if rdf != [] and Config.has_section(SEC_INI_OTHER) == True:
            print "new application name : %s" % self.application_name    #LANG
            Config.set(SEC_INI_OTHER,ITM_APPNAME,self.application_name)
            cfgfile = open(INIFILE,'w')
            Config.write(cfgfile)
            cfgfile.close()
        self.wndPGlob.destroy()
    
    def chg_appname(self, x, widget):
        """Change application name"""
        self.application_name = widget.get_text()
        
    def cancelglob(self, widget):
        self.wndPGlob.destroy()
    
    def delete_event(self, widget, event, data=None):
        self.wndPGlob.destroy()
        return False

def main():
    gtk.main()

if __name__ == "__main__":
    ParamsTab()
    main()
