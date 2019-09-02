var mac_array = ["","","","","",""]

$("#btn-registrar").click(function () {
	if (verificar()) {
		setMacString();
		$("#form").submit();
	} else {
		alert("Ingrese todos los campos")
	}
});

$(".mac-input").keyup(function() {
	var posicion = parseInt($(this).attr("posicion"));
	var value = $(this).val();
	if (value.length == 2) {
		mac_array[posicion] = value;
	}
});

function verificar() {
	var value = true;
	$(".input").each(function() {
		console.log($(this).val(), $(this).val() == "");
		if ($(this).val() == "") {
			value = false;
		}
	});
	return value
}

function setMacString() {
	var string = "";
	for (var i = 0; i < mac_array.length; i++) {
		if (i == mac_array.length - 1) {
			string += mac_array[i];
		} else {
			string += mac_array[i] + ":";
		}
	}
	$("#mac").val(string);
}
