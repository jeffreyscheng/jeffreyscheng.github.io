var CUBESHAPE = 0;

if(!window.matchMedia( "(max-width: 680px)" ).matches) {
	$("li.dropdown .dropdown-content a:last").css("border", "2px solid #c5e8e0");
	$("li.dropdown .dropdown-content a:last").css("border-radius", "0px 0px 10px 10px");
}

function dropdown(){
	$("li.dropdown").click(function(){
		$(this).find(".dropdown-content").fadeToggle(100); 
	}, function(){
		$(this).find(".dropdown-content").fadeToggle(100);
	});
}

function hideP(){
	$("p.hide").click(function(){
		if(!$(this).hasClass("open")){
			$(this).find(".toShow").show(500);
			$(this).addClass("open");
		} else {
			$(this).find(".toShow").hide(500);
			$(this).removeClass("open");
		}
	});
}

function cubeshapeCases(){
	$("#cubeshape1").click(function(){
		if([0,2,3].indexOf(CUBESHAPE) >= 0){
			if([2,3].indexOf(CUBESHAPE) >= 0){
				$("#cu2").hide();
				$("#cu3").hide();
			}
			$("#cu1").show();
			CUBESHAPE = 1;
		} else if (CUBESHAPE === 1){
			$("#cu1").hide();
			CUBESHAPE = 0;
		} 
		
	});

	$("#cubeshape2").click(function(){
		if([0,1,3].indexOf(CUBESHAPE) >= 0){
			if([1,3].indexOf(CUBESHAPE) >= 0){
				$("#cu1").hide();
				$("#cu3").hide();
			}
			$("#cu2").show();
			CUBESHAPE = 2;
		} else if (CUBESHAPE === 2) {
			$("#cu2").hide();
			CUBESHAPE = 0;
		} 

	});

	$("#cubeshape3").click(function(){
		if([0,1,2].indexOf(CUBESHAPE) >= 0){
			if([1,2].indexOf(CUBESHAPE) >= 0){
				$("#cu1").hide();
				$("#cu2").hide();
			}
			$("#cu3").show();
			CUBESHAPE = 3;
		} else if (CUBESHAPE === 3){
			$("#cu3").hide();
			CUBESHAPE = 0;
		} 
		
	});
}

function appear(){
	if (!$("nav ul").hasClass("response")){
		$("nav ul").addClass("response");
	} else {
		$("nav ul").removeClass("response");
	}
}


$(document).ready(function(){
	new WOW().init();
	$(function(){
		$.stellar({
			horizontalScrolling: false,
		});
	});
	dropdown();
	hideP();
	cubeshapeCases();
	$("li.dropdown .dropdown-content").hide();
	$("p.hide .toShow").hide();
	for (var i = 1; i <= 3; i++){
		$("#cu" + i).hide();
		console.log("blah");
	}
	CUBESHAPE = 0;
	$('.hover').bind('touchstart touchend', function(e) {
        e.preventDefault();
        $(this).toggleClass('hover_effect');
    });

    renderMathInElement(document.body);
})