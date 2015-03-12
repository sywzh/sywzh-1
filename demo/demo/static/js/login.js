
function funclogin(){
	var msglogin = document.getElementById("login");
	msglogin.style.backgroundColor='#fff';
	var msgreg = document.getElementById("reg");
	msgreg.style.backgroundColor='rgba(0,0,0,0)';
	var logintext = document.getElementById("logintext");
	logintext.style.display='block';
	var regtext = document.getElementById("regtext");
	regtext.style.display='none';
}

function funcreg(){
	var msglogin = document.getElementById("login");
	msglogin.style.backgroundColor='rgba(0,0,0,0)';
	var msgreg = document.getElementById("reg");
	msgreg.style.backgroundColor='#fff';
	var logintext = document.getElementById("logintext");
	logintext.style.display='none';
	var regtext = document.getElementById("regtext");
	regtext.style.display='block';
}

