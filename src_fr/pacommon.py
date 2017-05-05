# -*- coding: utf-8 -*-
#!/usr/bin/env python 
from pachooser import PaChooser
import gobject
import re       #regular expressions managment

PASCAL_VER = "0.4.5"    #common version of PASCAL application except paparams.py (settings application)
INIFILE = "pascal.ini"
SEC_INI_OPEN = "LastOpenFile"
SEC_INI_OTHER = "OtherParams"
SEC_PARAMS = "params"
SEC_STRUCT = "structure"
SEC_DATA = "data"
ITM_LASTFILE = "file01"
ITM_LASTSTRUCT = "struct01"
ITM_APPNAME = "appliname"
ITM_VER = "appliversion"
ITM_PARAMVER = "paramversion"
ITM_NAME = "name"
ITM_IDPA = "idpa"
ITM_IDMIN = "idmin"
ITM_IDMAX = "idmax"
ITM_IDROOF = "idroof"
ITM_NBCHXLST = "nbchoicelist"
ITM_NBCOL = "nbcol"
ITM_IDPOS = "idpos"
ITM_COUNT = "itemcount"
#configuration element position in configuration file ('structure' section)
TT = 0
FLDNAT = 1
FLDTYP = 2
FLDMOD = 3
VISIB = 4
EDFCT = 5
CHLIST = 6

MOTHERPOS = 0
ORDERPOS = 1
INTDATACOUNT = 2   #number of internal data = position of the first external data

#Field natures
dicoType = {
            "bool": gobject.TYPE_BOOLEAN,
            "str": gobject.TYPE_STRING}

import ConfigParser #manage init files

def set_default_ini_config(Config, dicoIni=None):
    """Set data in memory equivalent to a default ini file loading"""
    if Config.has_section(SEC_INI_OPEN) == False:
        Config.add_section(SEC_INI_OPEN)
    if Config.has_option(SEC_INI_OPEN, ITM_LASTFILE) == False:
        Config.set(SEC_INI_OPEN,ITM_LASTFILE,"")
    if Config.has_option(SEC_INI_OPEN, ITM_LASTSTRUCT) == False:
        Config.set(SEC_INI_OPEN,ITM_LASTSTRUCT,"")
    if Config.has_section(SEC_INI_OTHER) == False:
        Config.add_section(SEC_INI_OTHER)
    if Config.has_option(SEC_INI_OTHER, ITM_APPNAME) == False:
        Config.set(SEC_INI_OTHER,ITM_APPNAME,"Gestion de plan d'action")
    if Config.has_option(SEC_INI_OTHER, ITM_VER) == False:
        Config.set(SEC_INI_OTHER,ITM_VER,PASCAL_VER)
    if Config.has_option(SEC_INI_OTHER, ITM_PARAMVER) == False:
        Config.set(SEC_INI_OTHER,ITM_PARAMVER,PASCAL_VER)
    if dicoIni != None:
        dicoIni["lastFile"] = ""
        dicoIni["appliname"] = "Gestion de plan d'action"
        dicoIni["version_appli"] = PASCAL_VER
        dicoIni["version_param"] = PASCAL_VER
    if Config.has_section(SEC_PARAMS) == False:
        Config.add_section(SEC_PARAMS)
    if Config.has_option(SEC_PARAMS, ITM_NAME) == False:
        Config.set(SEC_PARAMS,ITM_NAME,"<nom du plan>")
    if Config.has_option(SEC_PARAMS, ITM_IDPA) == False:
        Config.set(SEC_PARAMS,ITM_IDPA,"<ID du plan>")
    if Config.has_option(SEC_PARAMS, ITM_IDMAX) == False:
        Config.set(SEC_PARAMS,ITM_IDMAX,"1")
    if Config.has_option(SEC_PARAMS, ITM_IDMIN) == False:
        Config.set(SEC_PARAMS,ITM_IDMIN,"1")
    if Config.has_option(SEC_PARAMS, ITM_IDROOF) == False:
        Config.set(SEC_PARAMS,ITM_IDROOF,"999")
    if Config.has_option(SEC_PARAMS, ITM_NBCHXLST) == False:
        Config.set(SEC_PARAMS,ITM_NBCHXLST,"1")
    if Config.has_section(SEC_STRUCT) == False:
        Config.add_section(SEC_STRUCT)
    if Config.has_option(SEC_STRUCT, ITM_NBCOL) == False:
        Config.set(SEC_STRUCT,ITM_NBCOL,"1")
    if Config.has_option(SEC_STRUCT, ITM_IDPOS) == False:
        Config.set(SEC_STRUCT,ITM_IDPOS,"0")
    if Config.has_option(SEC_STRUCT, "col0") == False:
        Config.set(SEC_STRUCT,"col0","ID;str;str;cst;True;;")
    if Config.has_section("list1") == False:
        Config.add_section("list1")
    if Config.has_option("list1", ITM_COUNT) == False:
        Config.set("list1",ITM_COUNT,"1")
    if Config.has_option("list1", "item1") == False:
        Config.set("list1","item1","")
    if Config.has_section(SEC_DATA) == False:
        Config.add_section(SEC_DATA)

def loadIni(initFile, dicoIni):
        Config = ConfigParser.ConfigParser()
        rdf = []
        rdf = Config.read(initFile)   #Return list of successfully read files
        if rdf == []:
            # define a default ini file
            dicoIni = {}
            set_default_ini_config(Config, dicoIni)
            writeIni(None, INIFILE, dicoIni)
            
        #Read the name of the file that must be loaded 
        dicoIni["lastFile"] = Config.get(SEC_INI_OPEN, ITM_LASTFILE)
        dicoIni["appliname"] = Config.get(SEC_INI_OTHER, ITM_APPNAME)
        dicoIni["version_appli"] = Config.get(SEC_INI_OTHER, ITM_VER)
        dicoIni["version_param"] = Config.get(SEC_INI_OTHER, ITM_PARAMVER)

def writeIni(fmodel, initFile, dicoIni,struct = None):
    """Save configuration file"""
    fn =""
    if fmodel != None:
        fn = fmodel.PAFile
    Config = ConfigParser.ConfigParser()
    cfgfile = open(initFile,'w')
    # ensure that there is at least a default loading
    set_default_ini_config(Config)
    if struct == None:
        #Record current data file
#        print "Enregistrement de lastfile : %s" % fn
        Config.set(SEC_INI_OPEN,ITM_LASTFILE,fn)
        Config.set(SEC_INI_OTHER,ITM_APPNAME,"Gestion de plan d'action")
        Config.set(SEC_INI_OTHER,ITM_VER,dicoIni["version_appli"])
        Config.set(SEC_INI_OTHER,ITM_PARAMVER,dicoIni["version_param"])
    if struct != None:
        #save or clear structure file name
        Config.set(SEC_INI_OPEN,ITM_LASTSTRUCT,struct)
        print "Enregistrement/Effacement du nom de structure dans le fichier ini"
    Config.write(cfgfile)
    cfgfile.close()

def paToCSV(fName):
    datafile = open(fName,'r')
    data = datafile.read()
    datafile.close()
    data2 = data.replace('"',"'")
    data2 = data.replace(" = ",";")
    targetfile = open(PaChooser("saveas", "csv"),'w')
    targetfile.write(data2)
    targetfile.close()

def CSVTopa(fName):
    if fName == None :
        return None
    datafile = open(fName,'r')
    data = datafile.readlines()
    datafile.close()
    data2=[]
    for ln in range(len(data)):
        if data[ln][0] == "[":
            curSection = data[ln].replace(";","")
            data2.append(curSection)
        else:
            if curSection != "[data]\n":
                if data[ln][0:3] != "col":
                    #print "data[ln] %s" % data[ln]
                    if data[ln][0] == ";" :
                        data[ln] = "\n"
                    data2.append(data[ln].replace(";"," = ",1).replace(";",""))
                else:
                    data2a = []
                    data2a = data[ln].split(";")
                    data2b =";".join(data2a[0:8]).replace(";", " = ",1)+"\n"
                    data2.append(data2b)
            else:
                data2.append(data[ln].replace(";"," = ",1))
    data3 = "".join(data2)
    paNane = PaChooser("saveas", "pa")
    if paNane != "" and paNane != None:
        targetfile = open(paNane,'w')
        targetfile.write(data3)
        targetfile.close()
        return paNane

def structPAControl(pafile, ext="pa"):
    """Control PASCAL file structure. Return False if file format is not correct or file is not found"""
    if pafile == "":
        return False,"Pas de fichier à charger"
    Config = ConfigParser.ConfigParser()
    rdf = []
    rdf = Config.read(pafile)   #Return list of successfully read files
    if rdf == []:
        if ext == "ini":
            return True, "Le fichier '" + pafile + "' n'a pas pu être ouvert"
        return False, "Le fichier '" + pafile + "' n'a pas pu être ouvert"

    for sec in [SEC_PARAMS,SEC_STRUCT,SEC_DATA]:
        if Config.has_section(sec) == False:
            return False,"Absence de la section '" + sec + "' dans le fichier '" + pafile + "'"
    for itm in [ITM_NAME,ITM_IDPA,ITM_IDMIN,ITM_IDMAX,ITM_IDROOF,ITM_NBCHXLST]:
        if Config.has_option(SEC_PARAMS, itm) == False:
            return False,"Section 'params', absence de la donnée " + itm
    for itm in [ITM_NBCOL,ITM_IDPOS]:
        if Config.has_option(SEC_STRUCT, itm) == False:
            return False,"Section 'structure', absence de la donnée " + itm
    colCount = int(Config.get(SEC_STRUCT,ITM_NBCOL))
    for itm in range(colCount):
        if Config.has_option(SEC_STRUCT, "col"+str(itm)) == False:
            return False,"Section 'structure', absence de la donnée 'col" + str(itm) + "'"
    if ext == "ini":
        for sec in [SEC_INI_OPEN,SEC_INI_OTHER]:
            if Config.has_section(sec) == False:
                return False,"Absence de la section '" + sec + "'"
        for itm in [ITM_LASTFILE,ITM_LASTSTRUCT]:
            if Config.has_option(SEC_INI_OPEN, itm) == False:
                return False,"Section 'LastOpenFile', absence de la donnée " + itm
        for itm in [ITM_APPNAME,ITM_VER,ITM_PARAMVER]:
            if Config.has_option(SEC_INI_OTHER, itm) == False:
                return False,"Section 'OtherParams', absence de la donnée '" + itm + "'"
    # list structures control
    nblist = int(Config.get(SEC_PARAMS,ITM_NBCHXLST))
    for sec in range(nblist):
        if Config.has_section("list" + str(sec+1)) == False:
            return False,"Absence de la section 'list" + str(sec+1) + "'"
        for itm in [ITM_COUNT]:
            if Config.has_option("list" + str(sec+1), itm) == False:
                return False,"Section '" + "list" + str(sec+1)+ "', absence de la donnée '" + itm + "'"
        nbitm = int(Config.get("list" + str(sec+1),ITM_COUNT))
        for itm in range(nbitm):
            if Config.has_option("list" + str(sec+1), "item"+str(itm+1)) == False:
                return False,"Section 'list" + str(sec+1) + "', absence de la donnée 'item" + str(itm+1) +"'"

    idmin = int(Config.get(SEC_PARAMS,ITM_IDMIN))
    idmax = int(Config.get(SEC_PARAMS,ITM_IDMAX))
    idroof = int(Config.get(SEC_PARAMS,ITM_IDROOF))
    if idroof < idmax:
        return False,"Section 'params' : Valeur de idmax > idroof "
    if idmax < idmin:
        return False,"Section 'params' : Valeur de idmin > idmax "

    #data control
    # text or choicelist columns => no control needed
    fieldsStruct=[]
    for fld in range(colCount):
        fieldsStruct.append(Config.get(SEC_STRUCT,"col"+str(fld)).split(";"))
    for opt in Config.options(SEC_DATA):
        dnode = Config.get(SEC_DATA, opt).split(";")
        # number of data versus number of columns
        if len(dnode) != colCount + INTDATACOUNT:
            return False,"la donnée '" + str(opt) + "' ne contient pas "+ str(colCount) + " valeurs!"
        # boolean columns as True or False
#        if fieldsStruct[fld][FLDNAT] == "bool" and dnode[FLDNAT + INTDATACOUNT] != "True" and dnode[FLDNAT + INTDATACOUNT] != "False":
        for fld in range(colCount):
            if fieldsStruct[fld][FLDNAT] == "bool" :
                if dnode[INTDATACOUNT + fld] != "True" and dnode[INTDATACOUNT + fld] != "False":
                    print "fld %s" % fld
                    print dnode
                    print dnode[INTDATACOUNT+fld]
                    return False,"la donnée '" + str(opt) + "' ne contient pas une valeur booléenne pour le champ n°"+ str(fld+1)
            # date columns à empty or jj/mm/aa format
            if fieldsStruct[fld][FLDTYP] == "date" and dnode[INTDATACOUNT + fld] != "" and re.search(r"^\d\d/\d\d/\d\d$", dnode[INTDATACOUNT + fld]) == None:
                return False,"la donnée '" + str(opt) + "' ne contient pas une valeur correspondant à une date pour le champ n°"+ str(fld+1)
            
    
    return True,""
    
