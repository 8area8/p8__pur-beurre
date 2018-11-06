import './vendor/autocomplete/jquery-ui.scss';
import './vendor/autocomplete/jquery-ui.js';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});


var autocomplete_valuesOne = [];

$('#input1').autocomplete({
    source: function (req, response) {
        $.ajax({
            type: "POST",
            url: window.product_names_url,
            dataType: 'json',
            data: {
                starts_with: $('#input1').val(),
                max_len: 15
            },

            success: function (datas) {
                autocomplete_valuesOne = datas.names;
                response(datas.names);
            }
        });
    },
});

var autocomplete_valuesTwo = [];

$('#logo-search').autocomplete({
    source: function (req, response) {
        $.ajax({
            type: "POST",
            url: window.product_names_url,
            dataType: 'json',
            data: {
                starts_with: $('#logo-search').val(),
                max_len: 15
            },

            success: function (datas) {
                autocomplete_valuesTwo = datas.names;
                response(datas.names);
            }
        });
    }
});