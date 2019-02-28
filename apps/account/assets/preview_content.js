$("#id_avatar").on("change", DisplayAvatarPath);

function DisplayAvatarPath(event) {
	if (event.target.files.length === 0) {
		return;
	}
	let label = $("#avatar-label");
	label.addClass("twotone-done");
	label.addClass("blue");
	label.removeClass("twotone-add_photo_alternate");
	var files = event.target.files;
	var filename = files[0].name;
	$("#avatar-confirmation").text(`image: ${filename}.`);
}

DisplayAvatarPath();