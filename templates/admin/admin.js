$(".generate-products-form").on("submit", function (e) {
    var image = $('<img src="{% webpack_static "loading.gif" %}" alt="chargement">');
    $(".modal-generate-corps").html(image);
});