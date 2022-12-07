from adminControllers import *
from visitorControllers import *
from mTLEConnectControllers import *
from covconnectControllers import *
from RDconnectControllers import *
from SEPconnectControllers import *
app = Flask(__name__)
uf = "./data/"
app.config["UPLOAD_FOLDER"] = uf
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

### ADMIN ROUTES ###
app.add_url_rule("/admin","adminIndex",adminIndex)
app.add_url_rule("/admin/login","adminLogin",adminLogin)
app.add_url_rule("/admin/login/verify","adminLoginVerify",adminLoginVerify,methods=["POST"])
app.add_url_rule("/admin/logout","adminLogout",adminLogout,methods=["POST"])
app.add_url_rule("/admin/users","adminUsers",adminUsers,methods=["GET"])
app.add_url_rule("/admin/notifications","adminNotification",adminNotification,methods=["GET"])
app.add_url_rule("/admin/patients","adminPatients",adminPatients,methods=["GET"])
app.add_url_rule("/admin/etab","adminEtab",adminEtab,methods=["GET"])
app.add_url_rule("/admin/apps","adminApps",adminApps,methods=["GET"])
app.add_url_rule("/admin/listUsers","adminListUsers",adminListUsers,methods=["POST"])
app.add_url_rule("/admin/deleteUser","adminDeleteUser",adminDeleteUser,methods=["POST"])
app.add_url_rule("/admin/infoUser","adminInfoUser",adminInfoUser,methods=['POST'])
app.add_url_rule("/admin/listApps","adminListApps",adminListApps,methods=['POST'])
app.add_url_rule("/admin/appInfo","adminAppInfo",adminAppInfo,methods=['POST'])
app.add_url_rule("/admin/appImg/<resImg>","adminImgApp",adminImgApp,methods=['GET'])
app.add_url_rule("/admin/addApp","adminAddApp",adminAddApp,methods=['POST'])
app.add_url_rule('/admin/uploadLogo/<logoName>',"adminUploadLogo",adminUploadLogo,methods=['POST'])
app.add_url_rule('/admin/uploadDemo/<demoName>',"adminUploadDemo",adminUploadDemo, methods=['POST'])
app.add_url_rule("/admin/appconfig","adminSetApp",adminSetApp,methods=['POST'])
app.add_url_rule("/admin/deleteApp","adminDestroyApp",adminDestroyApp,methods=['POST'])
app.add_url_rule("/admin/loadNotifs","adminLoadNotifs",adminLoadNotifs,methods=['POST'])
app.add_url_rule("/admin/deleteNotif","adminDeleteNotif",adminDeleteNotif,methods=['POST'])
app.add_url_rule("/admin/addUser","adminAddUser",adminAddUser,methods=['POST'])
app.add_url_rule("/admin/adminGetUsersStats","adminGetUsersStats",adminGetUsersStats,methods=['POST'])

### VISITOR ROUTES ###
app.add_url_rule("/","index",index)
app.add_url_rule("/index","index",index)
app.add_url_rule("/accueil","index",index)
app.add_url_rule("/loadApps","loadApps",loadApps,methods=["POST"])
app.add_url_rule("/imgApp/<resImg>","imgApp",imgApp)
app.add_url_rule("/demApp/<appDemName>","demApp",demApp)
app.add_url_rule("/loginGateway/<NameOfApp>","loginGateway",loginGateway)
app.add_url_rule("/loginUsers","loginUsers",loginUsers)
app.add_url_rule("/loginVerify","loginVerify",loginVerify,methods=["POST"])
app.add_url_rule("/signupUsers","signupUsers",signupUsers,methods=["POST"])
app.add_url_rule("/ajouterEtablissement","ajouterEtablissement",ajouterEtablissement, methods=['POST'])
app.add_url_rule("/getEtablissements","getEtablissement",getEtablissement, methods=['POST'])


# COVConnect ROUTES ###
app.add_url_rule("/app/COVConnect","covconnectApp",covconnectApp)
app.add_url_rule("/app/COVConnect/covconnectUserDetails","covconnectUserDetails",covconnectUserDetails,methods=["POST"])
app.add_url_rule("/app/COVConnect/covconnectLogOut","covconnectLogOut",covconnectLogOut,methods=["POST"])
app.add_url_rule("/app/COVConnect/covconnectAddPat","covconnectAddPat",covconnectAddPat,methods=["POST"])
app.add_url_rule("/app/COVConnect/covconnectDelPat","covconnectDelPat",covconnectDelPat,methods=["POST"])
app.add_url_rule("/app/COVConnect/listPat","covconnectlistPat",covconnectlistPat,methods=["POST"])
app.add_url_rule("/app/COVConnect/upload/<origin>","covconnectupload",covconnectupload,methods=["POST"])
app.add_url_rule("/app/COVConnect/generateThumbnails/<pat>","covconnectgenerateThumbnails",covconnectgenerateThumbnails,methods=["POST"])

app.add_url_rule("/app/COVConnect/returnImageOriginal/<pat>/<usr>","covconnectreturnImageOriginal",covconnectreturnImageOriginal,methods = ['POST'])
app.add_url_rule("/app/COVConnect/returnImageLesion/<pat>/<usr>","covconnectreturnImageLesion",covconnectreturnImageLesion,methods = ['POST'])
app.add_url_rule("/app/COVConnect/returnImageOrgane/<pat>/<usr>","covconnectreturnImageOrgane",covconnectreturnImageOrgane,methods = ['POST'])
app.add_url_rule("/app/COVConnect/returnImageNone","covconnectimgNone",covconnectimgNone,methods = ['POST'])

app.add_url_rule("/app/COVConnect/replaceImage/<pat>/<usr>","covconnectreplaceImage",covconnectreplaceImage,methods = ['POST'])
app.add_url_rule("/app/COVConnect/returnTotalImages/<pat>/<usr>","covconnectcountTotal",covconnectcountTotal,methods = ['POST'])
app.add_url_rule("/app/COVConnect/deleteOne/<pat>/<usr>","covconnectdeleteOne",covconnectdeleteOne,methods = ['POST'])
app.add_url_rule("/app/COVConnect/deleteMany/<pat>/<usr>","covconnectdeleteMany",covconnectdeleteMany,methods = ['POST'])
app.add_url_rule("/app/COVConnect/segmenter/","covconnectSegmenter",covconnectSegmenter,methods=['POST'])
app.add_url_rule("/app/COVConnect/construction3d/<pat>/<usr>","covconnectConstruction3d",covconnectConstruction3d,methods = ['POST'])
app.add_url_rule("/app/COVConnect/download3dfile/<pat>/<usr>","covconnectDownload_3d_file",covconnectDownload_3d_file,methods = ['GET'])
app.add_url_rule("/app/COVConnect/download3dfile2/<pat>/<usr>","covconnectDownload_3d_file2",covconnectDownload_3d_file2,methods = ['GET'])
app.add_url_rule("/app/COVConnect/getInfectionRate/<pat>/<usr>","covconnecttauxInfection",covconnecttauxInfection,methods = ['POST'])




# RDConnect ROUTES ###
app.add_url_rule("/app/RDConnect","RDconnectApp",RDconnectApp)
app.add_url_rule("/app/RDConnect/RDconnectUserDetails","RDconnectUserDetails",RDconnectUserDetails,methods=["POST"])
app.add_url_rule("/app/RDConnect/RDconnectLogOut","RDconnectLogOut",RDconnectLogOut,methods=["POST"])
app.add_url_rule("/app/RDConnect/RDconnectAddPat","RDconnectAddPat",RDconnectAddPat,methods=["POST"])
app.add_url_rule("/app/RDConnect/RDconnectDelPat","RDconnectDelPat",RDconnectDelPat,methods=["POST"])
app.add_url_rule("/app/RDConnect/listPat","RDconnectlistPat",RDconnectlistPat,methods=["POST"])
app.add_url_rule("/app/RDConnect/upload/<origin>","RDconnectupload",RDconnectupload,methods=["POST"])
app.add_url_rule("/app/RDConnect/generateThumbnails/<pat>","RDconnectgenerateThumbnails",RDconnectgenerateThumbnails,methods=["POST"])

app.add_url_rule("/app/RDConnect/returnImageOriginal/<pat>/<usr>","RDconnectreturnImageOriginal",RDconnectreturnImageOriginal,methods = ['POST'])
app.add_url_rule("/app/RDConnect/returnImageLesion/<pat>/<usr>","RDconnectreturnImageLesion",RDconnectreturnImageLesion,methods = ['POST'])
app.add_url_rule("/app/RDConnect/returnImageOrgane/<pat>/<usr>","RDconnectreturnImageOrgane",RDconnectreturnImageOrgane,methods = ['POST'])
app.add_url_rule("/app/RDConnect/returnImageNone","RDconnectimgNone",RDconnectimgNone,methods = ['POST'])

app.add_url_rule("/app/RDConnect/replaceImage/<pat>/<usr>","RDconnectreplaceImage",RDconnectreplaceImage,methods = ['POST'])
app.add_url_rule("/app/RDConnect/returnTotalImages/<pat>/<usr>","RDconnectcountTotal",RDconnectcountTotal,methods = ['POST'])
app.add_url_rule("/app/RDConnect/deleteOne/<pat>/<usr>","RDconnectdeleteOne",RDconnectdeleteOne,methods = ['POST'])
app.add_url_rule("/app/RDConnect/deleteMany/<pat>/<usr>","RDconnectdeleteMany",RDconnectdeleteMany,methods = ['POST'])
app.add_url_rule("/app/RDConnect/segmenter/","RDconnectSegmenter",RDconnectSegmenter,methods=['POST'])
app.add_url_rule("/app/RDConnect/classifier/<pat>/<usr>","RDconnectClassifier",RDconnectClassifier,methods=['POST'])

app.add_url_rule("/app/RDConnect/construction3d/<pat>/<usr>","RDconnectConstruction3d",RDconnectConstruction3d,methods = ['POST'])
app.add_url_rule("/app/RDConnect/download3dfile/<pat>/<usr>","RDconnectDownload_3d_file",RDconnectDownload_3d_file,methods = ['GET'])
app.add_url_rule("/app/RDConnect/download3dfile2/<pat>/<usr>","RDconnectDownload_3d_file2",RDconnectDownload_3d_file2,methods = ['GET'])
app.add_url_rule("/app/RDConnect/getInfectionRate/<pat>/<usr>","RDconnecttauxInfection",RDconnecttauxInfection,methods = ['POST'])

# SEP routes
app.add_url_rule("/app/SEPConnect","SEPconnectApp",SEPconnectApp)
app.add_url_rule("/app/SEPConnect/SEPconnectUserDetails","SEPconnectUserDetails",SEPconnectUserDetails,methods=["POST"])
app.add_url_rule("/app/SEPConnect/SEPconnectLogOut","SEPconnectLogOut",SEPconnectLogOut,methods=["POST"])
app.add_url_rule("/app/SEPConnect/SEPconnectAddPat","SEPconnectAddPat",SEPconnectAddPat,methods=["POST"])
app.add_url_rule("/app/SEPConnect/SEPconnectDelPat","SEPconnectDelPat",SEPconnectDelPat,methods=["POST"])
app.add_url_rule("/app/SEPConnect/listPat","SEPconnectlistPat",SEPconnectlistPat,methods=["POST"])
app.add_url_rule("/app/SEPConnect/upload/<origin>","SEPconnectupload",SEPconnectupload,methods=["POST"])
app.add_url_rule("/app/SEPConnect/generateThumbnails/<pat>","SEPconnectgenerateThumbnails",SEPconnectgenerateThumbnails,methods=["POST"])
app.add_url_rule("/app/SEPConnect/returnImageOriginal/<pat>/<usr>","SEPconnectreturnImageOriginal",SEPconnectreturnImageOriginal,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/returnImageLesion/<pat>/<usr>","SEPconnectreturnImageLesion",SEPconnectreturnImageLesion,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/returnImageOrgane/<pat>/<usr>","SEPconnectreturnImageOrgane",SEPconnectreturnImageOrgane,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/returnImageNone","SEPconnectimgNone",SEPconnectimgNone,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/replaceImage/<pat>/<usr>","SEPconnectreplaceImage",SEPconnectreplaceImage,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/returnTotalImages/<pat>/<usr>","SEPconnectcountTotal",SEPconnectcountTotal,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/deleteOne/<pat>/<usr>","SEPconnectdeleteOne",SEPconnectdeleteOne,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/deleteMany/<pat>/<usr>","SEPconnectdeleteMany",SEPconnectdeleteMany,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/segmenter/","SEPconnectSegmenter",SEPconnectSegmenter,methods=['POST'])
app.add_url_rule("/app/SEPConnect/construction3d/<pat>/<usr>","SEPconnectConstruction3d",SEPconnectConstruction3d,methods = ['POST'])
app.add_url_rule("/app/SEPConnect/download3dfile/<pat>/<usr>","SEPconnectDownload_3d_file",SEPconnectDownload_3d_file,methods = ['GET'])
app.add_url_rule("/app/SEPConnect/download3dfile2/<pat>/<usr>","SEPconnectDownload_3d_file2",SEPconnectDownload_3d_file2,methods = ['GET'])
app.add_url_rule("/app/SEPConnect/getInfectionRate/<pat>/<usr>","SEPconnecttauxInfection",SEPconnecttauxInfection,methods = ['POST'])


# MTLE connect routes

app.add_url_rule("/app/mTLEConnect","mTLEConnectApp",mTLEConnectApp)
app.add_url_rule("/app/mTLEConnect/mTLEConnectUserDetails","mTLEConnectUserDetails",mTLEConnectUserDetails,methods=["POST"])
app.add_url_rule("/app/mTLEConnect/mTLEConnectLogOut","mTLEConnectLogOut",mTLEConnectLogOut,methods=["POST"])
app.add_url_rule("/app/mTLEConnect/mTLEConnectAddPat","mTLEConnectAddPat",mTLEConnectAddPat,methods=["POST"])
app.add_url_rule("/app/mTLEConnect/mTLEConnectDelPat","mTLEConnectDelPat",mTLEConnectDelPat,methods=["POST"])
app.add_url_rule("/app/mTLEConnect/listPat","mTLEConnectlistPat",mTLEConnectlistPat,methods=["POST"])
app.add_url_rule("/app/mTLEConnect/upload/<origin>","mTLEConnectupload",mTLEConnectupload,methods=["POST"])
app.add_url_rule("/app/mTLEConnect/generateThumbnails/<pat>","mTLEConnectgenerateThumbnails",mTLEConnectgenerateThumbnails,methods=["POST"])
app.add_url_rule("/app/mTLEConnect/returnImageOriginal/<pat>/<usr>","mTLEConnectreturnImageOriginal",mTLEConnectreturnImageOriginal,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/returnImageLesion/<pat>/<usr>","mTLEConnectreturnImageLesion",mTLEConnectreturnImageLesion,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/returnImageOrgane/<pat>/<usr>","mTLEConnectreturnImageOrgane",mTLEConnectreturnImageOrgane,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/returnImageNone","mTLEConnectimgNone",mTLEConnectimgNone,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/replaceImage/<pat>/<usr>","mTLEConnectreplaceImage",mTLEConnectreplaceImage,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/returnTotalImages/<pat>/<usr>","mTLEConnectcountTotal",mTLEConnectcountTotal,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/deleteOne/<pat>/<usr>","mTLEConnectdeleteOne",mTLEConnectdeleteOne,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/deleteMany/<pat>/<usr>","mTLEConnectdeleteMany",mTLEConnectdeleteMany,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/segmenter/","mTLEConnectSegmenter",mTLEConnectSegmenter,methods=['POST'])
app.add_url_rule("/app/mTLEConnect/construction3d/<pat>/<usr>","mTLEConnectConstruction3d",mTLEConnectConstruction3d,methods = ['POST'])
app.add_url_rule("/app/mTLEConnect/download3dfile/<pat>/<usr>","mTLEConnectDownload_3d_file",mTLEConnectDownload_3d_file,methods = ['GET'])
app.add_url_rule("/app/mTLEConnect/download3dfile2/<pat>/<usr>","mTLEConnectDownload_3d_file2",mTLEConnectDownload_3d_file2,methods = ['GET'])
app.add_url_rule("/app/mTLEConnect/getInfectionRate/<pat>/<usr>","mTLEConnecttauxInfection",mTLEConnecttauxInfection,methods = ['POST'])

#404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

### RUN API ###
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)