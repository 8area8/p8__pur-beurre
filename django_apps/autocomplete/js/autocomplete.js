// IMPORTANT: This Js file is NOT used.
// It's a copie from the real file, found at assets/dev/default/js/autocomplete.js

import '../../vendor/autocomplete/jquery-ui.scss';
import '../../vendor/autocomplete/jquery-ui.js';

var autocomplete_valuesOne = [];

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
                console.log("success")
                autocomplete_valuesOne = datas.names;
                response(datas.names);
            }
        });
    },
    // change: function (event, ui) {
    //     var input = $('#input1');
    //     if (autocomplete_valuesOne.includes(input.val())) {
    //         $("#inputbutton").removeAttr("disabled");
    //     } else {
    //         $("#inputbutton").attr("disabled", true);
    //     }
    // }
});
$("#input1").on("change paste autocompleteselect input", function () {
    console.log("in 'change' function.")
    var input = $('#input1');
    if (autocomplete_valuesOne.includes(input.val())) {
        $("#inputbutton").removeAttr("disabled");
    } else {
        $("#inputbutton").attr("disabled", true);
    }
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
                console.log("success")
                autocomplete_valuesTwo = datas.names;
                response(datas.names);
            }
        });
    }
    // search: function (event, ui) {
    //     var input = $('#logo-search');
    //     if (autocomplete_values2.includes(input.val())) {
    //         Console.log("on peut chercher oui");
    //     } else {
    //         $("#logo-search").popover();
    //     }
    // }
});
$('#logo-search').keyup(function checkValueBeforeRequest(e) {
    if (e.keyCode == 13) {
        var input = $('#logo-search');
        if (autocomplete_valuesTwo.includes(input.val())) {
            console.log("on peut chercher oui");
        } else {
            console.log("Non.");
        }
    }
});

function inputIsName(input, names) {
    if (names.includes(input.val())) {
        input.prop("disabled", false);
    } else {
        input.prop("disabled", true);
    }
}