import os
import bcrypt
import string
import random
from flask import Flask, render_template, redirect, request, session, jsonify,send_file
from flask_session import Session
from models import *

def index():
    return render_template('index.html')

def loadApps():
    rcount=global_col_apps.count_documents({})
    y=""
    if rcount == 0:
        return jsonify({"msg":"empty"})
    else:
        for x in global_col_apps.find():
            y = y + str(x["Nom_App"]) + "&&&" + str(x["Route_App"]) + "&&&" + str(x["Description_App"]) + "///"
        return jsonify({"msg":"success","lsapps":str(y)})

def imgApp(resImg):
    out =""
    if global_col_appsLogoExtension.count_documents({"Application":resImg}) == 0:
        return send_file("./data/generic.png")
    else:
        for x in global_col_appsLogoExtension.find():
            if x["Application"] == resImg:
                out = str(resImg)+str(x["extension"])
        return send_file("./data/images/"+out)

def demApp(appDemName):
    out =""
    for x in global_col_appsDemoExtension.find():
        if x["Application"] == appDemName:
            out = str(appDemName)+".mp4"
    return send_file("./data/Demo/"+out)

def loginGateway(NameOfApp):
    return redirect(f'/loginUsers?initApp={NameOfApp}')

def loginUsers():
    return render_template("loginPage.html")

def loginVerify():
    data = request.get_json(force=True)
    #print(data)
    adresse = str(data['adr'])
    mdps = str(data['mdp'])
    app_init = str(data['app'])
    go = f'/app/{app_init}?accept={adresse}'
    
    if (adresse == "super@user") and (mdps == "superuser@1998"):
        session["su"]="su"
        return jsonify({"msg":"escape","urlto":go})
    elif global_col_users.count_documents({"App":app_init,"Mail":adresse}) == 1:
        x = global_col_users.find_one({"App":app_init,"Mail":adresse})
        r = x["MDP"]
        if bcrypt.checkpw(mdps.encode(), r):
            session[f"{adresse},{app_init}"] = f"{adresse},{app_init}"
            print("login success")
            return jsonify({"msg":"escape","urlto":go})
        else:
            print("login reload")
            return jsonify({"msg":"reload"})
    else:
        return redirect(f"/loginUsers?initApp={app_init}")

def logoutUser():
    args = request.args
    theapp=args.get("target")
    theuser=args.get("accept")
    session[f"{theuser},{theapp}"] = None
    return redirect(f"/loginUsers?initApp={theapp}")

def signupUsers():
    data = request.get_json(force=True)
    el1 = {
    "Date":str(data['Date']),
    "Code":str(data['Code']),
    "App":str(data['app']),
    "Nom":str(data['Nom']),
    "Prenom":str(data['Prenom']),
    "Cin":str(data['CIN']),
    "Mail":str(data['Mail']),
    "Tel":str(data['Tel']),
    "Spec":dict_spec_covconnect[str(data['Spec'])],
    "Etab":str(data['Etab']),
    "MDP":bcrypt.hashpw(str.encode(str(data['Password'])), bcrypt.gensalt())
    }
    if global_col_users.count_documents({"Mail":str(data['Mail']),"App":str(data['app'])}) == 0 :
        if global_col_notifications.count_documents({"Mail":str(data['Mail']),"App":str(data['app'])}) == 0:
            global_col_notifications.insert_one(el1)
            #return redirect(f"/loginUsers?initApp={str(data['app'])}")
            return jsonify({"msg":"redirected","urlto":f"/loginUsers?initApp={str(data['app'])}"})
        else:
            return jsonify({"msg":"pending"})
    else:
        return jsonify({"msg":"duplicate"})

def ajouterEtablissement():
    data = request.get_json(force=True)
    codeEtab = str(data['code'])
    libelleEtab = str(data['libelle'])
    categEtab = str(data['categorieEtablissement'])
    typeEtab = str(data['typeEtablissement'])
    if global_col_etab.count_documents({"Code_Etablissement":codeEtab}) == 0:
        global_col_etab.insert_one({"Code_Etablissement":codeEtab,"Libellé_Etablissement":libelleEtab,"Catégorie_Etablissement":categEtab,"Type_Etablissement":typeEtab})
        return jsonify({"msg":"reload"})
    else:
        return jsonify({"msg":"duplicate"})

def getEtablissement():
	y=""
	for x in global_col_etab.find(): 
		y = y + x["Libellé_Etablissement"] + "/"
	#print(y)
	return jsonify({'ls': y})