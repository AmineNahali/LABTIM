import pymongo
import os
from flask import Flask, render_template, redirect, request, session, jsonify,send_file,url_for
from flask_session import Session
import bcrypt


#Init MongoDB client object
mongo_client = pymongo.MongoClient()

#Base de données globale
global_db = mongo_client["BD_globale"]
global_col_users = global_db["BD_users"]
global_col_verif = global_db["BD_verif"]
global_col_etab = global_db["BD_Etab"]
global_col_sess = global_db["BD_sess"]
global_col_admin = global_db["BD_admin"]
global_col_patients = global_db["BD_patients"]
global_col_apps = global_db["BD_apps"]
global_col_appsLogoExtension = global_db["BD_appsLogoExtension"]
global_col_appsDemoExtension = global_db["BD_appsDemoExtension"]
global_col_notifications = global_db["BD_notifications"]


#Base de données COVConnect
cov_db = mongo_client["covconnect"]
cov_users = cov_db["cov_users"]
cov_etab = cov_db["cov_etablissement"]
cov_sess = cov_db["cov_sess"]
cov_pat = cov_db["cov_patients"]
cov_vol_infx = cov_db["cov_vol_infx"]
cov_vol_poum = cov_db["cov_vol_poum"]

dict_spec_covconnect = {"sp--":"(pas de spécialité)","sp00":"Médecine de famille","sp01":"Médecine interne","sp02":"Maladies infectieuses","sp03":"Réanimation médicale","sp04":"Carcinologie médicale"
,"sp05":"Nutrition et maladies nutritionnelles","sp06":"Hématologie clinique","sp07":"Endocrinologie","sp08":"Cardiologie"
,"sp09":"Néphrologie","sp10":"Neurologie","sp11":"Pneumologie","sp12":"Rhumatologie","sp13":"Gastro-entérologie"
,"sp14":"Médecine physique, rééducation et réadaptation fonctionnelle","sp15":"Dermatologie","sp16":"Pédiatrie","sp17":"Psychiatrie"
,"sp18":"Pédopsychiatrie","sp19":"Imagerie médicale","sp20":"Radiothérapie carcinologique","sp21":"Médecine légale","sp22":"Médecine du travail"
,"sp23":"Médecine préventive et communautaire","sp24":"Anesthésie - réanimation","sp25":"Anatomie et cytologie pathologique"
,"sp26":"Médecine d'urgence","sp27":"Chirurgie générale","sp28":"Chirurgie carcinologique","sp29":"Chirurgie thoracique"
,"sp30":"Chirurgie vasculaire périphérique","sp31":"Chirurgie neurologique","sp32":"Chirurgie urologique","sp33":"Chirurgie plastique, réparatrice et esthétique"
,"sp34":"Chirurgie orthopédique et traumatologique","sp35":"Chirurgie pédiatrique","sp36":"Chirurgie cardio-vasculaire","sp37":"Ophtalmologie"
,"sp38":"O.R.L","sp39":"Stomatologie et chirurgie maxillo-faciale","sp40":"Gynécologie-obstétrique","sp41":"Biologie médicale","sp42":"Histo-embryologie"
,"sp43":"Physiologie et exploration fonctionnelle","sp44":"Biophysique et médecine nucléaire","sp45":"Pharmacologie","sp46":"Génétique"
,"sp47":"Anatomie","sp48":"Direction et logistique médico-militaire","sp49":"Médecine de la plongée sous-marine"
,"sp50":"Médecine aéronautique et spatiale","sp51":"Hygiène nucléaire"}