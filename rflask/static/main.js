var myImage = document.querySelector('img');

myImage.onclick = function() {
    var mySrc = myImage.getAttribute('src');
    if(mySrc === '../../static/pizza.png'){
        myImage.setAttribute('src', '../../static/spooky.png');
    } else {
        myImage.setAttribute('src', '../../static/pizza.png');
    }
}
var myButton = document.querySelector('button');
var myHeading = document.querySelector('h1');
function setUserName() {
    var myName = prompt('Please enter your name.');
    localStorage.setItem('name', myName);
    myHeading.textContent = 'Welcome to Scuffed Pizza, ' + myName + '!';
}
if(!localStorage.getItem('name')) {
    setUserName();
} else {
    var storedName = localStorage.getItem('name');
    myHeading.textContent = 'Welcome to Scuffed Pizza, ' + storedName + '!';
}
myButton.onclick = function() {
    setUserName();
}