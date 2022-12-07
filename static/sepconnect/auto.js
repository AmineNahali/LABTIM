
//------------------init-----------------//
targetUserMail = getQueryVariable("accept").toString();
let fileField, statusDiv;
document.addEventListener('DOMContentLoaded', init, false);
var continueUpl = false;
targetPat="";
loadPatients();
modeUtilisation = 1;
currentImage=1;
//------------------Call-----------------//
document.getElementById('allerdroite').disabled = false ;
document.getElementById('validerRemplacement').disabled = false ;
document.getElementById('validerSuppression').disabled = false ;
document.getElementById('validerSuppressionPlusieurs').disabled = false ;

document.getElementById('btnSegmentation').disabled = false;
document.getElementById('btnReconstruction3d').disabled = false;
document.getElementById('btnSegmRecons').disabled = false;
putUserDetails();
targetPatientUpload =""

//----------------Declare----------------//

function putUserDetails() {
	fetch("/app/SEPConnect/SEPconnectUserDetails",{method:'POST',body:JSON.stringify({tr:targetUserMail.toString()}),contentType:'application/json'})
	.then(res=>res.json())
	.then((data)=>{
		if (data.msg == "success") {
			document.getElementById("userNamePlace").innerHTML=data.user;
			document.getElementById("userSpecPlace").innerHTML=data.spec;
		}
		if (data.msg == "redirected") {
			window.location.href = data.urlto;
		}
		if (data.msg == "failure") {
			document.getElementById("userNamePlace").innerHTML="erreur";
			document.getElementById("userSpecPlace").innerHTML="erreur";
		}
	})
	.catch(e=>console.log());
}

function logout(){
	fetch("/app/SEPConnect/SEPconnectLogOut",{method:'POST',body:JSON.stringify({tr:targetUserMail.toString()}),contentType:'application/json'})
	.then(res=>res.json())
	.then((data)=>{
		if (data.msg == "success"){
			window.location.reload();
		}
	})
	.catch(e=>console.log());
}

function getQueryVariable(variable)
{
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++)
	{
         var pair = vars[i].split("=");
         if(pair[0] == variable){return pair[1];}
    }
    return(false);
}
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function init() {
	fileField = document.querySelector('#filesToUpload');
	statusDiv = document.querySelector('#status');
	document.querySelector('#testUpload').addEventListener('click', doUpload, false);
}

let totalFilesToUpload = 0;
let uploadedSuccessfully = 0;

async function doUpload(e) {
	console.log('clicked');
	e.preventDefault();
	statusDiv.innerHTML = '';
	totalFilesToUpload = fileField.files.length;
	//nothing was selected
	if(totalFilesToUpload === 0) {
		statusDiv.innerHTML = 'SVP selectionnez des images';
		return;
	}
	avantUpl();
}

async function uploadFile(f) {
	statusDiv.innerHTML ="Chargement de " + f.name; 
	let form = new FormData();
	form.append('file', f);	
	fetch("/app/SEPConnect/upload/"+targetPatientUpload, { method: 'POST', body:form })
	.then((data)=> {return data.json()})
	.then((data)=>{
		if (data.msg == "success")
		{
			statusDiv.innerHTML = "terminé avec " + f.name  ;
			uploadedSuccessfully++ ;
			if(uploadedSuccessfully > totalFilesToUpload){uploadedSuccessfully = totalFilesToUpload;}
			if(uploadedSuccessfully==totalFilesToUpload)
			{
				statusDiv.innerHTML = "chargement terminé" ;
				fetch("/app/SEPConnect/generateThumbnails/"+targetPatientUpload,{method : 'POST'})
				.then(res => res.json())
				.then((data) =>{
					if(data.msg == "success"){
						document.getElementById('addNewPatientModal').style.display = 'none';
                        resetAddInput();
						loadPatients();
                        document.getElementById('loadz').style.display = 'none';
                        window.location.reload();
						
					}
				}).catch((e)=>{console.log(e);});
			}
		}
		else{alert("Un problème est survenu lors de la connexion");}
		})
	.catch((e)=>{
		console.log(e);
	});
}

function avantUpl(){
    continueUpl = false;
    if(document.getElementById('inputPatientID').value.toString()==""){alert("une ID patient est nécessaire");}
    else{
        targetPatientUpload = document.getElementById('inputPatientID').value.toString();
        var today = new Date();
	    var date = today.getDate()+'/'+(today.getMonth()+1)+'/'+today.getFullYear();
        snd = {who:targetPatientUpload.toString(),by:targetUserMail.toString(),when:date.toString()}
        fetch("/app/SEPConnect/SEPconnectAddPat",{method:'POST',body:JSON.stringify(snd),contentType:'application/json'})
        .then(res=>res.json())
        .then((data)=>{
            if(data.msg=="success"){
                document.getElementById('loadz').style.display = 'block';
                //********************************************************************/
                statusDiv.innerHTML = `chargement de ${totalFilesToUpload} images`;
                document.getElementById("addNewPatientModalClose").style.display = "none";
	            let uploads = [];	
	            for(let i=0;i<totalFilesToUpload; i++) {
		            uploads.push(uploadFile(fileField.files[i]));
	            }  
                //********************************************************************/
                document.getElementById("addNewPatientModalClose").style.display = "block";
            }
            if(data.msg=="duplicate"){
                alert("Ce patient existe")
            }
        })
        .catch(e=>console.log(e));
    }
}

function loadPatients(){
    document.getElementById('listOfPatientsPlace').innerHTML = "";
    fetch("/app/SEPConnect/listPat",{method:'POST',body:JSON.stringify({for:targetUserMail.toString()}),contentType:'application/json'})
    .then(res=>res.json())
    .then((data)=>{
        if(data.msg=="success"){
            arrpt = data.liste.split('///');
            arrpt.pop();
            arrpt.forEach(element => {
                datAjoutP=element.split('&&')[0];
                idP=element.split('&&')[1];
                mq = `
                <div class="elem" style="width: 98%;height: 50px;background-color: #eee;border: solid 1px;border-radius: 10px;margin-top: 5px;margin-left: 10px;">
                    <table style="width:100%;">
                      <tr>
                        <td style="width:33%;"><div style="float: left;margin-left: 10px;">${datAjoutP}</div></td>
                        <td style="width:33%;"><div style="text-align: center;">${idP}</div></td>
                        <td style="width:33%;">
                          <table style="width:74px;float: right;">
                            <tr>
                              <td style="width:37px !important;">
                                <div style="width: 35px;height: inherit;margin-top: 2px;">
                            <svg onclick="targetPat='${idP}';consulterPat();" class="choices1" style="border-radius: 22px; width: 35px;height:35px;" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 300 300" style="enable-background:new 0 0 300 300;" xml:space="preserve">
<g> <g><g><rect x="96.05" y="116.882" width="86.018" height="15.562"/>
      <rect x="96.05" y="145.705" width="86.018" height="15.562"/>
      <path d="M149.997,0C67.157,0,0,67.157,0,150c0,82.841,67.157,150,149.997,150C232.841,300,300,232.838,300,150
        C300,67.157,232.841,0,149.997,0z M170.609,62.066l25.075,28.027h-25.075V62.066z M159.666,214.335H93.56
        c-9.456,0-17.115-7.659-17.115-17.113V71.024c0-9.451,7.659-17.113,17.115-17.113h61.487v51.743h47.598v63.489
        c-0.163-0.005-0.322-0.026-0.488-0.026c-7.441,0-14.436,1.924-20.534,5.294H96.05v15.562h69.53
        c-3.815,6.378-6.046,13.808-6.046,21.768C159.534,212.618,159.615,213.474,159.666,214.335z M202.158,243.988
        c-1.084,0-2.155-0.054-3.211-0.163c-0.371-0.036-0.724-0.112-1.089-0.158c-0.682-0.091-1.362-0.176-2.031-0.314
        c-0.438-0.086-0.861-0.208-1.294-0.314c-0.576-0.143-1.152-0.272-1.714-0.441c-0.469-0.143-0.918-0.319-1.377-0.482
        c-0.503-0.176-1.012-0.35-1.504-0.552c-0.482-0.197-0.947-0.425-1.419-0.648c-0.444-0.207-0.892-0.41-1.323-0.638
        c-0.488-0.259-0.962-0.542-1.437-0.82c-0.384-0.228-0.773-0.456-1.146-0.7c-0.49-0.319-0.965-0.664-1.439-1.014
        c-0.327-0.239-0.656-0.477-0.975-0.729c-0.488-0.384-0.954-0.791-1.419-1.201c-0.272-0.244-0.547-0.488-0.812-0.739
        c-0.477-0.456-0.934-0.921-1.38-1.403c-0.22-0.239-0.441-0.477-0.656-0.724c-0.456-0.521-0.897-1.058-1.32-1.611
        c-0.171-0.223-0.345-0.451-0.511-0.68c-0.431-0.594-0.843-1.201-1.235-1.823c-0.13-0.207-0.254-0.415-0.379-0.622
        c-0.394-0.664-0.773-1.343-1.123-2.036c-0.088-0.176-0.174-0.366-0.262-0.542c-0.355-0.739-0.685-1.484-0.983-2.249
        c-0.057-0.153-0.109-0.303-0.166-0.456c-0.298-0.807-0.573-1.626-0.809-2.461c-0.034-0.112-0.057-0.223-0.088-0.335
        c-0.236-0.887-0.446-1.779-0.607-2.69c-0.013-0.06-0.018-0.122-0.031-0.182c-0.163-0.962-0.296-1.94-0.376-2.928
        c-0.067-0.856-0.132-1.717-0.132-2.594c0-8.393,3.25-16.023,8.525-21.768c0.537-0.589,1.097-1.154,1.675-1.701
        c0.091-0.086,0.187-0.166,0.278-0.254c0.542-0.501,1.097-0.993,1.675-1.46c5.517-4.412,12.496-7.068,20.093-7.068
        c0.163,0,0.322,0.021,0.488,0.026c8.774,0.132,16.711,3.779,22.456,9.594c0.039,0.041,0.067,0.08,0.106,0.117
        c0.674,0.695,1.325,1.408,1.935,2.158c0.083,0.101,0.156,0.213,0.236,0.314c0.555,0.695,1.092,1.408,1.587,2.148
        c0.124,0.182,0.226,0.379,0.345,0.563c0.436,0.68,0.864,1.362,1.245,2.072c0.153,0.283,0.275,0.584,0.42,0.871
        c0.319,0.633,0.641,1.266,0.918,1.919c0.163,0.389,0.288,0.801,0.438,1.196c0.215,0.578,0.449,1.149,0.633,1.748
        c0.153,0.49,0.259,1.004,0.386,1.504c0.135,0.521,0.29,1.032,0.399,1.567c0.13,0.638,0.205,1.292,0.298,1.945
        c0.057,0.41,0.145,0.814,0.184,1.232c0.112,1.079,0.166,2.173,0.166,3.278C234.404,229.521,219.937,243.988,202.158,243.988z"/>
      <polygon points="196.62,213.933 186.503,204.194 175.708,215.404 196.934,235.839 228.118,204.041 217.006,193.145       "/>
    </g></g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
                          </div>  
                              </td>
                              <td style="width:37px !important;">
                                <div style="width: 35px;height: inherit;float: right;"><svg onclick="targetPat='${idP}';supprimerPat();" class="choices2" style="border-radius: 22px;margin-top: 2px;width: 35px;height: 35px;" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink= "http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 459 459" style="enable-background:new 0 0 459 459;" xml:space="preserve"><g><g>
                                <path d="M229.5,0C102.751,0,0,102.751,0,229.5S102.751,459,229.5,459S459,356.249,459,229.5S356.249,0,229.5,0z M307.105,271.629
                                c9.797,9.797,9.797,25.68,0,35.477c-4.898,4.898-11.318,7.347-17.738,7.347c-6.42,0-12.84-2.449-17.738-7.347L229.5,264.977
                                l-42.128,42.129c-4.898,4.898-11.318,7.347-17.738,7.347c-6.42,0-12.84-2.449-17.738-7.347c-9.797-9.796-9.797-25.68,0-35.477
                                l42.129-42.129l-42.129-42.129c-9.797-9.797-9.797-25.68,0-35.477s25.68-9.797,35.477,0l42.128,42.129l42.128-42.129
                                c9.797-9.797,25.68-9.797,35.477,0c9.797,9.796,9.797,25.68,0,35.477l-42.13,42.129L307.105,271.629z"/>
                                </g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
                                </div>
                              </td>
                            </tr>
                        </table>
                        </td>
                      </tr>
                    </table>
                  </div>
                `;
                document.getElementById('listOfPatientsPlace').innerHTML += mq;
            });
        }
        if(data.msg=="empty"){
            document.getElementById('listOfPatientsPlace').innerHTML='<h5 style="text-align:center;">La liste des patients est vide</h5>'
        }
        if(data.msg=="failure"){
            alert('une erreur est survenue.. ressayer ultérieurement')
        }
    })
    .catch(e=>console.log(e));   
}

function supprimerPat(){
    document.getElementById('modalDelPat').style.display = 'block';
}

function confirmDeletingPat(){
    fetch("/app/SEPConnect/SEPconnectDelPat",{method:'POST',body:JSON.stringify({targDel:targetPat.toString(),deleter:targetUserMail}),contentType:'application/json'})
    .then(res=>res.json())
    .then((data)=>{
        if(data.msg == 'success'){
            loadPatients();
            document.getElementById('modalDelPat').style.display='none';
        }
    })
    .catch(e=>console.log(e));
    window.location.reload();
}

function resetAddInput(){
    document.getElementById('filesToUpload').value = '';
    document.getElementById('inputPatientID').value = '';
    document.getElementById('status').value = '';
}

function consulterPat(){
    document.getElementById('interfaceModal').style.display = 'block';
    document.getElementById('wherepat').innerHTML = `ID PATIENT: ${targetPat}`;
	putImage(1);
	updateTotal();
	setIndex(1);
    
}

function putImage(x){
	fetch("/app/SEPConnect/returnImageOriginal/"+targetPat.toString()+"/"+targetUserMail.toString(),{method: 'POST',body:JSON.stringify({mode:modeUtilisation.toString(),imgIndex : x.toString()}),contentType : "application/json"})
	.then((data) => data.blob())
	.then((imgFileOriginal)=>{document.getElementById('outputImagePreviewOriginal').src = URL.createObjectURL(imgFileOriginal);
        fetch("/app/SEPConnect/returnImageLesion/"+targetPat.toString()+"/"+targetUserMail.toString(),{method: 'POST',body:JSON.stringify({mode:modeUtilisation.toString(),imgIndex : x.toString()}),contentType : "application/json"})
        .then((data) => data.blob())
        .then((imgFileLesion)=>{
            document.getElementById('outputImagePreviewLesion').src = URL.createObjectURL(imgFileLesion);
            fetch("/app/SEPConnect/returnImageOrgane/"+targetPat.toString()+"/"+targetUserMail.toString(),{method: 'POST',body:JSON.stringify({mode:modeUtilisation.toString(),imgIndex : x.toString()}),contentType : "application/json"})
            .then((data) => data.blob())
            .then((imgFileOrgane)=>{
                document.getElementById('outputImagePreviewOrgane').src = URL.createObjectURL(imgFileOrgane);
            })
            .catch((e)=>{console.log(e);});
        })
        .catch((e)=>{console.log(e);});
    })
	.catch((e)=>{console.log(e);});
	
}

function putNone(){
	fetch('/app/SEPConnect/returnImageNone',{method: 'POST'})
	.then((data) => data.blob())
	.then((imgFile)=>{
        document.getElementById('outputImagePreviewOriginal').src = URL.createObjectURL(imgFile);
        document.getElementById('outputImagePreviewLesion').src = URL.createObjectURL(imgFile);
        document.getElementById('outputImagePreviewOrgane').src = URL.createObjectURL(imgFile);
    })
	.catch((e)=>{console.log(e);});
}

input_a_remplacer = document.getElementById('aRemplacer')
input_remplacer_par = document.getElementById('Remplacant')
valider_remplacement = document.getElementById('validerRemplacement')

input_supprimer = document.getElementById('aSupprimer')
valider_supprimer = document.getElementById('validerSuppression')

input_supprimer_plusieurs_gauche = document.getElementById('indiceGauche')
input_supprimer_plusieurs_droite = document.getElementById('indiceDroite')
valider_supprimer_plusieurs = document.getElementById('validerSuppressionPlusieurs')


valider_remplacement.addEventListener('click',(e)=>{
	e.preventDefault();
	if (input_a_remplacer.value.toString() == "" || input_a_remplacer.value.toString().split('').includes('-') || input_remplacer_par.value.toString() == "" || input_remplacer_par.value.toString().split('').includes('-')){alert('données incorrectes');}
	else{
		if (document.getElementById('finindicedimage').innerHTML== '0') {alert("pas d'images pour faire un remplacement");}
		else{
			if(parseInt(input_a_remplacer.value.toString()) > parseInt(document.getElementById('finindicedimage').innerHTML) || parseInt(input_remplacer_par.value.toString()) > parseInt(document.getElementById('finindicedimage').innerHTML)){alert('données incorrectes');}
			else {
				fetch("/app/SEPConnect/replaceImage/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST',body:JSON.stringify({mode:modeUtilisation.toString(),indx_a_remplacer:input_a_remplacer.value.toString(),indx_remplacer_par:input_remplacer_par.value.toString()}),contentType : "application/json"})
				.then((res)=> res.json())
				.then((data)=>{
				if (data.msg == 'success') {
					setIndex();
					input_a_remplacer.value = '';
					input_remplacer_par.value = '';
				}
				}).catch((e)=>{console.log(e);});
			}
		}
	}
});

valider_supprimer.addEventListener('click',(e)=>{
	e.preventDefault();
	if(input_supprimer.value.toString() == "" || input_supprimer.value.toString().split('').includes('-')){alert('données incorrectes');}
	else{
		if (document.getElementById('finindicedimage').innerHTML == '0') {alert("pas d'images pour faire une suppression");}
		else{
			if (parseInt(input_supprimer.value.toString()) > parseInt(document.getElementById('finindicedimage').innerHTML)){alert('données incorrectes');}
			else{
				fetch("/app/SEPConnect/deleteOne/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST',body:JSON.stringify({mode:modeUtilisation.toString(),deleted:input_supprimer.value.toString()}),contentType : "application/json"})
				.then((res)=> res.json())
				.then((data)=>{
				if (data.msg == 'success') {
					updateTotal();
					input_supprimer.value = '';
				}
				}).catch((e)=>{console.log(e);});
			}
		}
	}
});

valider_supprimer_plusieurs.addEventListener('click',(e)=>{
	e.preventDefault();
	
	if (input_supprimer_plusieurs_gauche.value.toString() == "" || input_supprimer_plusieurs_droite.value.toString() == "" || input_supprimer_plusieurs_gauche.value.toString().split('').includes('-') || input_supprimer_plusieurs_droite.value.toString().split('').includes('-')) {alert('données incorrectes');}
	else{
		
		if (document.getElementById('finindicedimage').innerHTML == '0') {alert("pas d'images pour faire une suppression");}
		else{
			if(parseInt(input_supprimer_plusieurs_gauche.value.toString()) > parseInt(document.getElementById('finindicedimage').innerHTML) || parseInt(input_supprimer_plusieurs_droite.value.toString()) > parseInt(document.getElementById('finindicedimage').innerHTML)){alert('données incorrectes');}
			else
				{fetch("/app/SEPConnect/deleteMany/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST',body:JSON.stringify({mode:modeUtilisation.toString(),left:input_supprimer_plusieurs_gauche.value.toString(),right:input_supprimer_plusieurs_droite.value.toString()}),contentType : "application/json"})
				.then((res)=> res.json())
				.then((data)=>{
					if (data.msg == 'success') {
						updateTotal();
						input_supprimer_plusieurs_gauche.value = '';
						input_supprimer_plusieurs_droite.value = '';
					}
				}).catch((e)=>{console.log(e);});
			}
		}
	}
});

function setIndex(){
	target1 = document.getElementById('indicedimage');
	target1.innerHTML = currentImage.toString();
	putImage(currentImage)
}

function updateTotal(){
	target2 = document.getElementById('finindicedimage');
	fetch("/app/SEPConnect/returnTotalImages/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST',body:JSON.stringify({mode:modeUtilisation.toString()}),contentType:"application/json"})
		.then((res)=> res.json())
		.then((data)=>{
			target2.innerHTML = data.lenF;
			if (target2.innerHTML.toString() == '0') {putNone();}
			else{currentImage=1;setIndex();}
		}).catch((e)=>{console.log(e);});
}

document.getElementById('allerdroite').addEventListener('click',(e)=>{
	e.preventDefault();
	document.getElementById('allergauche').disabled=false;
	currentImage += 1;
	if (currentImage>parseInt(document.getElementById('finindicedimage').innerHTML.toString())) {
		currentImage = parseInt(document.getElementById('finindicedimage').innerHTML.toString());
		setIndex();
		document.getElementById('allerdroite').disabled = true;
	}else{
		setIndex();
	}
});

document.getElementById('allergauche').addEventListener('click',(e)=>{
	e.preventDefault();
	document.getElementById('allerdroite').disabled=false;
	currentImage -= 1;
	if (currentImage<1) {
		currentImage = 1;
		setIndex();
		document.getElementById('allergauche').disabled = true;
	}else{
		setIndex();
	}
});

document.getElementById('btnSegmentation').addEventListener('click',(e)=>{
	e.preventDefault();
	modeUtilisation = 2;
	document.getElementById('msgloadz').innerHTML = "Segmentation en cours, veuillez patienter";
	document.getElementById('loadz').style.display = 'block';
	fetch("/app/SEPConnect/segmenter/",{method:'POST',body:JSON.stringify({pat:targetPat.toString(),usr:targetUserMail.toString()}),contentType:'application/json'})
	.then((res)=>res.json())
	.then((data)=>{
		if(data.msg == 'success'){
			document.getElementById('msgloadz').innerHTML = "";
			document.getElementById('loadz').style.display = 'none';
			document.getElementById('btnSegmentation').disabled = true;
			document.getElementById('btnReconstruction3d').disabled = false;
			updateTotal();
			currentImage = 1;
			setIndex();
		}
        if(data.msg == 'nooriginal'){
            alert('erreur: aucune image originale trouvée');
        }
    })
	.catch((e)=>{console.log(e);});
});

document.getElementById('btnReconstruction3d').addEventListener('click',(e)=>{
	e.preventDefault();
	document.getElementById('loadz').style.display = 'block';
	document.getElementById('msgloadz').innerHTML = "Reconstruction 3D en cours, veuillez patienter";
	fetch("/app/SEPConnect/construction3d/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST'})
	.then((res)=>res.json())
	.then((data)=>{
		if(data.msg == 'success'){
			document.getElementById('msgloadz').innerHTML = "Chargement du modèle 3D 'Lésion', veuillez patienter";
			fetch("/app/SEPConnect/download3dfile/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'GET'})
			.then(res=>res.blob())
			.then(blob100 => {
				mdlINFX = URL.createObjectURL(blob100);
				document.getElementById('msgloadz').innerHTML = "Chargement du modèle 3D 'Organe', veuillez patienter";
				fetch("/app/SEPConnect/download3dfile2/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'GET'})
				.then(res=>res.blob())
				.then(blob200=>{
					mdlPOUM = URL.createObjectURL(blob200);
					document.getElementById('superModalx').style.display = 'block';
					document.getElementById('c').style.display='block';
					setTauxInfection(targetPat);
					document.getElementById('loadz').style.display = 'none';
					document.getElementById('msgloadz').innerHTML = "";
					mainXYZ(mdlINFX,mdlPOUM);
				}).catch((e)=>{console.log(e);});
        	}).catch((e)=>{console.log(e);});
		}
		if (data.msg == 'failed') {
			alert('aucune image segmentée');
			document.getElementById('loadz').style.display = 'none';
			document.getElementById('msgloadz').innerHTML = "";
		}
	})
	.catch((e)=>{console.log(e);});
});

document.getElementById('btnSegmRecons').addEventListener('click',(e)=>{
	e.preventDefault();
	modeUtilisation = 2;
	document.getElementById('msgloadz').innerHTML = "Segmentation en cours, veuillez patienter";
	document.getElementById('loadz').style.display = 'block';
	fetch("/app/SEPConnect/segmenter/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST'})
	.then((res)=>res.json())
	.then((data)=>{
		if(data.msg == 'success'){
			document.getElementById('btnReconstruction3d').disabled = false;
			document.getElementById('msgloadz').innerHTML = "Reconstruction 3D en cours, veuillez patienter";
			updateTotal();
			setIndex(1);
			fetch("/app/SEPConnect/construction3d/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST'})
			.then((res)=>res.json())
			.then((data)=>{
				document.getElementById('msgloadz').innerHTML = "Chargement du modèle 3D 'Lésion', veuillez patienter";
				if(data.msg == 'success'){
					document.getElementById('loadz').style.display = '';
					fetch("/app/SEPConnect/download3dfile/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'GET'})
					.then(res=>res.blob())
					.then(blob101 => {
					mdlINFXd = URL.createObjectURL(blob101);
					document.getElementById('msgloadz').innerHTML = "Chargement du modèle 3D 'Organe', veuillez patienter";
					fetch("/app/SEPConnect/download3dfile2/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'GET'})
					.then(res=>res.blob())
					.then(blob201=>{
						mdlPOUMd = URL.createObjectURL(blob201);
						document.getElementById('loadz').style.display = 'none';
						document.getElementById('msgloadz').innerHTML = "";
						document.getElementById('superModalx').style.display = 'block';
						document.getElementById('c').style.display='block';
						setTauxInfection(targetPat);
						mainXYZ(mdlINFXd,mdlPOUMd);
					}).catch((e)=>{console.log(e);});
        		}).catch((e)=>{console.log(e);});
				}
				if (data.msg == 'failed') {
					alert('aucune image segmentée');
					document.getElementById('loadz').style.display = 'none';
					document.getElementById('msgloadz').innerHTML = "";
				}
			}).catch((e)=>{console.log(e);});
		}})
	.catch((e)=>{console.log(e);});
});

function setTauxInfection(ssinfx){
	fetch("/app/SEPConnect/getInfectionRate/"+targetPat.toString()+"/"+targetUserMail.toString(),{method:'POST',body:JSON.stringify({requested:ssinfx.toString()}),contentType:'application/json'})
	.then(res=>res.json())
	.then((data)=>{
		document.querySelector('#resTauxInfx').innerHTML = `Taux d'infection : ${data.fin} %`;
	}).catch((e)=>{console.log(e);});
}

document.getElementById('closeSuperModal').addEventListener('click',(e)=>{
	e.preventDefault();
	document.getElementById('c').style.display = 'none';
	document.getElementById('superModalx').style.display = 'none';
	
});