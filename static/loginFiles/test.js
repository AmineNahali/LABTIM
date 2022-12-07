initAppName = getQueryVariable("initApp").toString();
var logoPlace = document.getElementById('logoOfApp');
console.log("initAppName="+initAppName);

fetch("/imgApp/"+initAppName)
.then(res=>res.blob())
.then((imgFile)=>{document.getElementById('logoOfApp').src = URL.createObjectURL(imgFile);})
.catch(e=>console.log(e));

function doLogin(){

	if(document.querySelector('#email-8816').value!="" && (document.querySelector('#email-8816').value.split('').includes('@')) && document.querySelector('#text-8357').value!=""){
		fetch('/loginVerify',{
			method: 'POST',
			redirect: 'follow',
			body: JSON.stringify({adr: document.querySelector('#email-8816').value.toString() , mdp: document.querySelector('#text-8357').value.toString(),app:initAppName}),
			contentType : "application/json"
		})
		/*.then((response)=>{         
			if(response.redirected){
				window.location.href = response.url;
			}
		})*/
		.then(res=>res.json())
		.then((data)=>{
			if (data.msg == "escape") {window.location.href = data.urlto;}
			else {alert("vérifiez vos identifiants et réssayez")}
		})
		.catch((e)=>{
			console.log(e);
		});
	}else{
		alert("e-mail/mot-de-passe non valide");
	}
}

function doSignUp(){
	
	let signup_date = new Date().toISOString().slice(0, 10);
	const signup_Code = randomString(20);
	
	if(document.querySelector('#name-ec05').value!="" && document.querySelector('#text-692c').value!="" && document.querySelector('#inputTel').value!="" && document.querySelector('#text-4ee5').value!="" && document.querySelector('#email-ec05').value!="" && (document.querySelector('#email-ec05').value.split('').includes('@')) 
	&& document.querySelector('#select-a07a').value !="" && document.querySelector('#text-7aa1').value != "")
	{
		document.getElementById('signupbuttonid').disabled = true;
		obj2 = {Date:signup_date.toString() , Code:signup_Code.toString() , Nom:document.querySelector('#name-ec05').value.toString() , Prenom: document.querySelector('#text-692c').value.toString() ,Tel:document.querySelector('#inputTel').value.toString(),Mail:document.querySelector('#email-ec05').value.toString(),
			CIN:document.querySelector('#text-4ee5').value.toString() , Etab:document.querySelector('#select-a07a').value.toString() ,Spec:document.querySelector('#select-57cf').value.toString(),
			Password:document.querySelector('#text-7aa1').value.toString(),app:initAppName}
		fetch('/signupUsers',{
			method: 'POST',
			redirect: 'follow',
			body: JSON.stringify(obj2),
			contentType : "application/json"
			})
		/*.then((response)=>{         
			if(response.redirected){
				window.location.href = response.url;
			}
			})*/
		.then(res=>res.json())
		.then((data)=>{
			if (data.msg == "redirected") {window.location.href = data.urlto;}
			else {alert("cet utilisateur existe dejà");}
		})
		.catch((e)=>{console.log(e);});
	}
}

function opmvr(e){
	e.preventDefault;
	smdl2.style.display = 'block';
}
function clmvr(){
	smdl2.style.display = 'none';
}
function clmvrout(e){
	if (e.target == smdl2) {
	smdl2.style.display = 'none';
	}
}

function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

function randomString(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@/*-+&@^_';
    var randomString = '';
    for (var i = 0; i < len; i++) {
        var randomPoz = Math.floor(Math.random() * charSet.length);
        randomString += charSet.substring(randomPoz,randomPoz+1);
    }
    return randomString;
}