function allow() {
        
    var visitor = document.getElementById('name').value.trim().toLowerCase();
    console.log(visitor)
    var phone = document.getElementById('phoneNumber').value;
    console.log(phone)

    apigClient = apigClientFactory.newClient();

    var params = {};
    var body = {
        'message' : {    
                    'firstname': visitor,
                    'phonenumber': phone,
                }
        }

    var additionalParams = {};

    apigClient.visitorPost(params, body, additionalParams)
        .then(function (result) {
            alert(result.data)
            // console.log(result)
        }).catch(function (result) {
        //error callback
    });
}

function deny(){
    var visitor = document.getElementById('name').value.trim().toLowerCase();
    console.log(visitor)
    var phone = document.getElementById('phoneNumber').value;
    console.log(phone)

    apigClient = apigClientFactory.newClient();

    var params = {};
    var body = {
        'message' : {    
                    'firstname': visitor,
                    'phonenumber': phone,
                }
        }

    var additionalParams = {};

    apigClient.visitorPost(params, body, additionalParams)
        .then(function (result) {
            alert(result.data)
            // console.log(result)
        }).catch(function (result) {
        //error callback
    });
}
