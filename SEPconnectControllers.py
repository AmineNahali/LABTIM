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

def SEPconnectApp():
    args = request.args
    theuser=args.get("accept")
    if session.get(f"{theuser},SEPConnect") or session.get("su"):
        return render_template('SEPConnect/SEPConnect.html')
    else:
        return redirect("/loginUsers?initApp=SEPConnect")

def SEPconnectUserDetails():
    data = request.get_json(force=True)
    varMail = str(data["tr"])
    if session.get(f"{varMail},SEPConnect") or session.get("su"):
        if global_col_users.count_documents({"Mail":varMail}) == 0:
            #user n'existe pas
            return jsonify({"msg":"failure","user":"erreur","spec":"erreur"})
        else:
            tmpUSR = global_col_users.find_one({"Mail":varMail})
            _usernameSEP = str(tmpUSR["Nom"]) + " " +str(tmpUSR["Prenom"])
            _specSEP = str(tmpUSR["Spec"])
            return jsonify({"msg":"success","user":str(_usernameSEP),"spec":str(_specSEP)})
    else:
        return jsonify({"msg":"redirected","urlto":"/loginUsers?initApp=SEPConnect"})

def SEPconnectLogOut():
    data = request.get_json(force=True)
    varMail = str(data["tr"])
    session[f"{varMail},SEPConnect"] = None
    return jsonify({"msg":"success"})

def SEPconnectAddPat():
    data = request.get_json(force=True)
    npat = str(data["who"])
    varMail = str(data["by"])
    dat = str(data["when"])
    if session.get(f"{varMail},SEPConnect"):
        if global_col_patients.count_documents({"ID":npat}) == 0:
            os.makedirs("./upload/"+npat+"/original")
            os.makedirs("./upload/"+npat+"/segmented")
            os.makedirs("./upload/"+npat+"/segmented2")
            os.makedirs("./upload/"+npat+"/3dfile")
            os.makedirs("./upload/"+npat+"/tmp")
            os.makedirs("./upload/"+npat+"/tmp2")
            global_col_patients.insert_one({"ID":npat,"App":"SEPConnect","Ajout":dat,"Responsable":varMail})
            ##x = global_col_apps.find_one({"Nom_App":"SEPConnect"})
            ##total_old = int(str(x["Total_patients"]))
            ##total_old = total_old+1
            ##global_col_apps.update_one({"Nom_App":"SEPConnect"},{"$set":{"Total_patients":str(total_old)}})
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
            global_col_patients.insert_one({"ID":npat,"App":"SEPConnect","Ajout":dat,"Responsable":"su"})
            x = global_col_apps.find_one({"Nom_App":"SEPConnect"})
            total_old = int(str(x["Total_patients"]))
            total_old = total_old+1
            global_col_apps.update_one({"Nom_App":"SEPConnect"},{"$set":{"Total_patients":str(total_old)}})
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"duplicate"})
    else:
        return jsonify({"msg":"failure","urlto":"/loginUsers?initApp=SEPConnect"})

def SEPconnectlistPat():
    data = request.get_json(force=True)
    resp = str(data["for"])
    if session.get(f"{resp},SEPConnect"):
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
        return redirect("/loginUsers?initApp=SEPConnect")

def SEPconnectupload(origin):
    files = request.files.getlist("file")
    for file in files:
        file.save(os.path.join("./upload/"+origin+"/original/", file.filename))
    return jsonify({"msg":"success"})

def SEPconnectgenerateThumbnails(pat):
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

def SEPconnectDelPat():
    data = request.get_json(force=True)
    targDel = str(data["targDel"])
    deleter = str(data["deleter"])
    if session.get(f"{deleter},SEPConnect"):
        if global_col_patients.count_documents({"ID":targDel}) >= 1:
            global_col_patients.delete_many({"ID":targDel})
            SEP_vol_infx.delete_many({"ID":targDel})
            SEP_vol_poum.delete_many({"ID":targDel})
            x = global_col_apps.find_one({"Nom_App":"SEPConnect"})
            total_old = int(str(x["Total_utilisateurs"]))
            print(f"TOTAL OLD = {total_old}")
            nexTotP = total_old-1
            if nexTotP < 0:
                nexTotP=0
            print(f"TOTAL new = {nexTotP}")
            global_col_apps.update_one({"Nom_App":"SEPConnect"},{"$set":{"Total_patients":str(nexTotP)}})
            remover(f"./upload/{targDel}")
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"success"})
    elif session.get("su"):
        if global_col_patients.count_documents({"ID":targDel}) >= 1:
            global_col_patients.delete_many({"ID":targDel})
            SEP_vol_infx.delete_many({"ID":targDel})
            SEP_vol_poum.delete_many({"ID":targDel})
            x = global_col_apps.find_one({"Nom_App":"SEPConnect"})
            total_old = int(str(x["Total_utilisateurs"]))
            print('TOTAL OLD = '+total_old)
            nexTotP = total_old-1
            if nexTotP < 0:
                nexTotP=0
            print('TOTAL new = '+nexTotP)
            global_col_apps.update_one({"Nom_App":"SEPConnect"},{"$set":{"Total_patients":str(nexTotP)}})
            remover(f"./upload/{targDel}")
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"success"})
    else:
        return redirect("/loginUsers?initApp=SEPConnect")

def SEPconnectreturnImageOriginal(pat,usr):
    data = request.get_json(force=True)
    mode = int(data["mode"])
    indx = str(data["imgIndex"])
    path_to_img = "./upload/"+pat+"/original/"+ indx +".png"
    if os.path.exists(path_to_img):
        print("requested Image : "+path_to_img)
        return send_file(path_to_img)
    else:
        return send_file("./aucune.png")

def SEPconnectreturnImageLesion(pat,usr):
    data = request.get_json(force=True)
    mode = int(data["mode"])
    indx = str(data["imgIndex"])
    path_to_img = "./upload/"+pat+"/segmented/"+ indx +".png"
    if os.path.exists(path_to_img):
        print("requested Image : "+path_to_img)
        return send_file(path_to_img)
    else:
        return send_file("./aucune.png")

def SEPconnectreturnImageOrgane(pat,usr):
    data = request.get_json(force=True)
    mode = int(data["mode"])
    indx = str(data["imgIndex"])
    path_to_img = "./upload/"+pat+"/segmented2/"+ indx +".png"
    if os.path.exists(path_to_img):
        print("requested Image : "+path_to_img)
        return send_file(path_to_img)
    else:
        return send_file("./aucune.png")

def SEPconnectimgNone():
	path_to_img = "./aucune.png"
	return send_file(path_to_img)

def SEPconnectreplaceImage(pat,usr):
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

def SEPconnectcountTotal(pat,usr):
    data = request.get_json(force = True)
    mode = int(data["mode"])
    path, dirs, files = next(os.walk("./upload/"+pat+"/original/"))
    file_count = len(files)
    return jsonify({"lenF":f"{file_count}"})

def SEPconnectdeleteOne(pat,usr):
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

def SEPconnectdeleteMany(pat,usr):
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

def SEPconnectSegmenter():
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

def SEPconnectConstruction3d(pat,usr):
    if os.path.exists("./upload/"+pat+"/3dfile/model3D.obj") and os.path.exists("./upload/"+pat+"/3dfile/poumons.obj"):
        return jsonify({"msg":"success"})
    else:
        if len(os.listdir("./upload/"+pat+"/segmented/")) == 0 or len(os.listdir("./upload/"+pat+"/segmented2/")) == 0:
            return jsonify({"msg":"failed"})
        else:
            Reconstruction3D_Lesion(pat)
            Reconstruction3D_Poumons(pat)
            return jsonify({"msg":"success"})

def SEPconnectDownload_3d_file(pat,usr):
	return send_file("./upload/"+pat+"/3dfile/model3D.obj")

def SEPconnectDownload_3d_file2(pat,usr):
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

def load_hdf5(infile):
       with h5py.File(infile,"r") as f:  #"with" close the file after its nested commands
           return f["image"][()]

def rgb2gray(rgb):
    assert (len(rgb.shape)==4)  
    assert (rgb.shape[1]==3)
    bn_imgs = rgb[:,0,:,:]*0.299 + rgb[:,1,:,:]*0.587 + rgb[:,2,:,:]*0.114
    bn_imgs = np.reshape(bn_imgs,(rgb.shape[0],1,rgb.shape[2],rgb.shape[3]))
    return bn_imgs

def my_PreProc(data):
    assert(len(data.shape)==4)
    assert (data.shape[1]==3)  #Use the original images
    #black-white conversion
    train_imgs = rgb2gray(data)
    #my preprocessing:
    train_imgs = dataset_normalized(train_imgs)
    train_imgs = clahe_equalized(train_imgs)
    train_imgs = adjust_gamma(train_imgs, 1.2)
    train_imgs = train_imgs/255.  #reduce to 0-1 range
    return train_imgs

 #==== histogram equalization
def histo_equalized(imgs):
     assert (len(imgs.shape)==4)  
     imgs_equalized = np.empty(imgs.shape)
     for i in range(imgs.shape[0]):
         imgs_equalized[i,0] = cv2.equalizeHist(np.array(imgs[i,0], dtype = np.uint8))
     return imgs_equalized


def clahe_equalized(imgs):
     assert (len(imgs.shape)==4)  
     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
     imgs_equalized = np.empty(imgs.shape)
     for i in range(imgs.shape[0]):
         imgs_equalized[i,0] = clahe.apply(np.array(imgs[i,0], dtype = np.uint8))
     return imgs_equalized


 # ===== normalize over the dataset
def dataset_normalized(imgs):
     assert (len(imgs.shape)==4)  
     imgs_normalized = np.empty(imgs.shape)
     imgs_std = np.std(imgs)
     imgs_mean = np.mean(imgs)
     imgs_normalized = (imgs-imgs_mean)/imgs_std
     for i in range(imgs.shape[0]):
         imgs_normalized[i] = ((imgs_normalized[i] - np.min(imgs_normalized[i])) / (np.max(imgs_normalized[i])-np.min(imgs_normalized[i])))*255
     return imgs_normalized

# ===== adjust_gamma
def adjust_gamma(imgs, gamma):
    assert (len(imgs.shape)==4) 
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    new_imgs = np.empty(imgs.shape)
    for i in range(imgs.shape[0]):
        new_imgs[i,0] = cv2.LUT(np.array(imgs[i,0], dtype = np.uint8), table)
    return new_imgs


        #***********extract patches randomly in the full training images*************


def paint_border_overlap(full_imgs, patch_h, patch_w, stride_h, stride_w):
     assert (len(full_imgs.shape)==4)  #4D arrays
     assert (full_imgs.shape[1]==1 or full_imgs.shape[1]==3)  #check the channel is 1 or 3
     img_h = full_imgs.shape[2]  #height of the full image
     img_w = full_imgs.shape[3] #width of the full image
     leftover_h = (img_h-patch_h)%stride_h  #leftover on the h dim
     leftover_w = (img_w-patch_w)%stride_w  #leftover on the w dim
     if (leftover_h != 0):  #change dimension of img_h
         tmp_full_imgs = np.zeros((full_imgs.shape[0],full_imgs.shape[1],img_h+(stride_h-leftover_h),img_w))
         tmp_full_imgs[0:full_imgs.shape[0],0:full_imgs.shape[1],0:img_h,0:img_w] = full_imgs
         full_imgs = tmp_full_imgs
     if (leftover_w != 0):   #change dimension of img_w
         tmp_full_imgs = np.zeros((full_imgs.shape[0],full_imgs.shape[1],full_imgs.shape[2],img_w+(stride_w - leftover_w)))
         tmp_full_imgs[0:full_imgs.shape[0],0:full_imgs.shape[1],0:full_imgs.shape[2],0:img_w] = full_imgs
         full_imgs = tmp_full_imgs
     return full_imgs

        #**************Divide all the full_imgs in pacthes*********************
def extract_ordered_overlap(full_imgs, patch_h, patch_w,stride_h,stride_w):
    assert (len(full_imgs.shape)==4)  #4D arrays
    assert (full_imgs.shape[1]==1 or full_imgs.shape[1]==3)  #check the channel is 1 or 3
    img_h = full_imgs.shape[2]  #height of the full image
    img_w = full_imgs.shape[3] #width of the full image
    assert ((img_h-patch_h)%stride_h==0 and (img_w-patch_w)%stride_w==0)
    N_patches_img = ((img_h-patch_h)//stride_h+1)*((img_w-patch_w)//stride_w+1)  #// --> division between integers
    N_patches_tot = N_patches_img*full_imgs.shape[0]
    patches = np.empty((N_patches_tot,full_imgs.shape[1],patch_h,patch_w))
    iter_tot = 0   #iter over the total number of patches (N_patches)
    for i in range(full_imgs.shape[0]):  #loop over the full images
        for h in range((img_h-patch_h)//stride_h+1):
            for w in range((img_w-patch_w)//stride_w+1):
                patch = full_imgs[i,:,h*stride_h:(h*stride_h)+patch_h,w*stride_w:(w*stride_w)+patch_w]
                patches[iter_tot]=patch
                iter_tot +=1   #total
    assert (iter_tot==N_patches_tot)
    return patches  #array with all the full_imgs divided in patches

        #********************Recompone the full images with the patches******************
def recompone_overlap(preds, img_h, img_w, stride_h, stride_w):
    assert (len(preds.shape)==4)  #4D arrays
    assert (preds.shape[1]==1 or preds.shape[1]==3)  #check the channel is 1 or 3
    patch_h = preds.shape[2]
    patch_w = preds.shape[3]
    N_patches_h = (img_h-patch_h)//stride_h+1
    N_patches_w = (img_w-patch_w)//stride_w+1
    N_patches_img = N_patches_h * N_patches_w
    assert (preds.shape[0]%N_patches_img==0)
    N_full_imgs = preds.shape[0]//N_patches_img
    full_prob = np.zeros((N_full_imgs,preds.shape[1],img_h,img_w)) 
    full_sum = np.zeros((N_full_imgs,preds.shape[1],img_h,img_w))

    k = 0 #iterator over all the patches
    for i in range(N_full_imgs):
        for h in range((img_h-patch_h)//stride_h+1):
            for w in range((img_w-patch_w)//stride_w+1):
                full_prob[i,:,h*stride_h:(h*stride_h)+patch_h,w*stride_w:(w*stride_w)+patch_w]+=preds[k]
                full_sum[i,:,h*stride_h:(h*stride_h)+patch_h,w*stride_w:(w*stride_w)+patch_w]+=1
                k+=1
    assert(k==preds.shape[0])
    assert(np.min(full_sum)>=1.0)  #at least one
    final_avg = full_prob/full_sum
    print (final_avg.shape)
    assert(np.max(final_avg)<=1.0) #max value for a pixel is 1.0
    assert(np.min(final_avg)>=0.0) #min value for a pixel is 0.0
    return final_avg
        #Training

#prepare the mask in the right shape for the Unet
def masks_Unet(masks):
    assert (len(masks.shape)==4)  #4D arrays
    assert (masks.shape[1]==1 )  #check the channel is 1
    im_h = masks.shape[2]
    im_w = masks.shape[3]
    masks = np.reshape(masks,(masks.shape[0],im_h*im_w))
    new_masks = np.empty((masks.shape[0],im_h*im_w,2))
    for i in range(masks.shape[0]):
        for j in range(im_h*im_w):
            if  masks[i,j] == 0:
                new_masks[i,j,0]=1
                new_masks[i,j,1]=0
            else:
                new_masks[i,j,0]=0
                new_masks[i,j,1]=1
    return new_masks

        #===== Convert the prediction arrays in corresponding images
def pred_to_imgs(pred, patch_height, patch_width, mode="original"):
    assert (len(pred.shape)==3)  #3D array: (Npatches,height*width,2)
    assert (pred.shape[2]==2 )  #check the classes are 2
    pred_images = np.empty((pred.shape[0],pred.shape[1]))  #(Npatches,height*width)
    if mode=="original":
        for i in range(pred.shape[0]):
            for pix in range(pred.shape[1]):
                pred_images[i,pix]=pred[i,pix,1]
    elif mode=="threshold":
        for i in range(pred.shape[0]):
            for pix in range(pred.shape[1]):
                if pred[i,pix,1]>=0.5:
                    pred_images[i,pix]=1
                else:
                    pred_images[i,pix]=0
    else:
        print ("mode " +str(mode) +" not recognized, it can be 'original' or 'threshold'")
        exit()
    pred_images = np.reshape(pred_images,(pred_images.shape[0],1, patch_height, patch_width))
    return pred_images

    
#         #********************Get data testing**************************
def get_data_testing_overlap(test_imgs_original,test_groudTruth, Imgs_to_test, patch_height, patch_width, stride_height, stride_width):
    ### test
    test_imgs_original = load_hdf5(test_imgs_original)

    test_masks = load_hdf5(test_groudTruth)


    test_imgs = my_PreProc(test_imgs_original)
    test_masks = test_masks/255.

    #extend both images and masks so they can be divided exactly by the patches dimensions
    test_imgs = test_imgs[0:Imgs_to_test,:,:,:]
    test_masks = test_masks[0:Imgs_to_test,:,:,:]

    test_imgs = paint_border_overlap(test_imgs, patch_height, patch_width, stride_height, stride_width)


    #extract the TEST patches from the full images
    patches_imgs_test = extract_ordered_overlap(test_imgs,patch_height,patch_width,stride_height,stride_width)

    return patches_imgs_test, test_imgs.shape[2], test_imgs.shape[3],test_masks


        #******************Affichage*************************

        #group a set of images row per columns
def group_images(data,per_row):
    assert data.shape[0]%per_row==0
    assert (data.shape[1]==1 or data.shape[1]==3)
    data = np.transpose(data,(0,2,3,1))  #corect format for imshow
    all_stripe = []
    for i in range(int(data.shape[0]/per_row)):
        stripe = data[i*per_row]
        for k in range(i*per_row+1, i*per_row+per_row):
            stripe = np.concatenate((stripe,data[k]),axis=1)
        all_stripe.append(stripe)
    totimg = all_stripe[0]
    for i in range(1,len(all_stripe)):
        totimg = np.concatenate((totimg,all_stripe[i]),axis=1)
    return totimg


#visualize image (as PIL image, NOT as matplotlib!)
def visualize(data,filename):
    assert (len(data.shape)==3) #height*width*channels
    img = None
    if data.shape[2]==1:  #in case it is black and white
        data = np.reshape(data,(data.shape[0],data.shape[1]))
    if np.max(data)>1:
        img = Image.fromarray(data.astype(np.uint8))   #the image is already 0-255
    else:
        img = Image.fromarray((data*255).astype(np.uint8))  #the image is between 0-1
    img.save(filename + '.png')
    return img


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
    print("debut segmentation")
#original test images 
    test_imgs_original = dataset_path + "SEP_dataset_imgs_test.hdf5"
    test_imgs_orig = load_hdf5(test_imgs_original)
    full_img_height = test_imgs_orig.shape[2]
    full_img_width = test_imgs_orig.shape[3]

    # dimension of the patches
    patch_height = 48
    patch_width = 48

    #model name
    name_experiment = 'test'
    #N full images to be predicted
    Imgs_to_test = len(N)


    #============ Load the data and divide in patches
    patches_imgs_test = None
    new_height = None
    new_width = None
    masks_test  = None
    patches_masks_test = None
    patches_imgs_test, new_height, new_width,masks_test = get_data_testing_overlap(
            test_imgs_original = test_imgs_original,  #original
            test_groudTruth = dataset_path + "SEP_dataset_groundTruth_test.hdf5", 
            Imgs_to_test = Imgs_to_test,
            patch_height = patch_height,
            patch_width = patch_width,
            stride_height = 5,
            stride_width = 5
        )
        #================ Run the prediction of the patches ==================================

    #Load the saved model
    model =  tf.keras.models.model_from_json(open("./models/sep_model.json").read())
    model.load_weights("./models/sep.h5")

    print('loading model done !')


    #Calculate the predictions
    predictions = model.predict(patches_imgs_test, batch_size=1, verbose=2) #batch size became 1 not 32 which correspond to the batch size in training phase


    #===== Convert the prediction arrays in corresponding images
    pred_patches = pred_to_imgs(predictions, patch_height, patch_width, "original")
    pred_imgs = None
    orig_imgs = None
    gtruth_masks = None

    pred_imgs = recompone_overlap(pred_patches, new_height, new_width, 5, 5)# predictions
    orig_imgs = my_PreProc(test_imgs_orig[0:pred_imgs.shape[0],:,:,:])    #originals

    gtruth_masks = masks_test 

    ## back to original dimensions
    orig_imgs = orig_imgs[:,:,0:full_img_height,0:full_img_width]
    pred_imgs = pred_imgs[:,:,0:full_img_height,0:full_img_width]
    gtruth_masks = gtruth_masks[:,:,0:full_img_height,0:full_img_width]


    #visualize results comparing mask and prediction:
    N_predicted = orig_imgs.shape[0]
    group =1
    assert (N_predicted%group==0)
    for i in range(int(N_predicted/group)):
        orig_stripe = group_images(orig_imgs[i*group:(i*group)+group,:,:,:],group)
        masks_stripe = group_images(gtruth_masks[i*group:(i*group)+group,:,:,:],group)
        pred_stripe = group_images(pred_imgs[i*group:(i*group)+group,:,:,:],group)
        total_img = np.concatenate((orig_stripe,masks_stripe,pred_stripe),axis=1)
        visualize(total_img,"./upload/"+userDir+"/segmented/Original_GroundTruth_Prediction"+str(i))#.show()
   
    if not os.path.exists(pred):
        os.makedirs(pred)
       
    for i in range(int(N_predicted/group)):
        pred_stripe = group_images(pred_imgs[i*group:(i*group)+group,:,:,:],group)
        visualize(pred_stripe,"./upload/"+userDir+"/segmented/Prediction"+str(i))#.show()
    # patch_size=48
    # model = tf.keras.models.load_model('./models/sep.h5',compile = False)
    # path="./upload/"+userDir+"/original"+"/*.png"
    # liste_predite=[]
    # x=1
    # for filename in natsorted(glob.glob(path)):
        # print(filename)
        # img=Image.open(filename)
        # large_image=np.array(img)
        # print("size="  ,large_image.shape)
        # large_image = np.reshape(large_image,(1,large_image.shape[0],large_image.shape[1]))
        # print("large im= ", large_image.shape)
        # segmented_image = prediction(model, large_image, patch_size)
        # liste_predite.append(segmented_image)
    # for i in range(len(liste_predite)):
        # image=liste_predite[i]
        # image=Image.fromarray(image) #.fromArray(image)
        # image.save("./upload/"+userDir+f"/segmented/{x}.tif")
        # with Imw(filename= "./upload/"+userDir+f"/segmented/{x}.tif") as Sampleimg:
            # Sampleimg.format = 'png'
            # Sampleimg.save(filename= "./upload/"+userDir+"/tmp/" + f"{x}.png")
            # print(f"{x} converted to PNG")    
        # print(f"{x} segmented successfully")
        # x+= 1
    # destroyFiles("./upload/"+userDir+"/segmented/")
    # copyToOriginal("./upload/"+userDir+"/tmp/","./upload/"+userDir+"/segmented/")
    # destroyFiles("./upload/"+userDir+"/tmp/")

def prediction(model, image, patch_size):
    print("debut prediction")
    segm_img = np.zeros(image.shape[:3])
    print ("image shape = ", image.shape)
    print ("seg 11 =  ", segm_img.shape)
    #segm_img = np.reshape(segm_img,(1,image.shape[1],image.shape[2]))
    patch_num=1
    for i in range(0, image.shape[1],48):
        for j in range(0, image.shape[2], 48):
            single_patch = image[i:i+patch_size, j:j+patch_size]
            print("single ----= ", single_patch.shape)

            print("**************")
            single_patch_shape = single_patch.shape[:3]
            print("single = ", single_patch_shape)
            single_patch_input = np.expand_dims(single_patch, 0)
            print("single2 = ", single_patch_input)
            single_patch_prediction = (model.predict(single_patch_input)[0,:,:,0] > 0.5).astype(np.uint8)
            segm_img[i:i+single_patch_shape[1], j:j+single_patch_shape[2]] += cv2.resize(single_patch_prediction, single_patch_shape[::-1])
            print("seg im = ",segm_img )
            patch_num+=1
    print("fin prediction")
    return segm_img



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

def SEPconnecttauxInfection(pat,usr):
	data = request.get_json(force = True)
	targetUser = str(data["requested"])
	tmpInfx = SEP_vol_infx.find_one({"ID":pat})
	tmpPoum = SEP_vol_poum.find_one({"ID":pat})
	infectionVol = float(tmpInfx["volINFX"])
	poumonsVol = float(tmpPoum["volPOUM"])
	resultatFinale = float((infectionVol / poumonsVol)*100)
	return jsonify({"fin":str(resultatFinale)})