
function openSideMenu() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeSideMenu() {
  document.getElementById("mySidenav").style.width = "0";
}
////////////////////////////////////////////////////////////////////////////////
document.querySelector('#logoutbtn').addEventListener('click',(e)=>{
	e.preventDefault();
	fetch('/admin/logout',{method:'POST'})
	.then((response)=>{         
		if(response.redirected){
		window.location.href = response.url;
		}
	})
	.catch((e)=>{
		console.log(e);
	});
});
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}