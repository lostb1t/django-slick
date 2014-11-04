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

	$('.selectpicker').selectpicker();

	slick.initFilter = function() {
		// Dont autoclose
		/*
		$('.slk-filter .dropdown-menu').click(function (e) {
			e.stopPropagation();
		});
		*/


		$(".filter-choice").change(function() {
			//console.log($(this).val());
			//console.log($('.selectpicker').val())
			location.href = $(this).val();
		});
	};
    
    slick.initSidebar = function() {
    	$("[data-click='sidebar-toggle']").click(function (e) {
			e.stopPropagation();
			$( "#sidebar" ).toggleClass( "toggled" );
		});
    };
	

})(slk.jQuery);