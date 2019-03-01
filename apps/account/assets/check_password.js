$("#id_password, #id_new_pass, #id_confirm_new_pass").on("change", () => {
	let password = $("#id_password");
	let confirm = $("#id_confirm_new_pass");
	let newPass = $("#id_new_pass");

	if (!validNewPass() || password.val() !== "" && confirm.val() !== newPass.val()) {
		$("#send-form").attr("disabled", true);
	} else {
		$("#send-form").removeAttr("disabled");
	}
});

function validNewPass() {
	let textBox = $("#pass-errors");
	let confirm = $("#id_confirm_new_pass").val();
	let newPass = $("#id_new_pass").val();

	if (newPass.length >= 8) {
		if (confirm === newPass) {
			textBox.text("les deux mots de passe sont confirmés.");
			textBox.addClass("good_pass_mess").removeClass("pass_mess");
			return true;
		} else {
			textBox.text("Les deux nouveaux mots de passe ne se correspondent pas.");
		}
	} else {
		textBox.text("Le nouveau mot de passe doit faire 8 caractères minimum.");
	}
	textBox.addClass("pass_mess").removeClass("good_pass_mess");
	return false;
}