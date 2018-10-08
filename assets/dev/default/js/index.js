import '../css/styles.scss'

document.addEventListener("DOMContentLoaded", function (event) {
    // BASE TEST
    var body = document.querySelector("body");
    body.innerHTML = "<p>Hello world ok?</p>";

    // HTTPREQUEST
    var httpRequest;
    var content;
    var divChild;
    function newcelery() {
        httpRequest = new XMLHttpRequest();
        httpRequest.onreadystatechange = function () {
            console.log(httpRequest);
            if (httpRequest.readyState == 4) {
                if (httpRequest.status === 200) {
                    content = JSON.parse(httpRequest.responseText).resp;
                    divChild = document.createElement('div');
                    divChild.innerHTML = content;
                    body.appendChild(divChild);
                }
            }
        }
        httpRequest.open("GET", window.func_celery);
        httpRequest.send();
    }

    // BUTTON AN BUTTON-EVENT
    body.innerHTML += "<button class='celery'>celery event</button>";
    var celery = document.getElementsByClassName('celery')[0];
    celery.addEventListener('click', (event) => {
        newcelery();
    })
});