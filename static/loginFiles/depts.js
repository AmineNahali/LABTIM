const modal = document.querySelector('#modal_id');
const closeBtn = document.querySelector('#closeBtn');
closeBtn.addEventListener('click',closeModal);
window.addEventListener('click',closeOutside);

function openModal(){
	modal.style.display = 'block';
}
function closeModal(){
	modal.style.display = 'none';
	$("#select-a07a").val('None');
}
function closeOutside(e){
	if (e.target == modal) {
		modal.style.display = 'none';
		$("#select-a07a").val('None');
	}
}
$(document).ready(function() {
	$("#select-a07a").select2({placeholder: 'choisir'});
});

$('#select-a07a').on("change", function (e) {
	e.preventDefault();
	var selectionza = $(this).val();
    if (selectionza == 'ajouter') {
		openModal();
    	}
});

$('#categorieEtablissement').on("change", function (e){
	e.preventDefault();
	var selection = $(this).val();
	if (selection =='privé') {
		document.getElementById("types_etablissement_publique").style.display = "none";
		document.getElementById("types_etablissement_privé").style.display = "block";
	}
	if (selection =='publique') {
		document.getElementById("types_etablissement_publique").style.display = "block";
		document.getElementById("types_etablissement_privé").style.display = "none";
	}
});

const selectCategorie = document.getElementById('categorieEtablissement');
const selectTypePrive = document.getElementById('types_etablissement_privé');
const selectTypePublique = document.getElementById('types_etablissement_publique');
const codeEtablissement = document.querySelector('#codeEtablissement');
const libelleEtablissement = document.querySelector('#libelleEtablissement');
const ButtAjoutEt = document.querySelector('#boutonajouter');

ButtAjoutEt.addEventListener('click',(e)=>{
	e.preventDefault();

	if (codeEtablissement.value != "" && libelleEtablissement.value != "") {
		if (selectCategorie.value == "privé") {
			var etObj = {code: codeEtablissement.value.toString(),libelle: libelleEtablissement.value.toString(),categorieEtablissement: "privé",typeEtablissement:selectTypePrive.value.toString()};
			fetch('/ajouterEtablissement',{
				method: 'POST',
				redirect: 'follow',
				body: JSON.stringify(etObj),
				contentType : "application/json"
			})
			/*.then((response)=>{         
			if(response.redirected){
				window.location.href = response.url;
			}
			})   */
			.then(res=>res.json())        
			.then((data)=>{
				if (data.msg == "duplicate") {alert('Etablissement existe déjà');}
				if (data.msg == "reload") {window.location.reload();}
			})
			.catch((e)=>{
				console.log(e);
			});

		}//if privé
		if (selectCategorie.value == "publique") {
			var etObj2 = {code: codeEtablissement.value.toString(),libelle: libelleEtablissement.value.toString(),categorieEtablissement: "publique",typeEtablissement:selectTypePrive.value.toString()};
			fetch('/ajouterEtablissement',{
				method: 'POST',
				redirect: 'follow',
				body: JSON.stringify(etObj2),
				contentType : "application/json"
			})
			/*.then((response)=>{         
			if(response.redirected){
				window.location.href = response.url;
			}
			})*/
			.then(res=>res.json())        
			.then((data)=>{
				if (data.msg == "duplicate") {alert('Etablissement existe déjà');}
				if (data.msg == "reload") {window.location.reload();}
			})     
			.catch((e)=>{
				console.log(e);
			});

		}//if publique
		
	}
});

fetch('/getEtablissements',{method: 'POST',redirect: 'follow',contentType : "application/json"})
.then(res => res.json())
.then((data)=>{	
	ets = data.ls.split('/');
	for (var i = 0 ; ets[i] ; i++) {
	//document.getElementById('select-a07a').options.add(new Option(ets[i] , ets[i]));		
	$("#select-a07a").append($('<option>', {value: ets[i], text: ets[i]}));	}})
.catch((e)=>{	console.log(e);});










