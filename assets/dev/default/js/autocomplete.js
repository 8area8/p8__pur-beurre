import '../../vendor/autocomplete/jquery-ui.scss';
import '../../vendor/autocomplete/jquery-ui.js';


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

$('input').autocomplete({
    source: function (req, response) { // les deux arguments représentent les données nécessaires au plugin
        $.ajax({
            type: "POST",
            url: window.product_names_url, // on appelle le script JSON
            dataType: 'json', // on spécifie bien que le type de données est en JSON
            data: {
                starts_with: $('#input').val(), // on donne la chaîne de caractère tapée dans le champ de recherche
                max_len: 15
            },

            success: function (datas) {
                console.log("success")
                response(datas.names)
            }
        });
    }
});