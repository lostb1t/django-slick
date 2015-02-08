(function($) {

    $('#sidebar .nav').metisMenu();
	
	var popover_elements = $('#sidebar .nav > li > a'); // todo beter naming

	$(".sidebar-toggle").on("click", function(e) {
		e.preventDefault();
		$("body").toggleClass('sidebar-sm');
		popover_menu_toggle();

		if($("body").hasClass('sidebar-sm')) {
			$.cookie('SIDEBAR_SM', true, { expires: 7, path: '/' });
		}else{
			$.removeCookie('SIDEBAR_SM', { path: '/' });
		}
	});

	popover_elements.each(function() {
		var e = $(this);
		var title = e.children(".nav-title");
		var content = e.parent().children(".submenu");

  		e.popover({
  			animation: false,
  			html: true,
  			viewport: e,
  			trigger: "manual",
  			title: function() {
                return title.html();
            },
  			content: function() {
  				//console.log(content.html());
  				return content.html();
  			},
  			//placement: 'right',
  			container: '#sidebar .nav',
  			template: '<div class="popover menu-popover"><h4 class="popover-title"></h4><div class="popover-content"></div></div>',
  		}).on("show.bs.popover", function() {

  		})
  		.on("hidden.bs.popover", function() {
  			//console.log('hidden');
            //e.removeClass("hover");
        }).on("mouseenter", function() {	// TODO add check if popover is already in progress to be hidden, otherwise ...twitching..
		    var _this = this;
		    popover_elements.not(this).popover('hide');
		    $(_this).popover("show");
		    $(".popover").on("mouseleave", function () {
		        $(_this).popover('hide');
		    }, 500);
        }).on("mouseleave", function () {
		    var _this = this;
		    setTimeout(function () {
		        if (!$(".popover:hover").length) {
		            $(_this).popover("hide");
		        }
		    }, 500);
    	});
	})

	popover_menu_toggle = function () {
		if ($("body").hasClass('sidebar-sm')) {
			popover_elements.popover('enable');
		}else{
			popover_elements.popover('disable');
		}
	}

	// Init
	popover_menu_toggle();

})(jQuery);