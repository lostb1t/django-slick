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
            $(e).removeClass("hover");
        }).on("mouseenter", function() {
		    var _this = this;
		    
		    popover_elements.not(e).popover('hide');
		    $(e).not(".hover").popover("show");
		    $(e).addClass("hover");

		    var id = e.data('bs.popover').tip().attr("id");
		    var popover = e.data('bs.popover').tip();

		    $("#" + id).mouseleave(function () {
		    	setTimeout(function() { 
			    	if ($(".popover").length) {
			    		e.popover('hide');
			    	}
		    	}, 300);
		    });

			
        }).on("mouseleave", function () {
		    var _this = this;

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