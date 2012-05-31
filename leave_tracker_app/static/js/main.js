$(function() {

	// Init jQuery slider
	$(".slider").each(function() {
		$(this).slider({
			value:0,
			min: 0,
			max: 20,
			step: 1,
			slide: function(event, ui) {
				$(this).siblings("input").val(ui.value);
			}
		});
	});

	// Show/hide Wabi section
	$("#wabi-button a").click(function() {
		if ($("#wabi-content").css("display") == "block") {
			$("#wabi-content").fadeOut();
		} else {
			$("#wabi-content").fadeIn();
		}

		return false;
	});

	// Goals/Rating tabs
	function tabs() {
		var tabs = $("#tabs > div");

		$("#tab-headings").delegate("li", "click", function(e) {
			var li = $(this),
				hash = li.children("a").attr("href");

			li.addClass("goals-rating-tab-selected").siblings().removeClass("goals-rating-tab-selected");
			tabs.hide().filter(hash).show();

			e.preventDefault();
		});
	};
	if ($("#tabs").length > 0) {
		tabs();
	}


	// Browser fixes
	if (navigator.userAgent.match(/Webkit/ig)) {
		$("#nav li").css("margin-top", "1px");
	}
	if (navigator.userAgent.match(/Firefox/ig)) {
		$("input[type='submit'], a.button").css("line-height", "30px");
		$("#basic-info #fake-form").css("padding-bottom", "56px");
		$("#wabi-help").css("padding-bottom", "40px");
	}
	if (navigator.userAgent.match(/MSIE/ig)) {
		$("table:not(#sidebar table)").css("border", "1px solid rgb(225, 214, 207)");
	}
	if (navigator.userAgent.match(/MSIE 6/ig)) {
		$("body").html("Sorry! Your browser, Internet Explorer 6, is not compatible with this website. Please upgrade to <a href='http://www.apple.com/safari'>Apple Safari</a> or <a href='http://google.com/chrome'>Google Chrome</a> to view this website.");
		$(".container_12").css("display", "none");
	}


	// Confirm adding client to client list
	$(".add-to-client-list").click(function() {
		var answer = confirm("Are you sure you want to add this client to your clients list?\n\nThis cannot be undone.");
		if (answer) {
			location.href = "index.html";
		}
	});

	// Init jQuery dialog
	$(".jquery-archive").click(function() {
		$("#dialog-confirm").dialog({
			resizable: false,
			height:290,
			width:450,
			modal: true,
			buttons: {
				"Archive the Goal": function() {
					$( this ).dialog( "close" );
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				}
			}
		});
	});


	// Adds support for the HTML5 placeholder attribute for older browsers
    var i = document.createElement('input');
    if ('placeholder' in i) {
        return;
    }
	var isPassword = function(input) {
		return $(input).attr('realType') == 'password';
	}
	var valueIsPlaceholder = function(input) {
		return input.value == $(input).attr('placeholder');
	}
	var showPlaceholder = function(input, loading) {
		if (input.value == '' || (loading && valueIsPlaceholder(input))) {
			if (isPassword(input)) {
				try {
					input.setAttribute('type', 'input');
				} catch (e) { }
			}
			input.value = $(input).attr('placeholder');
			$(input).addClass('placeholder');
		}
	}
	var hidePlaceholder = function(input) {
		if (valueIsPlaceholder(input) && $(input).hasClass('placeholder')) {
			if (isPassword(input)) {
				try {
					input.setAttribute('type', 'password');
					input.focus();
				} catch (e) { }
			}
			input.value = '';
			$(input).removeClass('placeholder');
		}
	}
	$(':text[placeholder],:password[placeholder]').each(function(index) {
		if ($(this).attr('type') == 'password') {
			$(this).attr('realType', 'password');
		}
		showPlaceholder(this, true);
		$(this).focus(function() { hidePlaceholder(this) });
		$(this).blur(function() { showPlaceholder(this, false) });
	});

});





