# -*- coding: utf-8 -*-
#!/usr/bin/env python 
from pachooser import PaChooser
import gobject
import re       #regular expressions management

PASCAL_VER = "0.4.5"    #common version of PASCAL application except paparams.py (settings application)
INIFILE = "pascal.ini"
# data storage file sections
SEC_INI_OPEN = "LastOpenFile"   # last session data
SEC_INI_OTHER = "OtherParams"   # application common data
SEC_PARAMS = "params"           # counters and identification
SEC_STRUCT = "structure"        # data structure
SEC_DATA = "data"               # data records
# data storage file items
ITM_LASTFILE = "file01"         # last opened file
ITM_LASTSTRUCT = "struct01"     # last structure defined if not used yet
ITM_APPNAME = "appliname"       # application name ("action plan mamager" by default)
ITM_VER = "appliversion"        # PASCAL_VER
ITM_PARAMVER = "paramversion"   # PASCAL_PARAM_VER
ITM_NAME = "name"               # plan name
ITM_IDPA = "idpa"               # id of the plan (idpa + action id will identify an unique action
ITM_DTF = "dateformat"          # date format
ITM_IDMIN = "idmin"             # first id value
ITM_IDMAX = "idmax"             # higher id used
ITM_IDROOF = "idroof"           # limit of id for this action plan
ITM_NBCHXLST = "nbchoicelist"   # number of choicelist field
ITM_NBCOL = "nbcol"             # number of field
ITM_IDPOS = "idpos"             # position of the id field in field sequence
ITM_COUNT = "itemcount"         # number of available items in the choicelist
#configuration element position in configuration file ('structure' section)
TT = 0          # title = field name
FLDNAT = 1      # field nature (text or boolean)
FLDTYP = 2      # field type (text = text or date or choicelist )
FLDMOD = 3      # can be modify or not
VISIB = 4       # is visible or not
EDFCT = 5       # edit function called
CHLIST = 6      # name of the choicelist if the field is one

MOTHERPOS = 0   # what field refers to master record
ORDERPOS = 1    # what field refers to slave order
INTDATACOUNT = 2   #number of internal data = position of the first external data in data storage record

#Field natures
dicoType = {
            "bool": gobject.TYPE_BOOLEAN,
            "str": gobject.TYPE_STRING}

import ConfigParser #manage init files
from locale import getlocale, LC_TIME


def set_default_ini_config(Config, dicoIni=None):
    """Complete loaded data structure according to a default ini file.
       Default structure is a numbered list of title."""
    whereami = getlocale(LC_TIME)[0]
    dtf = '%Y-%m-%d'
    if whereami in ['fr_FR','fo_FO','aa_ER','aa_ER@saaho','aa_ET','af_ZA','am_ET','an_ES','ast_ES','ayc_PE','byn_ER','ca_ES','dv_MV','el_CY','el_GR','en_AG','en_AU','en_CA','en_GB','en_IE','en_IL','en_NG','en_NZ','en_SG','en_ZA','en_ZM','es_AR','es_BO','es_CL','es_CO','es_CR','es_CU','es_DO','es_EC','es_ES','es_GT','es_HN','es_MX','es_NI','es_PA','es_PE','es_PR','es_PY','es_SV','es_US','es_UY','es_VE','ff_SN','fr_BE','gd_GB','gez_ER','gez_ET','gl_ES','gv_GB','ha_NG','he_IL','ht_HT','id_ID','ig_NG','ik_CA','it_IT','ku_TR','kw_GB','lg_UG','lij_IT','ln_CD','mi_NZ','nhn_MX','niu_NU','niu_NZ','nr_ZA','nso_ZA','om_ET','om_KE','pa_PK','quz_PE','shs_CA','sid_ET','so_ET','so_KE','so_SO','ss_ZA','st_ZA','sw_KE','sw_TZ','ti_ER','ti_ET','tig_ER','tn_ZA','ts_ZA','unm_US','ur_PK','uz_UZ','uz_UZ@cyrillic','ve_ZA','vi_VN','wa_BE','wal_ET','xh_ZA','yi_US','yo_NG','zu_ZA','bi_TV','kab_DZ','mh_MH','son_ML']:
        dtf = '%d/%m/%y'
    if whereami in ['de_DE','sl_SI','sr_ME','sr_RS','sr_RS@latin','aa_DJ','az_AZ','be_BY','be_BY@latin','ber_DZ','ber_MA','br_FR','bs_BA','crh_UA','cv_RU','cy_GB','de_CH','de_IT','et_EE','fi_FI','fr_LU','fy_DE','ga_IE','hr_HR','hsb_DE','ia_FR','kk_KZ','ky_KG','lb_LU','li_BE','li_NL','mg_MG','mk_MK','nds_DE','nds_NL','oc_FR','os_RU','pl_PL','ro_RO','ru_RU','ru_UA','rw_RW','sk_SK','so_DJ','sv_FI','szl_PL','tg_TJ','tk_TM','tt_RU','tt_RU@iqtelif','uk_UA','wo_SN','myv_RU','myv_RU@cyrillic']:
        dtf = '%d.%m.%y'
    if whereami in ['fy_NL','nl_AW','nl_BE','nl_NL','pap_AN','pap_AW','pap_CW']:
        dtf = '%d-%m-%y'
    if whereami in ['pt_BR','pt_PT','tr_TR','da_DK']:
        dtf = '%d-%m-%Y'
    if whereami in ['fo_FO']:
        dtf = '%d/%m-%Y'
    if whereami in ['sl_SI']:
        dtf = '%d. %m. %Y'
    if whereami in ['fr_CH','fur_IT','it_CH','sc_IT']:
        dtf = '%d. %m. %y'
    if whereami in ['cs_CZ']:
        dtf = '%-d.%-m.%Y'
    if whereami in ['bg_BG']:
        dtf = '%e.%m.%Y'
    if whereami in ['as_IN']:
        dtf = '%e-%m-%Y'
    if whereami in ['en_US','bem_ZM','chr_US','fil_PH','hy_AM','iu_CA','ka_GE','tl_PH']:
        dtf = '%m/%d/%y'
    if whereami in ['sq_AL','csb_PL','de_AT','de_BE','de_LU','en_DK','eo','fr_CA','hu_HU','se_NO','si_LK','sv_SE','wae_CH']:
        dtf = '%Y-%m-%d'
    if whereami in ['ce_RU','lv_LV','lt_LT','mhr_RU','mn_MN','sgs_LT','ak_GH']:
        dtf = '%Y.%d.%m'
    if whereami in ['nb_NO','nn_NO']:
        dtf = '%d. %b %Y'
    if whereami in ['ar_AE','ar_BH','ar_DZ','ar_EG','ar_IQ','ar_JO','ar_KW','ar_LB','ar_LY','ar_MA','ar_OM','ar_QA','ar_SD','ar_SS','ar_SY','ar_TN','ar_YE']:
        dtf = '%d %b, %Y'
    if whereami in ['kl_GL']:
        dtf = '%d %b %Y'
    if whereami in ['te_IN']:
        dtf = '%B %d %A %Y'
    if whereami in ['ug_CN']:
        dtf = '%a، %d-%m-%Y'
    if whereami in ['eu_ES']:
        dtf = '%a, %Y.eko %bren %da'
    if whereami in ['mt_MT']:
        dtf = '%A, %d ta %b, %Y'
    if whereami in ['en_PH']:
        dtf = '%A, %d %B, %Y'
    if whereami in ['en_HK']:
        dtf = '%A, %B %d, %Y'
    if whereami in ['is_IS']:
        dtf = '%a %e.%b %Y'
    if whereami in ['ar_SA']:
        dtf = '%A %e %B %Y'
    if whereami in ['ta_IN','ta_LK']:
        dtf = '%A %d %B %Y'
    if whereami in ['anp_IN','ar_IN','bhb_IN','bho_IN','bn_BD','bn_IN','brx_IN','doi_IN','en_IN','gu_IN','hi_IN','hne_IN','kn_IN','kok_IN','ks_IN','ks_IN@devanagari','mag_IN','ml_IN','mni_IN','mr_IN','ms_MY','pa_IN','raj_IN','sa_IN','sat_IN','sd_IN','sd_IN@devanagari','tcy_IN','the_NP','ur_IN',]:
        dtf = '%A %d %b %Y'
    #print 'date format : %s' %dtf
    
    if Config.has_section(SEC_INI_OPEN) == False:
        Config.add_section(SEC_INI_OPEN)
    if Config.has_option(SEC_INI_OPEN, ITM_LASTFILE) == False:
        Config.set(SEC_INI_OPEN,ITM_LASTFILE,"")
    if Config.has_option(SEC_INI_OPEN, ITM_LASTSTRUCT) == False:
        Config.set(SEC_INI_OPEN,ITM_LASTSTRUCT,"")
    if Config.has_section(SEC_INI_OTHER) == False:
        Config.add_section(SEC_INI_OTHER)
    if Config.has_option(SEC_INI_OTHER, ITM_APPNAME) == False:
        Config.set(SEC_INI_OTHER,ITM_APPNAME,"Action Plan Manager")    #LANG
    if Config.has_option(SEC_INI_OTHER, ITM_VER) == False:
        Config.set(SEC_INI_OTHER,ITM_VER,PASCAL_VER)
    if Config.has_option(SEC_INI_OTHER, ITM_PARAMVER) == False:
        Config.set(SEC_INI_OTHER,ITM_PARAMVER,PASCAL_VER)
    if Config.has_option(SEC_INI_OTHER, ITM_DTF) == False:
        Config.set(SEC_INI_OTHER,ITM_DTF,'%d/%m/%y')    #LANG
    if dicoIni != None:
        dicoIni["lastFile"] = ""
        dicoIni["appliname"] = "Action Plan Manager"    #LANG
        dicoIni["version_appli"] = PASCAL_VER
        dicoIni["version_param"] = PASCAL_VER
        dicoIni["date_format"] = '%d/%m/%y'         #LANG
    if Config.has_section(SEC_PARAMS) == False:
        Config.add_section(SEC_PARAMS)
    if Config.has_option(SEC_PARAMS, ITM_NAME) == False:
        Config.set(SEC_PARAMS,ITM_NAME,"<Plan Name>")   #LANG
    if Config.has_option(SEC_PARAMS, ITM_IDPA) == False:
        Config.set(SEC_PARAMS,ITM_IDPA,"<Plan ID>")  #LANG
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
        Config.set(SEC_STRUCT,ITM_NBCOL,"2")
    if Config.has_option(SEC_STRUCT, ITM_IDPOS) == False:
        Config.set(SEC_STRUCT,ITM_IDPOS,"0")
    if Config.has_option(SEC_STRUCT, "col0") == False:
        Config.set(SEC_STRUCT,"col0","ID;str;str;cst;True;;")
    if Config.has_option(SEC_STRUCT, "col1") == False:
        Config.set(SEC_STRUCT,"col1","Title;str;str;cst;True;;")    #LANG
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
            rdf = []
            rdf = Config.read(initFile)   #Return list of successfully read files
            
        #Read the name of the file that must be loaded 
        dicoIni["lastFile"] = Config.get(SEC_INI_OPEN, ITM_LASTFILE)
        dicoIni["appliname"] = Config.get(SEC_INI_OTHER, ITM_APPNAME)
        dicoIni["version_appli"] = Config.get(SEC_INI_OTHER, ITM_VER)
        dicoIni["version_param"] = Config.get(SEC_INI_OTHER, ITM_PARAMVER)
        dicoIni["date_format"] = Config.get(SEC_INI_OTHER, ITM_DTF)

def writeIni(fmodel, initFile, dicoIni,struct = None):
    """Save configuration file"""
    fn =""
    if fmodel != None:
        fn = fmodel.PAFile
    else :
        fn = ""
    Config = ConfigParser.ConfigParser()
    cfgfile = open(initFile,'w')
    # ensure that there is at least a default loading
    set_default_ini_config(Config)
    
    if struct == None:
        #Record current data file
        Config.set(SEC_INI_OPEN,ITM_LASTFILE,fn)
        Config.set(SEC_INI_OTHER,ITM_APPNAME,"Action Plan Manager")    #LANG
        Config.set(SEC_INI_OTHER,ITM_VER,dicoIni["version_appli"])
        Config.set(SEC_INI_OTHER,ITM_PARAMVER,dicoIni["version_param"])
        Config.set(SEC_INI_OTHER,ITM_DTF,dicoIni["date_format"])
    if struct != None:
        #save or clear structure file name
        Config.set(SEC_INI_OPEN,ITM_LASTSTRUCT,struct)
        print "Saving structure name in ini file"   #LANG
    Config.write(cfgfile)
    cfgfile.close()

def paToCSV(fName):
    """Convert .pa data storage file to csv file."""
    datafile = open(fName,'r')
    data = datafile.read()
    datafile.close()
    data2 = data.replace('"',"'")
    data2 = data.replace(" = ",";")
    targetfile = open(PaChooser("saveas", "csv"),'w')
    targetfile.write(data2)
    targetfile.close()

def CSVTopa(fName):
    """Convert csv file to .pa file"""
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
    """Control .pa file structure. Return False if file format is not correct or file is not found"""
    if pafile == "":
        return False,"No file to load"  #LANG
    Config = ConfigParser.ConfigParser()
    rdf = []
    rdf = Config.read(pafile)   #Return list of successfully read files
    if rdf == []:
        if ext == "ini":
            return True, "Impossible to open '" + pafile + "'"  #LANG
        return False, "Impossible to open '" + pafile + "'"  #LANG

    for sec in [SEC_PARAMS,SEC_STRUCT,SEC_DATA]:
        if Config.has_section(sec) == False:
            return False,"Lack of section '" + sec + "' in the '" + pafile + "' file." #LANG
    for itm in [ITM_NAME,ITM_IDPA,ITM_IDMIN,ITM_IDMAX,ITM_IDROOF,ITM_NBCHXLST]:
        if Config.has_option(SEC_PARAMS, itm) == False:
            return False,"'params' section : '" + itm + "' data is missing"    #LANG
    for itm in [ITM_NBCOL,ITM_IDPOS]:
        if Config.has_option(SEC_STRUCT, itm) == False:
            return False,"'structure' section :  '" + itm + "' data is missing"    #LANG
    colCount = int(Config.get(SEC_STRUCT,ITM_NBCOL))
    for itm in range(colCount):
        if Config.has_option(SEC_STRUCT, "col"+str(itm)) == False:
            return False,"'structure' section : 'col" + str(itm) + "' data is missing"    #LANG
    if ext == "ini":
        for sec in [SEC_INI_OPEN,SEC_INI_OTHER]:
            if Config.has_section(sec) == False:
                return False,"'" + sec + "' section is missing" #LANG
        for itm in [ITM_LASTFILE,ITM_LASTSTRUCT]:
            if Config.has_option(SEC_INI_OPEN, itm) == False:
                return False,"'LastOpenFile' section : '" + itm + "' data is missing"    #LANG
        for itm in [ITM_APPNAME,ITM_VER,ITM_PARAMVER,ITM_DTF]:
            if Config.has_option(SEC_INI_OTHER, itm) == False:
                return False,"'OtherParams' section : '" + itm + "' data is missing"    #LANG
    # list structures control
    nblist = int(Config.get(SEC_PARAMS,ITM_NBCHXLST))
    for sec in range(nblist):
        if Config.has_section("list" + str(sec+1)) == False:
            return False,"'list" + str(sec+1) + "' section is missing"  #LANG
        for itm in [ITM_COUNT]:
            if Config.has_option("list" + str(sec+1), itm) == False:
                return False, "'list" + str(sec+1)+ "' section : '" + itm + "' data is missing"    #LANG
        nbitm = int(Config.get("list" + str(sec+1),ITM_COUNT))
        for itm in range(nbitm):
            if Config.has_option("list" + str(sec+1), "item"+str(itm+1)) == False:
                return False,"'list" + str(sec+1) + "' section : 'item" + str(itm+1) +"' data is missing"    #LANG

    idmin = int(Config.get(SEC_PARAMS,ITM_IDMIN))
    idmax = int(Config.get(SEC_PARAMS,ITM_IDMAX))
    idroof = int(Config.get(SEC_PARAMS,ITM_IDROOF))
    if idroof < idmax:
        return False,"'params' section : idmax value is upper than idroof value"  #LANG
    if idmax < idmin:
        return False,"'params' section : idmin value is upper than idmax value"     #LANG

    #data control
    # text or choicelist columns => no control needed
    fieldsStruct=[]
    for fld in range(colCount):
        fieldsStruct.append(Config.get(SEC_STRUCT,"col"+str(fld)).split(";"))
    for opt in Config.options(SEC_DATA):
        dnode = Config.get(SEC_DATA, opt).split(";")
        # number of data against number of columns
        if len(dnode) != colCount + INTDATACOUNT:
            return False,"'" + str(opt) + "' doesn't include "+ str(colCount) + " values!"  #LANG
        # boolean columns as True or False
#        if fieldsStruct[fld][FLDNAT] == "bool" and dnode[FLDNAT + INTDATACOUNT] != "True" and dnode[FLDNAT + INTDATACOUNT] != "False":
        for fld in range(colCount):
            if fieldsStruct[fld][FLDNAT] == "bool" :
                if dnode[INTDATACOUNT + fld] != "True" and dnode[INTDATACOUNT + fld] != "False":
#                     print "fld %s" % fld
#                     print dnode
#                     print dnode[INTDATACOUNT+fld]
                    return False,"'" + str(opt) + "' data doesn't include a boolean value in the field number "+ str(fld+1)     #LANG
            # date columns à empty or jj/mm/aa format
            if fieldsStruct[fld][FLDTYP] == "date" and dnode[INTDATACOUNT + fld] != "" and re.search(r"^\d\d/\d\d/\d\d$", dnode[INTDATACOUNT + fld]) == None:
                return False,"'" + str(opt) + "' data doesn't contain a date format value in the field number "+ str(fld+1) #LANG
            
    
    return True,""
    
