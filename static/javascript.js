$.fn.exists = function () {
    return this.length !== 0;
}

var submitCurrentComment = function( piece, comment ) {
	Dajaxice.puzzlaef.puzzle.post_comment( function(data){
		$('#piece-comments').replaceWith(data.commentsView);
		initialize_comment_input(piece);
	}, {'piece':piece, 'comment':comment});
}

var initialize_comment_input = function ( piece ) {
	$('#new-comment-textarea').bind('keypress', function(e) {
	     var code = (e.keyCode ? e.keyCode : e.which);
		 if(code == 13) { //Enter keycode
			e.preventDefault();
		    submitCurrentComment(piece, $('#new-comment-textarea').val());
		 }
	});
	$("#new-comment-button").click( function(e) {
		submitCurrentComment(piece, $('#new-comment-textarea').val());
	});
}
var showPiece = function( piece ){
	if($('#pieceViewModal').exists()){
		Dajaxice.puzzlaef.puzzle.get_piece_view(function (data){
			$('#pieceView').replaceWith(data.pieceView);
			$('#pieceViewModal').modal('show');
			
			initialize_comment_input(piece);
		}, {'piece':piece});
	} else {
		Dajaxice.puzzlaef.puzzle.get_piece_view_with_modal(function (data){
			$('body').append(data.pieceViewModal);
			$('#pieceViewModal').modal();
			
			initialize_comment_input(piece);
		}, {'piece':piece});
	}
	
}

var show_profile = function(){
	Dajaxice.puzzlaef.puzzle.get_profile(function (data){
		$('body').append(data.profile);
		$('#profileModal').modal();
	});
}

var prependUserPuzzle = function( puzzle_as_string ){
	var puzzleObj = $(puzzle_as_string);
	puzzleObj.hide();
	if(!$("#user-puzzles > div.puzzle").exists()){
		$("#user-puzzles").empty();
	}
	$("#user-puzzles").prepend( puzzleObj );
	puzzleObj.show('medium');
}

var initialize_start_puzzle = function(){
	
	/*$(".thumbWrapper").first().addClass("selected");
	$(".thumbWrapper").first().children().addClass("selected");*/
	
	var onClickFunction = 
	$('.play-button').click( function (e){
		$(e.delegateTarget).addClass("selected");
		$(e.delegateTarget).children().addClass("selected");
		var puzzle_id = $(e.delegateTarget).siblings('.open-puzzle-id').html();
		Dajaxice.puzzlaef.puzzle.join_play_puzzle(function (data){
			$('#start-puzzle-panel').collapse('hide');
			prependUserPuzzle(data['puzzleAsString']);
			eval(data['uploadButtonScript']);
		}, {'puzzle':puzzle_id});
	});
	
	$('#start-puzzle-file-uploader').button()

};

var refreshPuzzle = function(id, filename, response){
	if(response.puzzleAsString){
		$("#puzzle"+response.puzzleID).replaceWith($(response.puzzleAsString.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace('\t', '').replace('\n', '').replace('\\"','"')));
	}
}

var refreshThemes = function(id, filename, response){
	Dajaxice.puzzlaef.puzzle.get_latest_picture_grid(function (data){
		$('.pictureGrid').replaceWith(data.newPictureGrid);
		initialize_pick_theme(null);
	});
}

var refresh_start_puzzle = function(_with){
	Dajaxice.puzzlaef.puzzle.get_start_puzzle_content( function(data){
			Dajax.process(data);
		});
};

var new_puzzle_started = function(id, filename, response) {
	$('#start-puzzle-panel').collapse('hide');
	if (response.success){
		var alert = '<div class="alert alert-block alert-success"> <a class="close" data-dismiss="alert">×</a> <h4 class="alert-heading">A new Puzzle was started!</h4> Soon enough someone else will join your Puzzle with a response!</div>';
	} else {
		var alert = '<div class="alert alert-block alert-error"> <a class="close" data-dismiss="alert">×</a> <h4 class="alert-heading">Woops!</h4> Something seems to have gone wrong! Please try again!</div>';
	}
	$("#alerts-panel").append(alert);
};

var start_puzzle = function(_with){
	Dajaxice.puzzlaef.puzzle.start_puzzle( function(data){
			Dajax.process(data);
		}, {'username': _with});
};

var initialize = function(id) {        
	var uploader = new qq.FileUploader({
	    element: document.getElementById('file-uploader'),
	    action: 'upload/profile',
		allowedExtensions: ['jpg', 'jpeg', 'png', 'gif'],
		template: '<div class="qq-uploader">' + 
                '<div class="qq-upload-drop-area"><span>Drop files here to upload</span></div>' +
                '<div class="qq-upload-button button red">Upload your Profile Picture</div>' +
                '<ul class="qq-upload-list"></ul>' + 
             '</div>',
	    debug: true
	});
	
	var avatar = document.getElementById('id_avatar');
	avatar.setAttribute("hidden", "true");
	$(avatar).prevAll().remove();
	
    var mapOptions = {
		  center: new google.maps.LatLng(-33.8688, 151.2195),
		  zoom: 13,
		  mapTypeId: google.maps.MapTypeId.ROADMAP
		};
	var map = new google.maps.Map(document.getElementById('map_canvas'),
	  mapOptions);

	var defaultBounds = new google.maps.LatLngBounds(
	  new google.maps.LatLng(-33.8902, 151.1759),
	  new google.maps.LatLng(-33.8474, 151.2631));

	var input = document.getElementById(id);
	var options = {
	  bounds: defaultBounds,
	  types: ['geocode']
	};
	var autocomplete = new google.maps.places.Autocomplete(input, options);
	
	autocomplete.bindTo('bounds', map);

	var infowindow = new google.maps.InfoWindow();
	var marker = new google.maps.Marker({
	  map: map
	});
	
	google.maps.event.addListener(autocomplete, 'place_changed', function() {
	  infowindow.close();
	  var place = autocomplete.getPlace();
	  if (place.geometry.viewport) {
	    map.fitBounds(place.geometry.viewport);
	  } else {
	    map.setCenter(place.geometry.location);
	    map.setZoom(17);  // Why 17? Because it looks good.
	  }

	  marker.setPosition(place.geometry.location);
	  
	  var address = '';
	  if (place.formatted_address) {
	    address = place.formatted_address;
	  }

	  infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
	  infowindow.open(map, marker);
	});
}

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

var send_form = function(){
	data = $('#my_form').serializeObject();
	Dajaxice.puzzlaef.main.send_form(function(data){
		Dajax.process(data);
		$('#profileModal').modal('hide');
	},{'form':data});
}

var change_page = function(event){
	console.log("clicked!");
	var pageClickedTarget = $(event.target);
	var pageClicked = pageClickedTarget.html();
	var currentPage = $('.selected').html();
	if (currentPage != pageClicked) {
		$('.selected').removeClass('selected');
		pageClickedTarget.addClass('selected');
		Dajaxice.puzzlaef.main.changePage(function(data){
			Dajax.process(data);
			if (pageClicked == "Play"){
				initiate_play_search();
			} else if (pageClicked == "Settings") {
				initialize('id_location');
			}
		},{'newPage':pageClicked});
	}
};


$(document).ready(function() {
	if($(".nav-page-element").exists()){
		$(".nav-page-element").mousedown(change_page);
	}
	
	if ($(".registrationForm #my_form").exists()) {
		var inputs = $(".form > * > input");
		var labels = $(".form > * > label");
		for (i=0; i< inputs.length; i++){
			if (labels[i-1]){
				$(inputs[i]).attr("placeholder",$(labels[i-1]).html().replace(":", "..."));
				$(labels[i-1]).remove();
			}
		}
		$(labels[inputs.length]).remove();
	}
	
	
	if($('#start-puzzle-panel').exists()) {
		$('#start-puzzle-panel').on('show', function () {
		  	refresh_start_puzzle();
		});
		$("#start-puzzle-panel").collapse({
		  toggle: false
		});
	}
	
});
