function allow() {
        
    var visitor = document.getElementById('visitor-name').value.trim().toLowerCase();
    console.log(visitor)
    var phone = document.getElementById('phone-number').value.trim().toLowerCase();
    console.log(phone)
    var faceid;
    
    console.log(faceid);
    console.log(s3key)
    apigClient = apigClientFactory.newClient();
    console.log('initialized client')
    var params = {};
    var body = {
        'message' : {    
                        'name': visitor,
                        'phone': phone,
                        'fileName': s3key
                    }
        }

    var additionalParams = {};

    apigClient.visitorCheckPost(params, body, additionalParams)
        .then(function (result) {
            // alert(result.data.body)
            // console.log(result)
        }).catch(function (result) {
        //error callback
    });
}

function deny(){
    // send deny message.
}