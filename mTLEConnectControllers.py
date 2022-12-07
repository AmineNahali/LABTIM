import os
import os.path
from flask import Flask, render_template, redirect, request, session, jsonify,send_file,url_for
from flask_session import Session
from models import *
from natsort import natsorted
from tools import *
from wand.image import Image as Imw
import glob
import numpy as np
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import trimesh
import skimage
from tensorflow.keras import Input
from tensorflow.keras.models import Model, load_model, save_model
from tensorflow.keras.layers import Input, Activation, BatchNormalization, Dropout, Lambda, Conv2D
from tensorflow.keras.layers import Conv2DTranspose, MaxPooling2D, concatenate, AveragePooling2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from numpy import loadtxt
from PIL import Image, ImageTk
from mpl_toolkits.axes_grid1 import ImageGrid
from skimage import measure
from stl import mesh
from trimesh.viewer import windowed
from trimesh.remesh import subdivide
import h5py
import sys
import numpy as np
from PIL import Image
import cv2
import os

def mTLEConnectApp():
    args = request.args
    theuser=args.get("accept")
    if session.get(f"{theuser},mTLEConnect") or session.get("su"):
        return render_template('mTLEConnect/mTLEConnect.html')
    else:
        return redirect("/loginUsers?initApp=mTLEConnect")

def mTLEConnectUserDetails():
    data = request.get_json(force=True)
    varMail = str(data["tr"])
    if session.get(f"{varMail},mTLEConnect") or session.get("su"):
        if global_col_users.count_documents({"Mail":varMail}) == 0:
            #user n'existe pas
            return jsonify({"msg":"failure","user":"erreur","spec":"erreur"})
        else:
            tmpUSR = global_col_users.find_one({"Mail":varMail})
            _usernameSEP = str(tmpUSR["Nom"]) + " " +str(tmpUSR["Prenom"])
            _specSEP = str(tmpUSR["Spec"])
            return jsonify({"msg":"success","user":str(_usernameSEP),"spec":str(_specSEP)})
    else:
        return jsonify({"msg":"redirected","urlto":"/loginUsers?initApp=mTLEConnect"})

def mTLEConnectLogOut():
    data = request.get_json(force=True)
    varMail = str(data["tr"])
    session[f"{varMail},mTLEConnect"] = None
    return jsonify({"msg":"success"})

def mTLEConnectAddPat():
    data = request.get_json(force=True)
    npat = str(data["who"])
    varMail = str(data["by"])
    dat = str(data["when"])
    if session.get(f"{varMail},mTLEConnect"):
        if global_col_patients.count_documents({"ID":npat}) == 0:
            os.makedirs("./upload/"+npat+"/original")
            os.makedirs("./upload/"+npat+"/segmented")
            os.makedirs("./upload/"+npat+"/segmented2")
            os.makedirs("./upload/"+npat+"/3dfile")
            os.makedirs("./upload/"+npat+"/tmp")
            os.makedirs("./upload/"+npat+"/tmp2")
            global_col_patients.insert_one({"ID":npat,"App":"mTLEConnect","Ajout":dat,"Responsable":varMail})
            ##x = global_col_apps.find_one({"Nom_App":"mTLEConnect"})
            ##total_old = int(str(x["Total_patients"]))
            ##total_old = total_old+1
            ##global_col_apps.update_one({"Nom_App":"mTLEConnect"},{"$set":{"Total_patients":str(total_old)}})
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"duplicate"})
    elif session.get("su"):
        if global_col_patients.count_documents({"ID":npat}) == 0:
            os.makedirs("./upload/"+npat+"/original")
            os.makedirs("./upload/"+npat+"/segmented")
            os.makedirs("./upload/"+npat+"/segmented2")
            os.makedirs("./upload/"+npat+"/3dfile")
            os.makedirs("./upload/"+npat+"/tmp")
            os.makedirs("./upload/"+npat+"/tmp2")
            global_col_patients.insert_one({"ID":npat,"App":"mTLEConnect","Ajout":dat,"Responsable":"su"})
            x = global_col_apps.find_one({"Nom_App":"mTLEConnect"})
            total_old = int(str(x["Total_patients"]))
            total_old = total_old+1
            global_col_apps.update_one({"Nom_App":"mTLEConnect"},{"$set":{"Total_patients":str(total_old)}})
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"duplicate"})
    else:
        return jsonify({"msg":"failure","urlto":"/loginUsers?initApp=mTLEConnect"})

def mTLEConnectlistPat():
    data = request.get_json(force=True)
    resp = str(data["for"])
    if session.get(f"{resp},mTLEConnect"):
        y=""
        if global_col_patients.count_documents({"Responsable":resp}) == 0:
            return jsonify({"msg":"empty"})
        else:
            for x in global_col_patients.find({"Responsable":resp}):
                y=y+str(x["Ajout"])+"&&"+str(x["ID"])+"///"
            return jsonify({"msg":"success","liste":str(y)})
    elif session.get("su"):
        y=""
        if global_col_patients.count_documents({"Responsable":"su"}) == 0:
            return jsonify({"msg":"empty"})
        else:
            for x in global_col_patients.find({"Responsable":"su"}):
                y=y+str(x["Ajout"])+"&&"+str(x["ID"])+"///"
            return jsonify({"msg":"success","liste":str(y)})
    else:
        return redirect("/loginUsers?initApp=mTLEConnect")

def mTLEConnectupload(origin):
    files = request.files.getlist("file")
    for file in files:
        file.save(os.path.join("./upload/"+origin+"/original/", file.filename))
    return jsonify({"msg":"success"})

def mTLEConnectgenerateThumbnails(pat):
	origin_path = "./upload/"+pat +"/original/"
	destination_path = "./upload/"+pat+"/tmp/"
	y = 1
	dirList=os.listdir(origin_path)
	for fname in natsorted(dirList):
		with Imw(filename= f"./upload/{pat}/original/{fname}") as Sampleimg:
			Sampleimg.format = 'png'
			Sampleimg.save(filename= destination_path + f"{y}.png")
			print(f"{y} converted to PNG")
			y += 1
	destroyFiles("./upload/"+pat+"/original/")
	copyToOriginal("./upload/"+pat+"/tmp/" , "./upload/"+pat+"/original/")
	destroyFiles("./upload/"+pat+"/tmp/")
	return  jsonify({"msg":"success"})

def mTLEConnectDelPat():
    data = request.get_json(force=True)
    targDel = str(data["targDel"])
    deleter = str(data["deleter"])
    if session.get(f"{deleter},mTLEConnect"):
        if global_col_patients.count_documents({"ID":targDel}) >= 1:
            global_col_patients.delete_many({"ID":targDel})
            SEP_vol_infx.delete_many({"ID":targDel})
            SEP_vol_poum.delete_many({"ID":targDel})
            x = global_col_apps.find_one({"Nom_App":"mTLEConnect"})
            total_old = int(str(x["Total_utilisateurs"]))
            print(f"TOTAL OLD = {total_old}")
            nexTotP = total_old-1
            if nexTotP < 0:
                nexTotP=0
            print(f"TOTAL new = {nexTotP}")
            global_col_apps.update_one({"Nom_App":"mTLEConnect"},{"$set":{"Total_patients":str(nexTotP)}})
            remover(f"./upload/{targDel}")
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"success"})
    elif session.get("su"):
        if global_col_patients.count_documents({"ID":targDel}) >= 1:
            global_col_patients.delete_many({"ID":targDel})
            SEP_vol_infx.delete_many({"ID":targDel})
            SEP_vol_poum.delete_many({"ID":targDel})
            x = global_col_apps.find_one({"Nom_App":"mTLEConnect"})
            total_old = int(str(x["Total_utilisateurs"]))
            print('TOTAL OLD = '+total_old)
            nexTotP = total_old-1
            if nexTotP < 0:
                nexTotP=0
            print('TOTAL new = '+nexTotP)
            global_col_apps.update_one({"Nom_App":"mTLEConnect"},{"$set":{"Total_patients":str(nexTotP)}})
            remover(f"./upload/{targDel}")
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"success"})
    else:
        return redirect("/loginUsers?initApp=mTLEConnect")

def mTLEConnectreturnImageOriginal(pat,usr):
    data = request.get_json(force=True)
    mode = int(data["mode"])
    indx = str(data["imgIndex"])
    path_to_img = "./upload/"+pat+"/original/"+ indx +".png"
    if os.path.exists(path_to_img):
        print("requested Image : "+path_to_img)
        return send_file(path_to_img)
    else:
        return send_file("./aucune.png")

def mTLEConnectreturnImageLesion(pat,usr):
    data = request.get_json(force=True)
    mode = int(data["mode"])
    indx = str(data["imgIndex"])
    path_to_img = "./upload/"+pat+"/segmented/"+ indx +".png"
    if os.path.exists(path_to_img):
        print("requested Image : "+path_to_img)
        return send_file(path_to_img)
    else:
        return send_file("./aucune.png")

def mTLEConnectreturnImageOrgane(pat,usr):
    data = request.get_json(force=True)
    mode = int(data["mode"])
    indx = str(data["imgIndex"])
    path_to_img = "./upload/"+pat+"/segmented2/"+ indx +".png"
    if os.path.exists(path_to_img):
        print("requested Image : "+path_to_img)
        return send_file(path_to_img)
    else:
        return send_file("./aucune.png")

def mTLEConnectimgNone():
	path_to_img = "./aucune.png"
	return send_file(path_to_img)

def mTLEConnectreplaceImage(pat,usr):
    data = request.get_json(force=True)
    mode = int(data["mode"])
    indx_a_remplacer = str(data["indx_a_remplacer"])
    indx_remplacer_par = str(data["indx_remplacer_par"])
    if (indx_a_remplacer == indx_remplacer_par) :
        return jsonify({"msg":"success"})
    else:
        if os.path.exists("./upload/"+pat+"/original/"+indx_remplacer_par+".png") and os.path.exists("./upload/"+pat+"/original/"+"/"+indx_a_remplacer+".png"):
            shutil.copy2("./upload/"+pat+"/original/"+indx_remplacer_par+".png","./upload/"+pat+"/tmp2/")
            os.rename("./upload/"+pat+"/tmp2/"+indx_remplacer_par+".png","./upload/"+pat+"/tmp2/"+indx_a_remplacer+".png")
            os.remove("./upload/"+pat+"/original/"+"/"+indx_a_remplacer+".png")
            shutil.copy2("./upload/"+pat+"/tmp2/"+indx_a_remplacer+".png","./upload/"+pat+"/original/")
            destroyFiles("./upload/"+pat+"/tmp2/")
        if os.path.exists("./upload/"+pat+"/segmented/"+indx_remplacer_par+".png") and os.path.exists("./upload/"+pat+"/segmented/"+"/"+indx_a_remplacer+".png"):
            shutil.copy2("./upload/"+pat+"/segmented/"+indx_remplacer_par+".png","./upload/"+pat+"/tmp2/")
            os.rename("./upload/"+pat+"/tmp2/"+indx_remplacer_par+".png","./upload/"+pat+"/tmp2/"+indx_a_remplacer+".png")
            os.remove("./upload/"+pat+"/segmented/"+"/"+indx_a_remplacer+".png")
            shutil.copy2("./upload/"+pat+"/tmp2/"+indx_a_remplacer+".png","./upload/"+pat+"/segmented/")
            destroyFiles("./upload/"+pat+"/tmp2/")
        if os.path.exists("./upload/"+pat+"/segmented2/"+indx_remplacer_par+".png") and os.path.exists("./upload/"+pat+"/segmented2/"+"/"+indx_a_remplacer+".png"):
            shutil.copy2("./upload/"+pat+"/segmented2/"+indx_remplacer_par+".png","./upload/"+pat+"/tmp2/")
            os.rename("./upload/"+pat+"/tmp2/"+indx_remplacer_par+".png","./upload/"+pat+"/tmp2/"+indx_a_remplacer+".png")
            os.remove("./upload/"+pat+"/segmented2/"+"/"+indx_a_remplacer+".png")
            shutil.copy2("./upload/"+pat+"/tmp2/"+indx_a_remplacer+".png","./upload/"+pat+"/segmented2/")
            destroyFiles("./upload/"+pat+"/tmp2/")
        return jsonify({"msg":"success"})

def mTLEConnectcountTotal(pat,usr):
    data = request.get_json(force = True)
    mode = int(data["mode"])
    path, dirs, files = next(os.walk("./upload/"+pat+"/original/"))
    file_count = len(files)
    return jsonify({"lenF":f"{file_count}"})

def mTLEConnectdeleteOne(pat,usr):
    data = request.get_json(force = True)
    mode = int(data["mode"])
    toBeDeleted = str(data["deleted"])
    if os.path.exists("./upload/"+pat+"/original/"+toBeDeleted+".png"):
        os.remove("./upload/"+pat+"/original/"+toBeDeleted+".png")
        resetNames(pat,"original")
    if os.path.exists("./upload/"+pat+"/segmented/"+toBeDeleted+".png"):
        os.remove("./upload/"+pat+"/segmented/"+toBeDeleted+".png")
        resetNames(pat,"segmented")
    if os.path.exists("./upload/"+pat+"/segmented2/"+toBeDeleted+".png"):
        os.remove("./upload/"+pat+"/segmented2/"+toBeDeleted+".png")
        resetNames(pat,"segmented2")
    return jsonify({"msg":"success"})

def mTLEConnectdeleteMany(pat,usr):
    data = request.get_json(force = True)
    mode = int(data["mode"])
    leftIndx = int(data["left"])
    rightIndx = int(data["right"])
    if (leftIndx == rightIndx):
        if os.path.exists("./upload/"+pat+"/original/"+leftIndx+".png"):
            os.remove("./upload/"+pat+"/original/"+leftIndx+".png")
            resetNames(pat,"original")
        if os.path.exists("./upload/"+pat+"/segmented/"+leftIndx+".png"):
            os.remove("./upload/"+pat+"/segmented/"+leftIndx+".png")
            resetNames(pat,"segmented")
        if os.path.exists("./upload/"+pat+"/segmented2/"+leftIndx+".png"):
            os.remove("./upload/"+pat+"/segmented2/"+leftIndx+".png")
            resetNames(pat,"segmented2")
        return jsonify({"msg":"success"})
    elif(leftIndx > rightIndx):
        return jsonify({"msg":"failed"})
    else:
        for xx in range(leftIndx,rightIndx+1):
            if os.path.exists("./upload/"+pat+"/original/"+str(xx)+".png"):
                os.remove("./upload/"+pat+"/original/"+str(xx)+".png")
            if os.path.exists("./upload/"+pat+"/segmented/"+str(xx)+".png"):
                os.remove("./upload/"+pat+"/segmented/"+str(xx)+".png")
            if os.path.exists("./upload/"+pat+"/segmented2/"+str(xx)+".png"):
                os.remove("./upload/"+pat+"/segmented2/"+str(xx)+".png")
        resetNames(pat,"original")
        resetNames(pat,"segmented")
        resetNames(pat,"segmented2")
        return jsonify({"msg":"success"})

def mTLEConnectSegmenter():
    data = request.get_json(force = True)
    pat = str(data["pat"])
    usr = str(data["usr"])
    if len(os.listdir(f"./upload/{pat}/original")) == 0:
        return jsonify({"msg":"nooriginal"})
    else:
        if len(os.listdir(f"./upload/{pat}/segmented")) != 0 or len(os.listdir(f"./upload/{pat}/segmented2")) != 0:
            remover(f"./upload/{pat}/segmented")
            remover(f"./upload/{pat}/segmented2")
            os.makedirs(f"./upload/{pat}/segmented")
            os.makedirs(f"./upload/{pat}/hdf5")
            os.makedirs(f"./upload/{pat}/segmented2")
        segmenter(pat)
        #segmenter2(pat)
        return jsonify({"msg":"success"})

def mTLEConnectConstruction3d(pat,usr):
    if os.path.exists("./upload/"+pat+"/3dfile/model3D.obj") and os.path.exists("./upload/"+pat+"/3dfile/poumons.obj"):
        return jsonify({"msg":"success"})
    else:
        if len(os.listdir("./upload/"+pat+"/segmented/")) == 0 or len(os.listdir("./upload/"+pat+"/segmented2/")) == 0:
            return jsonify({"msg":"failed"})
        else:
            Reconstruction3D_Lesion(pat)
            Reconstruction3D_Poumons(pat)
            return jsonify({"msg":"success"})

def mTLEConnectDownload_3d_file(pat,usr):
	return send_file("./upload/"+pat+"/3dfile/model3D.obj")

def mTLEConnectDownload_3d_file2(pat,usr):
	return send_file("./upload/"+pat+"/3dfile/poumons.obj")


def prediction(model, image, patch_size):
    print("debut prediction")
    segm_img = np.zeros(image.shape[:2])
    patch_num=1
    for i in range(0, image.shape[0],128):
        for j in range(0, image.shape[1], 128):
            single_patch = image[i:i+patch_size, j:j+patch_size]
            single_patch_shape = single_patch.shape[:2]
            single_patch_input = np.expand_dims(single_patch, 0)
            single_patch_prediction = (model.predict(single_patch_input)[0,:,:,0] > 0.5).astype(np.uint8)
            segm_img[i:i+single_patch_shape[0], j:j+single_patch_shape[1]] += cv2.resize(single_patch_prediction, single_patch_shape[::-1])
            patch_num+=1
    print("fin prediction")
    return segm_img


def write_hdf5(arr,outfile):
    with h5py.File(outfile,"w") as f:
        f.create_dataset("image", data=arr, dtype=arr.dtype)

def get_datasets(Nimgs,imgs_dir,groundTruth_dir,train_test="null"):
    height=217
    width=181
    channels=3
    imgs = np.empty((Nimgs,height,width,channels))
    groundTruth = np.empty((Nimgs,height,width))
    border_masks = np.empty((Nimgs,height,width))
    
    for path, subdirs, files in os.walk(imgs_dir): #list all files
        for i in range(len(files)):
            #original
            print ("original image: " +files[i])
            img = Image.open(imgs_dir+files[i])
            img=img.convert('RGB')
            #img.show()
            print (img)
            imgs[i] = np.asarray(img)
            #corresponding ground truth
            groundTruth_name = files[i][0:4] + "_manual.gif"
            print ("ground truth name: " + groundTruth_name)
            g_truth = Image.open(groundTruth_dir + groundTruth_name)
            g_truth=g_truth.convert('L')
            groundTruth[i] = np.asarray(g_truth)
    imgs = np.transpose(imgs,(0,3,1,2))

    groundTruth = np.reshape(groundTruth,(Nimgs,1,height,width))
    border_masks = np.reshape(border_masks,(Nimgs,1,height,width))
    return  imgs, groundTruth;

def segmenter (userDir):


    original_imgs_test = "C:/Users/amani/Desktop/patient_2/originale/"
    groundTruth_imgs_test = "C:/Users/amani/Desktop/patient_2/groundtruth/"

    dataset_path="./upload/"+userDir+"/hdf5/"
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    N=glob.glob("./upload/"+userDir+'/original/*.png')
    print(len(N))
    imgs_test, groundTruth_test= get_datasets(len(N),original_imgs_test,groundTruth_imgs_test,"test")
    print ("Saving test datasets")
    write_hdf5(imgs_test, dataset_path + "SEP_dataset_imgs_test.hdf5")
    write_hdf5(groundTruth_test, dataset_path + "SEP_dataset_groundTruth_test.hdf5")



def Reconstruction3D_Lesion(userdirectory):
	path_image_original = "./upload/"+userdirectory+"/segmented/"
	path=path_image_original+"/*.png"
	liste_image=[]    
	for filename in natsorted(glob.glob(path)):
		img=Image.open(filename)
		large_image=np.array(img)
		liste_image.append(large_image) 
	slices=[]
	for i in range(len(liste_image)):
		img=liste_image[i]
		large_image=np.array(img)
		slices.append(large_image)
	liste_images=list()	
	for i in range(len(slices)):
		img=slices[i]
		liste_images.append(img)
		stacke_c=np.dstack(liste_images)
	spacing=(1.0,1.0,1.0)
	step=1
	stacke_c =stacke_c.T
	verts, faces, normals, values = skimage.measure.marching_cubes(stacke_c , level=.05 , spacing=spacing , gradient_direction='ascent' , step_size=1 ,allow_degenerate = True)
	surf_mesh1 = trimesh.Trimesh(verts, faces)
	surf_mesh1.export("./upload/"+userdirectory+"/3dfile/model3D.obj")
	volINFX = surf_mesh1.volume
	ginfx = SEP_vol_infx.count_documents({"ID":str(userdirectory)})
	if (ginfx == 0):
		SEP_vol_infx.insert_one({"ID":str(userdirectory),"volINFX":str(volINFX)})

def Reconstruction3D_Poumons(userdirectory):
	path_image_original = "./upload/"+userdirectory+"/segmented2/"
	path=path_image_original+"/*.png"
	liste_image=[]    
	for filename in natsorted(glob.glob(path)):
		img=Image.open(filename)
		large_image=np.array(img)
		liste_image.append(large_image) 
	slices=[]
	for i in range(len(liste_image)):
		img=liste_image[i]
		large_image=np.array(img)
		slices.append(large_image)
	liste_images=list()	
	for i in range(len(slices)):
		img=slices[i]
		liste_images.append(img)
		stacke_c=np.dstack(liste_images)
	spacing=(1.0,1.0,1.0)
	step=1
	stacke_c =stacke_c.T
	vert, face, norm1, val1 = skimage.measure.marching_cubes(stacke_c,level=.05,spacing=spacing,gradient_direction='ascent',step_size=step, allow_degenerate=True)
	surf_mesh2 = trimesh.Trimesh(vert, face)
	surf_mesh2.export("./upload/"+userdirectory+"/3dfile/poumons.obj")
	volPOUM = surf_mesh2.volume
	gpoum = SEP_vol_poum.count_documents({"ID":str(userdirectory)})
	if (gpoum == 0):
		SEP_vol_poum.insert_one({"ID":str(userdirectory),"volPOUM":str(volPOUM)})

def mTLEConnecttauxInfection(pat,usr):
	data = request.get_json(force = True)
	targetUser = str(data["requested"])
	tmpInfx = SEP_vol_infx.find_one({"ID":pat})
	tmpPoum = SEP_vol_poum.find_one({"ID":pat})
	infectionVol = float(tmpInfx["volINFX"])
	poumonsVol = float(tmpPoum["volPOUM"])
	resultatFinale = float((infectionVol / poumonsVol)*100)
	return jsonify({"fin":str(resultatFinale)})