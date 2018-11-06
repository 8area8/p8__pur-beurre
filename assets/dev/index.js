/* JS INDEX */

import './styles.scss';

import 'bootstrap';

import '../../apps/index/assets/js/creative.js';
import '../../apps/index/assets/js/logonav.js';
import '../../templates/admin/main_admin.js';
import '../../apps/autocomplete/assets/autocomplete.js';

const carrot = require('../../apps/index/assets/icons/carrot.png');
const logo = require('../../apps/index/assets/icons/logo.png');
const colette = require('../../apps/index/assets/imgs/colette.jpg');
const remy = require('../../apps/index/assets/imgs/remy.jpg');
const load = require('../../templates/admin/loading.gif');
const nutriscore_a = require('../../apps/products/assets/nutriscore/nutriscore-a.png');
const nutriscore_b = require('../../apps/products/assets/nutriscore/nutriscore-b.png');
const nutriscore_c = require('../../apps/products/assets/nutriscore/nutriscore-c.png');
const nutriscore_d = require('../../apps/products/assets/nutriscore/nutriscore-d.png');
const nutriscore_e = require('../../apps/products/assets/nutriscore/nutriscore-e.png');
const results_list = require('../../apps/products/assets/images/products_list.jpg');
const substitutes = require('../../apps/products/assets/images/substitutes.jpg');
const mentions = require('../../apps/index/assets/imgs/mentions.jpg');


/*
function celeryTest() {
    var body = document.querySelector("body");

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

    // BUTTON A BUTTON-EVENT
    var button = document.createElement('button');
    button.innerHTML = 'celery event';
    button.classList.add('celery');
    body.appendChild(button);
    var celery = document.getElementsByClassName('celery')[0];
    celery.addEventListener('click', (event) => {
        newcelery();
    })
}
*/