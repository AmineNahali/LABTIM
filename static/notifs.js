refreshNotifs();


function refreshNotifs(){
	fetch("/admin/loadNotifs",{method:'POST'})
	.then(res=>res.json())
	.then((data)=>{
        if(data.msg == "empty"){
            document.getElementById("msgContainer").innerHTML = "Aucune notification";
        }
        if(data.msg =="success"){
            ijk=0;
            totalNotifs=parseInt(data.totNotifs.toString());
            arr = data.ls.split("///");
            arr.pop();
            arr.forEach(element => {
                if(ijk<totalNotifs){
                    _date = element.split("&&&")[0];//date
                    _code = element.split("&&&")[1];//code
                    _app = element.split("&&&")[2];//app
                    _nom = element.split("&&&")[3];//nom
                    _prenom = element.split("&&&")[4];//prenom
                    _cin = element.split("&&&")[5];//cin
                    _mail = element.split("&&&")[6];//mail
                    _tel = element.split("&&&")[7];//tel
                    _spec = element.split("&&&")[8];//spec
                    _etab = element.split("&&&")[9];//etab
                    _template = `
                    <div> <!-- BEGIN ELEMENT -->
		                <button type="button" class="collapsible"><table style="width:100%;"><td style="text-align: left;width: 33%;">${_date}</td><td style="text-align: center;width: 33%;">Demande d'inscription</td><td><td style="text-align:right;width: 33%;">▼</td></td></table></button>
		                    <!-- BEGIN CONTENT -->
		                <div class="content">
			                <div style="margin-left: 10px;">
				                <table style="width:100%">
				    	            <tr>
				    		            <td><h3>Nouvelle demande d'inscription:</h3></td><td><img style="width:25%;height:25%;float:right;margin-top:5px;margin-right:10px;" src="/imgApp/${_app}"></td>
				    	            </tr>
				                </table>
				                <table style="width: 50%;">
				    	            <tr>
				    		            <td>Code°: </td><td id="">${_code}</td>
				    	            </tr>
				    	            <tr>
				    		            <td>Nom: </td><td id="">${_nom}</td>
				    	            </tr>
				    	            <tr>
				    		            <td>Prénom: </td><td id="">${_prenom}</td>
				    	            </tr>
				    	            <tr>
				    		            <td>CIN: </td><td id="">${_cin}</td>
				    	            </tr>
				    	            <tr>
				    		            <td>Mail: </td><td id="">${_mail}</td>
				    	            </tr>
									<tr>
				    		            <td>Téléphone: </td><td id="">${_tel}</td>
				    	            </tr>
				    	            <tr>
				    		            <td>Specialité: </td><td id="">${_spec}</td>
				    	            </tr>
				    	            <tr>
				    		            <td>Etablissement: </td><td id="">${_etab}</td>
				    	            </tr>
				    	            <tr>
				    		            <td>Application: </td><td id="napp${ijk}">${_app}</td>
				    	            </tr>
				                </table><br>
				                <table style="padding-left: 20%;width: 80%;">
				    	            <tr>
				    		            <td width="40%" height="36px"><div onclick="_accepter('${_code}')" class="decision">ACCEPTER</div></td>
				    		            <td width="40%" height="36px"><div onclick="_ignorer('${_code}')" class="decision">IGNORER</div></td>
				    	            </tr>
				                </table>
			                </div><br>
		                </div> <!-- END CONTENT -->
	                </div><br> <!-- END ELEMENT -->
                    `;
                    document.getElementById("listOfNotifs").innerHTML += _template;
                    ijk++;
                }
            });
            var coll = document.getElementsByClassName("collapsible");
            var i;
            for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                });
            }
        }
    })
	.catch((e)=>{console.log(e);});
}

function _accepter(inputX){
	var today = new Date();
	var date = today.getDate()+'/'+today.getMonth()+'/'+today.getFullYear();
	// la date d'inscription dans la platforme.
	fetch("/admin/addUser",{method:'POST',body:JSON.stringify({"target":inputX.toString(),"targetDate":date.toString()}),contentType:'application/json'})
    .then(res=>res.json())
	.then((data)=>{
		if (data.msg == "success"){
			alert("Demande d'inscription n°"+inputX.toString()+" acceptée.");
			window.location.reload();
		}
	}).catch((e)=>{console.log(e);});
}

function _ignorer(inputY){
	//alert("ignored :"+inputY.toString());
	fetch("/admin/deleteNotif",{method:'POST',body:JSON.stringify({"target":inputY.toString()}),contentType:'application/json'})
	.then(res=>res.json())
	.then((data)=>{
		if (data.msg == "success"){
			alert("Demande d'inscription n°"+inputY.toString()+" rejettée.");
			window.location.reload();
		}
	}).catch((e)=>{console.log(e);});
}