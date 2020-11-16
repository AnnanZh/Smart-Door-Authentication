function on_submit() {
            
    var apigClient = apigClientFactory.newClient();
    var params = {
        //This is where any header, path, or querystring request params go.
    };

    var link = window.location.href;
    var faceId

    if(link){
        params = link.split('?')[1]
        temp = params.split('=')
        if(temp[0] == "faceId")
            faceId = temp[1]  
    }
    var body = {
        //This is where you define the body of the request
        'message': {
            'otp': document.getElementById("OTP").value,
            'faceId' : faceId
        }
    }
    var additionalParams = {}

    apigClient.oTPValidatePost(params, body, additionalParams)
        .then(function (result) {
            alert(result.data.body);
        }).catch(function (result) {
        //error callback
    });
};