$("#acceso_ilimitado").click(function() {
	// Change button color
	$(this).addClass("btn-success");
	$(this).removeClass("btn-secondary");

	$("#acceso_limitado").addClass("btn-secondary");
	$("#acceso_limitado").removeClass("btn-success");

	// Hide Limited Access options
	$("#multiCollapseExample2").collapse('hide');
});

$("#acceso_limitado").click(function() {
	// Change button color
	$(this).addClass("btn-success")
	$(this).addClass("btn-secondary")

	$("#acceso_ilimitado").addClass("btn-secondary");
	$("#acceso_ilimitado").removeClass("btn-success");
});

function verificar() {
	$(".input").each(function () {
		if (isNaN($(this).val())) {

		}
	});
}

