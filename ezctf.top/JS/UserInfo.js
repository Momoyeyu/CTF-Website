function change(){
    document.getElementById("userInfo").style.display = "none";
    document.getElementById("changeInfo").style.display = "block";
}

function closeUserInfo(){
    document.getElementById("userInfo").style.display = "none";
}

function closeChangeInfo(){
    document.getElementById("userInfo").style.display = "block";
    document.getElementById("changeInfo").style.display = "none";
}

function changeComplete(){
    const newUsernameInput = document.getElementById('newUsername');
    const newIDInput = document.getElementById('newID');
    if(newUsernameInput.value!=""){
        let usernameSpan = document.getElementById('username');
        usernameSpan.textContent = newUsernameInput.value;
    }
    if(newIDInput.value!=""){
        let IDSpan = document.getElementById('ID');
        IDSpan.textContent = newIDInput.value;
    }
    newUsernameInput.value = '';
    newIDInput.value = '';
    document.getElementById("userInfo").style.display = "block";
    document.getElementById("changeInfo").style.display = "none";
}