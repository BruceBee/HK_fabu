$172(document).ready(function(){
							
	$172("#select1 dd").click(function () {
		$172(this).addClass("selected").siblings().removeClass("selected");
		if ($172(this).hasClass("select-all")) {
			$172("#selectA").remove();
		} else {
			var copyThisA = $172(this).clone();
			if ($172("#selectA").length > 0) {
				$172("#selectA a").html($172(this).text());
			} else {
				$172(".select-result dl").append(copyThisA.attr("id", "selectA"));
				console.log('选中01')
			}
		}
	});
	
	$172("#select2 dd").click(function () {
		$172(this).addClass("selected").siblings().removeClass("selected");
		if ($172(this).hasClass("select-all")) {
			$172("#selectB").remove();
		} else {
			var copyThisB = $172(this).clone();
			if ($172("#selectB").length > 0) {
				$172("#selectB a").html($172(this).text());
			} else {
				$172(".select-result dl").append(copyThisB.attr("id", "selectB"));
			}
		}
	});
	
	$172("#select3 dd").click(function () {
		$172(this).addClass("selected").siblings().removeClass("selected");
		if ($172(this).hasClass("select-all")) {
			$172("#selectC").remove();
		} else {
			var copyThisC = $172(this).clone();
			if ($172("#selectC").length > 0) {
				$172("#selectC a").html($172(this).text());
			} else {
				$172(".select-result dl").append(copyThisC.attr("id", "selectC"));
			}
		}
	});
	
	$172("#selectA").live("click", function () {
		$172(this).remove();
		$172("#select1 .select-all").addClass("selected").siblings().removeClass("selected");
	});
	
	$172("#selectB").live("click", function () {
		$172(this).remove();
		$172("#select2 .select-all").addClass("selected").siblings().removeClass("selected");
	});
	
	$172("#selectC").live("click", function () {
		$172(this).remove();
		$172("#select3 .select-all").addClass("selected").siblings().removeClass("selected");
	});
	
	$172(".select dd").live("click", function () {
		if ($172(".select-result dd").length > 1) {
			$172(".select-no").hide();
		} else {
			$172(".select-no").show();
		}
	});
	
});