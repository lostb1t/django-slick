// slick jQuery namespace
var slk = {
	"jQuery": jQuery.noConflict(true)
};

// django jQuery namespace
var django = {
	"jQuery": slk.jQuery.noConflict(true)
};

(function($) {
	
	$('.selectpicker').selectpicker();

	slick.initFilter = function() {
		$(".filter-choice").change(function() {
			location.href = $(this).val();
		});
	};

	slick.initSearchbar = function() {

	};

	slick.initSidebar = function () {
		$('#metis').metisMenu();
		
    	$("[data-click='sidebar-toggle']").click(function (e) {
			e.stopPropagation();
			$("#sidebar").toggleClass("collapse");
			$("#content").toggleClass("ml-sm-auto");
			
		});
    };

	
    // slick.initSidebar = function() {
    // 	$("[data-click='sidebar-toggle']").click(function (e) {
	// 		e.stopPropagation();
	// 		$( "#sidebar" ).toggleClass( "toggled" );
	// 	});
    // };
	

})(slk.jQuery);
