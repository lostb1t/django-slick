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

	slick.handlePanelAction = function() {
		var cookie_val = $.cookie('collapsed-panels');

		if (cookie_val !== undefined) {
			var states = $.parseJSON(cookie_val);
			
			// Set initial states
			$.each(states, function(index, panelid) {
				$("#" + panelid + " .panel-body").toggleClass('collapsed');
			});	
		}else{
			var states = [];
		}

		$("[data-click=panel-collapse]").click(function(e) {
        	e.preventDefault();
        	var t = $(this).closest(".panel");
        	var id = t.attr("id");

        	
			$(".panel-body", t).slideToggle( "normal", function() {
			    $(".panel-body", t).toggleClass('collapsed');
			 });
        	
        	// save state
        	if ($(".panel-body", t).hasClass('collapsed')) {
        		states.push(id);
        	}else{
        		var index = states.indexOf(id);
        		states.splice(index, 1);
        	}

        	$.cookie('collapsed-panels', JSON.stringify(states));

        });
	}

	slick.handleDraggablePanel = function() {
	    var e = ".row.sortable > [class*=col]";
	    var t = ".panel-heading";
	    var n = ".row.sortable > [class*=col]";
	    
	    $(e).sortable({
	        handle: t,
	        connectWith: n,	
	    });
        
        var id = getID(e);
        if(id !== false) {
	    	restoreOrder(id);
	    }

		$(e).sortable().bind('sortupdate', function(event, ui) {
			if(id !== false) {
				saveOrder(id);
			}
		});

		function getID(selector) {
			$p = $(selector).parent();

			if($("[data-sortable-id]", $p)) {
				return "sortable-" + $p.attr('data-sortable-id');
			}
			return false;
		}

		function saveOrder(id) {
			console.log(id);
			var order = [];
			var arr = $(e).sortable("toArray");
			
			arr.each(function() {
				var $column = $(this);
				var $panels = $column.children();
				var index = arr.index(this);

				order[index] = [];
				$panels.each(function() {
					order[index][$panels.index(this)] = $(this).attr('id');
				});

			});
			$.cookie(id, JSON.stringify(order));
    	}

    	function restoreOrder(id) {
    		var cookie_val = $.cookie(id);
    		if (cookie_val == undefined) {
    			return;
    		}

    		var order = $.parseJSON(cookie_val);
    		var columns = $(e).sortable("toArray");

    		$.each(order, function(index, panels) {
    			var $column = columns[index];

    			$.each(panels, function(i, id) {
    				$panel = $("#" + id);
    				$panel.appendTo($column);
    			});

    		});
    	}
	};

	slick.initFilter = function() {
		$(".filter-choice").change(function() {
			location.href = $(this).val();
		});
	};

	slick.initSearchbar = function() {

	};
    
    slick.initSidebar = function() {
    	$("[data-click='sidebar-toggle']").click(function (e) {
			e.stopPropagation();
			$( "#sidebar" ).toggleClass( "toggled" );
		});
		
    };

    slick.init = function() {
    	slick.handleDraggablePanel();
    	slick.handlePanelAction();
    }

    
    /*
    slick.init = function() {
	  	$('.add-another').each(function(){
		    $(this).data('onclick', this.onclick);

	    	// Replace popup with modals
		    this.onclick = function(e) {
		        BootstrapDialog.show({
		            //message: $('<div></div>').load($(this).attr('href') + "?_popup=1")
		            message: '<iframe id="modal-popup" onload="resizeIframe(this)" width="100%" frameBorder="0" scrolling="no" src="' + $(this).attr('href') + "?_popup=1" + '"></iframe>'
		        });
		    	e.preventDefault();
	 		};
		});
    };
    */


    /*
	$('.add-another').each(function(i,o){
	    select_obj=$(o).parent().find('select')[0];
	    item_id=select_obj.options[select_obj.selectedIndex].value;
	    edit_url=o.href.replace('add',item_id)+"?_popup=1";
	    $(this).after('<span> </span><a class="edit-popup" '
	            +'href="'+edit_url+'"><img src="/static/admin/img/admin/'
	            +'icon_changelink.gif"/></a>')
	})
	*/
	

})(slk.jQuery);