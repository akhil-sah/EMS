var usernameEle = document.getElementById('username').children[1];
var firstNameEle = document.getElementById('firstName').children[1];
var emailEle = document.getElementById('email').children[1];
var passwordEle = document.getElementById('password').children[1];
var password2Ele = document.getElementById('password2').children[1];
var submitButtonEle = document.getElementById('submitButton');

var usernameErrorMessage = document.getElementById('usernameErrorMessage');
var firstNameErrorMessage = document.getElementById('firstNameErrorMessage');
var emailErrorMessage = document.getElementById('emailErrorMessage');
var passwordErrorMessage = document.getElementById('passwordErrorMessage');
var password2ErrorMessage = document.getElementById('password2ErrorMessage');


/*
usernameEle.addEventListener('keyup',function(e){
	var text = this.value;
	text = text.trim();
	this.value = text;
	var errorCode = 0;
	for(let i = 0;i<text.length;i++){
		if((text[i] > 96 && text[i] < 123 ) || (text[i] > 64 && text[i] < 91) || (text[i] > 47 && text[i] < 58) || text[i] == 95){
			errerCode = 0;
		}
		else{
			errorCode = 1;
			break;
		}
	}
	if(text == '' || text.length > 150){
		errorCode = 1;
	}

	if(errorCode == 1){
		usernameErrorMessage.innerText = "Username doesn't abide to constraints."
	}
	else{
		usernameErrorMessage.innerText = '';
	}

});
*/


submitButtonEle.addEventListener('click',function(ev){
	p1 = passwordEle.value;
	p2 = password2Ele.value;
	p1 = p1.trim();
	p2 = p2.trim();
	if(p1.length < 6){
		ev.preventDefault();
		passwordErrorMessage.innerText = "Password too short";
	}
	if(p1 != p2){
		ev.preventDefault();
		password2ErrorMessage.innerText = "Password do not match";
	}
	passwordEle.value = p1;
	password2Ele.value = p2;
});