var $ = require('jquery');

if ($("#adminpage-flag").length > 0) {
    // run code for adminpage
    // $(document.body).append(form);
    $(".generate-products-form").on("submit", function (event) {
        var image = $(`<img src="${window.loading}" alt="chargement">`);
        $(".generate-explanations").html("Patientez environ cinq minutes...");
        $(".submit-generate-products").replaceWith(image);
    });
}