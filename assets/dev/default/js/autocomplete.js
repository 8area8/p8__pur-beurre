import '../../vendor/autocomplete/jquery-ui.scss';
import '../../vendor/autocomplete/jquery-ui.js';

var products;
var jqxhr = $.get(window.product_names_url, function () {
})
    .done(function () {
        console.log("success");
        products = JSON.parse(jqxhr.responseText).resp;
        $(function () {
            $("input").autocomplete({
                source: products.slice(50)
            });
        })
    })
    .fail(function () {
        console.log("error");
    });
