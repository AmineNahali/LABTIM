settings_focus = '';
delete_focus = '';
refreshApps();


function refreshApps(){
	fetch('/admin/listApps',{method:'POST'})
	.then(res=>res.json())
	.then((data)=>{
		if(data.n.toString() != '0'){
			i=0;
			data.l.split('///').forEach(element => {
				if(i < parseInt(data.n)){

				document.getElementById(`app_${i}`).style.visibility = 'visible';
				nnn = element.split('&&&')[0];
				rrr = element.split('&&&')[1];
				document.getElementById(`nom__App${i}`).innerHTML ="Nom: " + nnn ;
				document.getElementById(`route__App${i}`).innerHTML ="Route: " + rrr ;
				var placeOfImage = document.getElementById("imageOfApp"+i.toString());
				fetch("/admin/appImg/"+nnn,{method:'GET'})
				.then(res=>res.blob())
				.then((data)=>{
					placeOfImage.src = URL.createObjectURL(data);
				})
				.catch((e)=>{console.log(e);});
				i++;
				}
			});
		}
		else{
			document.getElementById('aucuneApp').innerHTML = 'Aucune Application';
		}
	})
	.catch((e)=>{console.log(e);});
}

function closeAddApp(){
	document.getElementById("modalAddApp").style.display = 'none';
}

function addApp(){
	__nom = document.getElementById("donnee_nomApp").value.toString();
	__route = document.getElementById("donnee_routeApp").value.toString();
	__ip = document. getElementById('donnee_ipApp').value.toString();
	__port = document. getElementById('donnee_portApp').value.toString();
	__desc = document.getElementById("donnee_descApp").value.toString();
	__dev = document.getElementById("donnee_devApp").value.toString();
	__devc = document.getElementById("donnee_devcontactApp").value.toString();

	if(__nom != "" && __route != ""  && __ip != ""  && __port != "" && __desc != "" && __dev != "" && __devc != "" && document.getElementById("donnee_logoApp").files.length != 0 && document.getElementById("donnee_demoApp").files.length != 0){
		fetch('/admin/addApp',{method:'POST',body:JSON.stringify({input_name:__nom,input_route:__route,input_ip:__ip,input_port:__port,input_description:__desc,input_dev:__dev,input_devcontact:__devc}),contentType:'application/json'})
		.then(res=>res.json())
		.then((data)=>{
			if (data.msg == 'success'){
				console.log('success details');
				inputFLogo = document.getElementById('donnee_logoApp');
				formData1 = new FormData();
				formData1.append('file',inputFLogo.files[0]);
				fetch("/admin/uploadLogo/"+__nom,{method:'POST',body:formData1})
				.then(res=>res.json())
				.then((data)=>{
					if(data.msg == 'success'){
						console.log('success logo');
						inputFDemo = document.getElementById('donnee_demoApp');
						formData2 = new FormData();
  						formData2.append('file', inputFDemo.files[0]);
						fetch("/admin/uploadDemo/"+__nom,{method:'POST',body:formData2})
						.then(res=>res.json())
						.then((data)=>{
							if(data.msg == 'success'){
								console.log('success demo');
								// cleanup
								document. getElementById('donnee_nomApp').value = '';
								document. getElementById('donnee_routeApp').value = '';
								document. getElementById('donnee_descApp').value = '';
								document. getElementById('donnee_ipApp').value = '';
								document. getElementById('donnee_portApp').value = '';
								document. getElementById('donnee_devApp').value = '';
								document. getElementById('donnee_devcontactApp').value = '';
								document. getElementById('donnee_logoApp').value = '';
								document. getElementById('donnee_demoApp').value = '';
								//hide modal and refresh apps
								document.getElementById("modalAddApp").style.display = 'none';
								window.location.reload();
								refreshApps();
							}
						})
					}
				})
			}
		}).catch((e)=>{console.log(e);})
	}else{
		alert("svp verifier vos données");
	}
}

function closeConfApp(){
	document.getElementById('modalConfApp').style.display = 'none';
	settings_focus='';
}


function showSetApp(){
	
	target_config = document.getElementById('nom__App'+settings_focus).innerHTML.toString().substring(5);
	console.log("target_config is :"+target_config);
	fetch("/admin/appInfo",{method:'POST',body:JSON.stringify({identifiant:target_config}),contentType:'application/json'})
	.then(res=>res.json())
	.then((data)=>{
		if (data.msg == 'success'){
			document.getElementById('conf_nomApp').placeholder = data.conf_nomApp;
			document.getElementById('conf_routeApp').placeholder = data.conf_routeApp;
			document.getElementById('conf_ipApp').placeholder = data.conf_ipApp;
			document.getElementById('conf_portApp').placeholder = data.conf_portApp ;
			document.getElementById('conf_descApp').placeholder = data.conf_descApp;
			document.getElementById('conf_devApp').placeholder = data.conf_devApp;
			document.getElementById('conf_devcontactApp').placeholder = data.conf_devcontactApp;
			//afficher modal
			document.getElementById('modalConfApp').style.display = 'block';
		}
		else{
			console.log('failure /appInfo');
		}
	})
	.catch(e=>console.log(e));
}


function confApp(){
	//prendre les donnees
	targ = document.getElementById('conf_nomApp').getAttribute("placeholder").toString();
	confnom = document.getElementById('conf_nomApp').value.toString();
	confroute = document.getElementById('conf_routeApp').value.toString();
	confip = document.getElementById('conf_ipApp').value.toString();
	confport = document.getElementById('conf_portApp').value.toString();
	confdesc = document.getElementById('conf_descApp').value.toString();
	confdev = document.getElementById('conf_devApp').value.toString();
	confcontactdev = document.getElementById('conf_devcontactApp').value.toString();
	// fill in the blanks
	if (confnom ==""){confnom=document.getElementById('conf_nomApp').getAttribute("placeholder").toString();}
	if (confroute ==""){confroute=document.getElementById('conf_routeApp').getAttribute("placeholder").toString();}
	if (confip ==""){confip=document.getElementById('conf_ipApp').getAttribute("placeholder").toString();}
	if (confport ==""){confport=document.getElementById('conf_portApp').getAttribute("placeholder").toString();}
	if (confdesc ==""){confdesc=document.getElementById('conf_descApp').getAttribute("placeholder").toString();}
	if (confdev ==""){confdev=document.getElementById('conf_devApp').getAttribute("placeholder").toString();}
	if (confcontactdev ==""){confcontactdev=document.getElementById('conf_devcontactApp').getAttribute("placeholder").toString();}
	//Validation
	bodyObj = {v0:targ,v1:confnom,v2:confroute,v3:confip,v4:confport,v5:confdesc,v6:confdev,v7:confcontactdev}
	console.log(JSON.stringify(bodyObj));
	fetch("/admin/appconfig",{method:'POST',body:JSON.stringify(bodyObj),contentType:'application/json'})
	.then(res=>res.json())
	.then((data)=>{
		if (data.msg == "success"){
			console.log("data updated")
		}
	}).catch((e)=>{console.log(e);});
	//Mise à jour du Logo
	if(document.getElementById("conf_logoApp").files.length != 0){
		inputConfLogo = document.getElementById("conf_logoApp");
		formData1 = new FormData();
		formData1.append('file',inputConfLogo.files[0]);
		fetch("/admin/uploadLogo/"+confnom.toString(),{method:'POST',body:formData1})
		.then(res=>res.json())
		.then((data)=>{
			if (data.msg == "success"){
				console.log("logo updated !");
			}
		}).catch((e)=>{console.log(e);});
	}
	//Mise à jour du Demo
	if(document.getElementById("conf_demoApp").files.length != 0){
		inputConfDemo = document.getElementById("conf_demoApp");
		formData1 = new FormData();
		formData1.append('file',inputConfDemo.files[0]);
		fetch("/admin/uploadDemo/"+confnom.toString(),{method:'POST',body:formData1})
		.then(res=>res.json())
		.then((data)=>{
			if (data.msg == "success"){
				console.log("demo updated !");
			}
		}).catch((e)=>{console.log(e);});
	}
	refreshApps();
	target_config = '';
	document.getElementById("modalConfApp").style.display = "none";
	refreshApps();
	window.location.reload();
}

function showDelApp(){
	document.getElementById("modalDelApp").style.display = 'block';
}
function confirmDeletingApp(){
	targdel = document.getElementById('nom__App'+delete_focus).innerHTML.toString().substring(5);
	fetch("/admin/deleteApp",{method:'POST',body:JSON.stringify({"target":targdel}),contentType:'application/json'})
	.then(res=>res.json())
	.then((data)=>{
		if(data.msg == 'success'){
			alert(`${targdel} est supprimée avec succès.`);
		}else{
			alert("suppression échouée, vérifiez votre connexion");
		}
	})
	.catch((e)=>{console.log(e);});
	delete_focus = '';
	document.getElementById("modalDelApp").style.display = 'none';
	refreshApps();
	window.location.reload();
}