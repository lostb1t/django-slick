// slick jQuery namespace
var slk = {
	"jQuery": jQuery.noConflict(true)
};

// django jQuery namespace
var django = {
	"jQuery": slk.jQuery.noConflict(true)
};

(function($) {
	$('#sidebar [data-scrollbar="true"]').slimScroll({
		height: '100%',
		width: 'auto'
	});

	slick.initFilter = function() {
		// Dont autoclose
		$('.dropdown-menu-form').click(function (e) {
			e.stopPropagation();
		});

		$(".filter-choice").change(function() {
			location.href = $(this).val();
		});
	};

})(slk.jQuery);