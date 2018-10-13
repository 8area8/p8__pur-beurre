var $ = require('jquery');

var logoAccount = $('#logo-account').html();
var logoAliments = $('#logo-aliments').html();
var logoDeco = $('#logo-deconexion').html();
changeLogoNav();
function getWindowSize() {
    return $(window).width() < 990;
}
function changeLogoNav() {
    if (getWindowSize()) {
        $("#logo-search").css({ "display": "none" });
        $('#logo-account').html("Mon compte");
        $('#logo-aliments').html("Mes aliments");
        $('#logo-deconexion').html("Déconnexion");
    } else {
        $("#logo-search").css({ "display": "block" });
        $('#logo-account').html(logoAccount);
        $('#logo-aliments').html(logoAliments);
        $('#logo-deconexion').html(logoDeco);
    }
}
$(window).on('resize', function () {
    changeLogoNav();
});