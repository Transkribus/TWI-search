$(document).ready(function(){
	$('span.minus').hide();
	$('span.plus').on('click', function () {
		$(this).hide();	
		$(this).siblings("span.minus").show();
	});

	$('.collapse').on('hidden.bs.collapse', function (e) {
		$('#' + e.currentTarget.id).siblings("span.minus").hide();	
		$('#' + e.currentTarget.id).siblings("span.plus").show();	
	});

	$('#search-result-length').on('change', function(){
		if(window.location.href.match(/r=\d+/)){
			console.log("HERE");
			window.location.href = window.location.href.replace(/r=\d+/,"r="+$(this).val());
		}else{
			window.location.href += "&r="+$(this).val();
		}
	});
});
