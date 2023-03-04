(function(){
    let url = window.location.href;
    let url_str = new URL(url);
    let auth = url_str.searchParams.get("auth");
    let profile = document.getElementById("nav-profile");
    let login = document.getElementById("nav-login");

    if(auth === "true"){
        profile.style.display = "list-item";
    }
    else{
        login.style.display = "list-item";
    }
})();
function navigate()
{
    let url = window.location.href;
    let url_str = new URL(url);
    let auth = url_str.searchParams.get("auth");
    if(auth == null) auth = "false"; 
    let link = event.target.id;

    location.href = `${link}?auth=${auth}`;
}
function setUrl(){
    let url = window.location.href;
    let url_str = new URL(url);
    let auth = url_str.searchParams.get("auth");
    if(auth == null) auth = "false"; 
    let link;
    if(auth==="true") link = event.target.classList[2];
    else link = event.target.classList[1];
    location.href = `${link}?auth=${auth}`;
}