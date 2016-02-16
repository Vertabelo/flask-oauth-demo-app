var requestingInterval = 1000;
var trialsNumber = 60000/requestingInterval;


function doRequest() {
$.ajax({
        type : "GET",
        url : "/get-status",
        contentType: 'application/json;charset=UTF-8',
        success: function(data) {
            console.log(data)

            if (data === 'ok') {
             console.log(data)
             $.ajax({
                type: "GET",
                url: "/"
             })
             window.location.replace("/success")
            }

            if (data === 'pending') {
                trialsNumber--;
                if(trialsNumber === 0) {
                    window.location.replace("/error")
                }
                //send request after 1000ms
            setTimeout(function() {
                doRequest(); },requestingInterval);
             }


            if (data === 'error') {
                console.log(data)
            window.location.replace("/error")
            }
        }
    });
}


function runCheckingStatus() {
    doRequest();
}
