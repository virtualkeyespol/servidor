$("#acceso_ilimitado").click(function() {
	// Change input value
	$("#acceso-input").val("true");

	// Change button color
	$(this).addClass("btn-success");
	$(this).removeClass("btn-secondary");

	$("#acceso_limitado").addClass("btn-secondary");
	$("#acceso_limitado").removeClass("btn-success");

	// Hide Limited Access options
	$("#multiCollapseExample2").collapse('hide');
});

$("#acceso_limitado").click(function() {
	// Change input value
	$("#acceso-input").val("false");

	// Change button color
	$(this).addClass("btn-success")
	$(this).addClass("btn-secondary")

	$("#acceso_ilimitado").addClass("btn-secondary");
	$("#acceso_ilimitado").removeClass("btn-success");
});

$("#checkbox").click(function() {
	var value = $("#MULTIUSO").val();
	if (value === "true") {
		$("#MULTIUSO").val("false");
	} else {
		$("#MULTIUSO").val("true");
	}
});

$("#compartir-btn").click(function() {
	if (verificar()) {
		$("#compartir-form").submit();
	} else {
		alert("Ingrese todos los campos");
	}
});

function verificar() {
	var value = true;
	$(".input").each(function () {
		if (isNaN($(this).val()) == false) {
			value = false;
		}
	});
	var acceso_input = $("#acceso-input").val();
	if (acceso_input === "false") {
		$(".sub-input").each(function () {
			if (isNaN($(this).val()) == false) {
				value = false;
			}
		});
	}
	return value;
}

