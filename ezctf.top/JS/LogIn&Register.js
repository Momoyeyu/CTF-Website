function openLoginPopup() {
    document.getElementById("loginPopup").style.display = "block";
}

function closeLoginPopup() {
    document.getElementById("loginPopup").style.display = "none";
}

function openRegisterPopup() {
    document.getElementById("loginPopup").style.display = "none";
    document.getElementById("registerPopup").style.display = "block";
}

function closeRegisterPopup() {
    document.getElementById("registerPopup").style.display = "none";
}

function submitLogin() {
    // 在这里处理登录逻辑
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
    // 此处可以发送登录请求或进行其他处理
    alert(`登录成功！用户名: ${username}`);
    closeLoginPopup();
}

function submitRegister() {
    const username = document.getElementById("registerUsername").value;
    const id = document.getElementById("registerId").value;
    const password = document.getElementById("registerPassword").value;
    const confirmPassword = document.getElementById("registerConfirmPassword").value;
    if(password==confirmPassword){
        // 此处可以发送注册请求或进行其他处理
        alert(`注册成功！用户名: ${username}`);
        closeRegisterPopup();
    }
    else{
        document.getElementById("registerPassword").value="";
        document.getElementById("registerConfirmPassword").value="";
        alert("密码设置失败，请重新设置密码！");
    }
}