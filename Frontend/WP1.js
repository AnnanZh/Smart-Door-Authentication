var start_img = document.getElementById("start_img");
var btn_deny = document.getElementById("btn_deny");
var btn_allow = document.getElementById("btn_allow");

init();

function init(){
    console.log("connected");
    var photo_uuid = get_image_uuid();
    if (photo_uuid!=""){
        var url = get_image_url(photo_uuid);
        console.log(url);
        start_img.src=url;
    }
    btn_allow.addEventListener("click", function(){
        allow();
    });
    btn_deny.addEventListener("click", function(){
        deny();
    });

}

function get_image_uuid(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const photo_uuid = urlParams.get('photo_id');
    return photo_uuid;
}

function get_image_url(photo_uuid){
    var url = "https://hw3-visitor-photos.s3.amazonaws.com/";
    url = url+photo_uuid+".jpg";
    return url;
}

function allow() {
    var visitor = document.getElementById('visitor-name').value;
    console.log(visitor);
    var phone = document.getElementById('phone-number').value;
    console.log(phone);
    var email = document.getElementById('email').value;
    console.log(email);

    apigClient = apigClientFactory.newClient();

    var params = {};
    var body = {
        'message' : {    
                    'firstname': visitor,
                    'phonenumber': phone,
                    'image_uuid': get_image_uuid(),
                    'email': email,
                }
        };

    var additionalParams = {};

    apigClient.visitorPost(params, body, additionalParams)
        .then(function (result) {
            alert(result.data);
            // console.log(result)
        }).catch(function (result) {
        //error callback
    });
}

function deny(){
    alert("visitor is denied");
    // var visitor = document.getElementById('name').value.trim().toLowerCase();
    // console.log(visitor)
    // var phone = document.getElementById('phoneNumber').value;
    // console.log(phone)

    // apigClient = apigClientFactory.newClient();

    // var params = {};
    // var body = {
    //     'message' : {    
    //                 'firstname': visitor,
    //                 'phonenumber': phone,
    //             }
    //     }

    // var additionalParams = {};

    // apigClient.visitorPost(params, body, additionalParams)
    //     .then(function (result) {
    //         alert(result.data)
    //         // console.log(result)
    //     }).catch(function (result) {
    //     //error callback
    // });
}
