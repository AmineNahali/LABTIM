from models import *
import moviepy.editor as moviepy


def adminIndex():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        return render_template('indexAdmin.html')

def adminLogin():
    return render_template("loginAdmin.html")

def adminLoginVerify():
    data = request.get_json(force=True)
    usr = str(data["user"])
    pwd = str(data["pass"])
    if usr == "admin" and pwd == "admin@1998":
        session["administrateur"] = "administrateur"
        return redirect("/admin")
    else:
        return jsonify({"msg":"failure"})

def adminLogout():
    session["administrateur"] = None
    return redirect("/admin/login")

def adminUsers():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        return render_template('usersAdmin.html')

def adminNotification():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        return render_template('notificationsAdmin.html')

def adminPatients():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        return render_template('patientsAdmin.html')

def adminEtab():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        return render_template('etabAdmin.html')

def adminApps():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        return render_template('appsAdmin.html')

def adminListUsers():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        y=""
        countUsers = global_col_users.count_documents({})
        if countUsers == 0:
            return jsonify({"msg":"empty"})
        else:
            for x in global_col_users.find():
                y=y+x["Nom"]+" "+x["Prenom"]+"&&&"+x["Mail"]+"&&&"+x["App"]+"&&&"+x["Cin"]+"///"
            return jsonify({"msg":"success",'ls': y})

def adminDeleteUser():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        userToDelete = str(data["targetMail"])
        userToDeleteApp = str(data["targetApp"])
        existe = global_col_users.count_documents({"Mail":userToDelete,"App":userToDeleteApp})
        if existe == 1:
            global_col_users.delete_one({"Mail":userToDelete,"App":userToDeleteApp})
            #mettre a jour le total des utilisateurs (si l'application existe sur la bd cad n'a pas été supprimée):
            if global_col_apps.count_documents({"Nom_App":userToDeleteApp}) == 1:
                x = global_col_apps.find_one({"Nom_App":userToDeleteApp})
                total_old = int(str(x["Total_utilisateurs"]))
                jk = total_old - 1
                if jk < 0:
                    jk=0 
                global_col_apps.update_one({"Nom_App":userToDeleteApp},{"$set":{"Total_utilisateurs":str(jk)}})
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"failed"})

def adminInfoUser():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        userToFindInfo = str(data["target"])
        existe = global_col_users.count_documents({"Mail":userToFindInfo})
        if existe == 1:
            infoDig = global_col_users.find_one({"Mail":userToFindInfo})
            infoDig_nom = str(infoDig["Nom"]) 
            infoDig_prenom = str(infoDig["Prenom"])
            infoDig_cin = str(infoDig["Cin"])
            infoDig_tel = str(infoDig["Tel"])
            infoDig_mail = str(infoDig["Mail"])
            infoDig_spec = str(infoDig["Spec"])
            infoDig_etab = str(infoDig["Etab"])
            infoDig_app = str(infoDig["App"])
            infoDig_insc = str(infoDig["Date"])
            return jsonify({"msg":"success","usr_nom":infoDig_nom,"usr_prenom":infoDig_prenom,"usr_mail":infoDig_mail,"usr_tel":infoDig_tel,"usr_cin":infoDig_cin,"usr_spec":infoDig_spec,"usr_etab":infoDig_etab,"usr_app":infoDig_app,"usr_insc":infoDig_insc})
        else:
            return jsonify({"msg":"failed"})

def adminListApps():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        y=""
        
        nbApps = global_col_apps.count_documents({})
        if nbApps == 0:
            return jsonify({"n":"0"})
        else:
            for curs in global_col_apps.find():
                y = y + str(curs["Nom_App"]) + "&&&" + str(curs["Route_App"]) + "///"
            return jsonify({"n":str(nbApps),"l":str(y)})

def adminAppInfo():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        identifiant = str(data["identifiant"])
        infApp = global_col_apps.find_one({"Nom_App":identifiant})
        
        conf_nomApp = str(infApp["Nom_App"])
        conf_routeApp = str(infApp["Route_App"])
        conf_ipApp  = str(infApp["IP"])
        conf_portApp  = str(infApp["PORT"])
        conf_descApp  = str(infApp["Description_App"])
        conf_devApp   = str(infApp["Développeur"])
        conf_devcontactApp  = str(infApp["Contact_dev"])
        return jsonify({"msg":"success","conf_nomApp":conf_nomApp,"conf_routeApp":conf_routeApp,"conf_ipApp":conf_ipApp,"conf_portApp":conf_portApp,"conf_descApp":conf_descApp,"conf_devApp":conf_devApp,"conf_devcontactApp":conf_devcontactApp})

def adminImgApp(resImg):
    out =""
    for x in global_col_appsLogoExtension.find():
        if x["Application"] == resImg:
            out = str(resImg)+str(x["extension"])
    return send_file("./data/images/"+out)

def adminAddApp():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        input_name = str(data["input_name"])
        input_route = str(data["input_route"])
        input_ip = str(data["input_ip"])
        input_port = str(data["input_port"])
        input_description = str(data["input_description"])
        input_dev = str(data["input_dev"])
        input_devcontact = str(data["input_devcontact"])

        ex = global_col_apps.count_documents({"Nom_App":input_name})
        if ex == 0:
            global_col_apps.insert_one({"Nom_App":input_name,"Route_App":input_route,"IP":input_ip,"PORT":input_port,"Description_App":input_description,"Développeur":input_dev,"Contact_dev":input_devcontact,"Total_utilisateurs":"0","Total_patients":"0"})
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"duplicate"})

def adminUploadLogo(logoName):
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        file = request.files['file']
        fbase = str(file.filename)
        filename, file_extension = os.path.splitext("/"+fbase)
        newF = str(logoName) + str(file_extension)
        checker = global_col_appsLogoExtension.count_documents({"Application":logoName})
        if checker == 0:
            global_col_appsLogoExtension.insert_one({"Application":logoName,"extension":str(file_extension)})
        else:
            global_col_appsLogoExtension.delete_one({"Application":logoName,"extension":str(file_extension)})
            global_col_appsLogoExtension.insert_one({"Application":logoName,"extension":str(file_extension)})
        file.save(os.path.join("./data/images/", newF))
        return jsonify({"msg":"success"})

def adminUploadDemo(demoName):
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        file = request.files['file'] 
        fbase = str(file.filename)
        filename, file_extension = os.path.splitext("/"+fbase)
        newF = str(demoName) + str(file_extension)
        checker = global_col_appsDemoExtension.count_documents({"Application":demoName})
        if checker == 0:
            global_col_appsDemoExtension.insert_one({"Application":demoName,"extension":str(file_extension)})
        else:
            global_col_appsDemoExtension.delete_one({"Application":demoName,"extension":str(file_extension)})
            global_col_appsDemoExtension.insert_one({"Application":demoName,"extension":str(file_extension)})
        file.save(os.path.join("./data/Demo/", newF))
        if file_extension == ".mp4":
            return jsonify({"msg":"success"})
        else:
            clip = moviepy.VideoFileClip(os.path.join("./data/Demo/", newF))
            clip.write_videofile(os.path.join("./data/Demo/",str(demoName) +".mp4"))
            return jsonify({"msg":"success"})

def adminSetApp():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        t = str(data["v0"])
        conf_nomApp = str(data["v1"])
        conf_routeApp = str(data["v2"])
        conf_ipApp = str(data["v3"])
        conf_portApp = str(data["v4"])
        conf_descApp = str(data["v5"])
        conf_devApp = str(data["v6"])
        conf_devcontactApp = str(data["v7"])
        
        chck = global_col_apps.count_documents({"Nom_App":str(t)})
        if chck == 1:
            filterConf = {"Nom_App":str(t)}
            newvalues = { "$set": {"Nom_App":conf_nomApp,"Route_App":conf_routeApp,"IP":conf_ipApp,"PORT":conf_portApp,"Description_App":conf_descApp,"Développeur":conf_devApp,"Contact_dev":conf_devcontactApp} }
            global_col_apps.update_one(filterConf,newvalues)
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"failure"})

def adminDestroyApp():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        dead = str(data["target"])
        counterDel = global_col_apps.count_documents({"Nom_App":dead})
        if counterDel == 0:
            return jsonify({"msg":"success"})
        else:
            global_col_apps.delete_one({"Nom_App":dead})
            global_col_appsDemoExtension.delete_one({"Application":dead})
            global_col_appsDemoExtension.delete_one({"Application":dead})
            return jsonify({"msg":"success"})

def adminLoadNotifs():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        sum = ""
        testNotifs = global_col_notifications.count_documents({})
        if testNotifs == 0:
            return jsonify({"msg":"empty","totNotifs":str(testNotifs)})
        else:
            for x in global_col_notifications.find():
                val_Date = str(x["Date"])
                val_Code = str(x["Code"])
                val_App = str(x["App"])
                val_Nom = str(x["Nom"])
                val_Prenom = str(x["Prenom"])
                val_Cin = str(x["Cin"])
                val_Mail = str(x["Mail"])
                val_Tel = str(x["Tel"])
                val_Spec = str(x["Spec"])
                val_Etab = str(x["Etab"])
                sum = sum + val_Date + "&&&" + val_Code + "&&&" + val_App + "&&&" + val_Nom + "&&&" + val_Prenom + "&&&" + val_Cin + "&&&" + val_Mail + "&&&" + val_Tel + "&&&" + val_Spec + "&&&" + val_Etab +"///"
            return jsonify({"msg":"success","totNotifs":str(testNotifs),"ls":sum})

def adminDeleteNotif():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        delNotif = str(data["target"])
        testDelNotif = global_col_notifications.count_documents({"Code":delNotif})
        if testDelNotif == 0:
            return jsonify({"msg":"success"})
        else:
            global_col_notifications.delete_one({"Code":delNotif})
            return jsonify({"msg":"success"})

def adminAddUser():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        data = request.get_json(force=True)
        acceptNotif = str(data["target"])
        acceptDate = str(data["targetDate"])
        print(acceptNotif)
        print(acceptDate)
        testAccNotif = global_col_notifications.count_documents({"Code":acceptNotif})
        if testAccNotif == 0:
            print("1")
            return jsonify({"msg":"failure"})
        else:
            print("2")
            tmpUser = global_col_notifications.find_one({"Code":acceptNotif})
            __userDate = acceptDate
            __userCode = str(tmpUser["Code"])
            __userApp = str(tmpUser["App"])
            __userNom = str(tmpUser["Nom"])
            __userPrenom = str(tmpUser["Prenom"])
            __userCin = str(tmpUser["Cin"])
            __userMail = str(tmpUser["Mail"])
            __userTel = str(tmpUser["Tel"])
            __userSpec = str(tmpUser["Spec"])
            __userEtab = str(tmpUser["Etab"])
            __userMdp = tmpUser["MDP"]
            global_col_users.insert_one({"Date":__userDate,"Code":__userCode,"App":__userApp,"Nom":__userNom,"Prenom":__userPrenom,"Cin":__userCin,"Mail":__userMail,"Tel":__userTel,"Spec":__userSpec,"Etab":__userEtab,"MDP":__userMdp})
            global_col_notifications.delete_one({"Code":acceptNotif})
            #mettre a jour le total des utilisateurs:
            x = global_col_apps.find_one({"Nom_App":__userApp})
            total_old = int(str(x["Total_utilisateurs"]))
            total_old += 1
            global_col_apps.update_one({"Nom_App":__userApp},{"$set":{"Total_utilisateurs":str(total_old)}})
            return jsonify({"msg":"success"})

def adminGetUsersStats():
    if not session.get("administrateur"):
        return redirect("/admin/login")
    else:
        y=""
        loggedin = 0
        totalusrs = global_col_users.count_documents({})
        if global_col_apps.count_documents({}) == 0:
            return jsonify({"msg":"failure"})
        else:
            for gg in session:
                if session[gg] != None:
                    loggedin += 1
            for x in global_col_apps.find():
                y=y+str(x["Nom_App"])+"&&&"+str(x["Total_utilisateurs"])+"&&&"+str(x["Total_patients"])+"///"
            return jsonify({"msg":"success","stats":str(y),"loggedin":str(loggedin-1),"allusers":str(totalusrs)})