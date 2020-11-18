function on_submit() {
    console.log(document.getElementById("OTP").value);
    var apigClient = apigClientFactory.newClient();
    var params = {
        'Content-type': 'application/json',
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        "Access-Control-Allow-Credentials": 'true'
    };
    var body = {
        'message': {
            'passwd': document.getElementById("OTP").value,
            'timestamp': ""
        }
    }
    var additionalParams = {}

    apigClient.lockPost(params, body, additionalParams)
        .then(function (result) {
            alert(result.data);
        }).catch(function (result) {
        //error callback
    });
};

    // var link = window.location.href;
    // var faceId

    // if(link){
    //     params = link.split('?')[1]
    //     temp = params.split('=')
    //     if(temp[0] == "faceId")
    //         faceId = temp[1]  
    // }
