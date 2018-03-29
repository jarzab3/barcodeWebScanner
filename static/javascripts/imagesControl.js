var $ = jQuery;

// $(document).load(function () {

var e0 = document.getElementById("element0");
var e1 = document.getElementById("element1");
var e2 = document.getElementById("element2");
var e3 = document.getElementById("element3");


// var button = document.getElementById("next");


var arrayOfImages = [e0, e1, e2, e3];

var index = 0;

// arrayOfImages[index].style.border = "solid 1px red";


function nextElement() {


    arrayOfImages[index].style.border = "none";


    if (index == arrayOfImages.length - 1) {
        index = 0;
    } else {
        index++;
    }


    arrayOfImages[index].style.border = "solid 1px red";


}



function requestAPI(arg) {

    $.getJSON($SCRIPT_ROOT + '/_changeImage', {
        // apiQ0: $('a#sendApi').text()
        apiQ0: arg

    }, function (data) {

        console.log(data.result);

    });

    return false;
}


// });