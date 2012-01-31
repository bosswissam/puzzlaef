var initialize_pick_theme = function( puzzle_id ){
	
	$(".thumbWrapper").first().addClass("selected");
	$(".thumbWrapper").first().children().addClass("selected");
	
	var onClickFunction = function (e){
		$("div.thumbWrapper.selected").removeClass("selected");
		$("img.thumb.selected").removeClass("selected");
		$("div.thumbLabel.selected").removeClass("selected");
		$(e.delegateTarget).addClass("selected");
		$(e.delegateTarget).children().addClass("selected");
	};
	$(".thumbWrapper").on("click", "img", onClickFunction);
	$(".thumbWrapper").on("click", "div", onClickFunction);
	
	$('#begin_button').click( function(e){
		var theme = $("div.thumbWrapper.selected > div").html();
		Dajaxice.puzzlaef.puzzle.theme_picked(Dajax.process, {'puzzle': puzzle_id, 'theme':theme});
	});
};


var start_puzzle = function(_with){
	Dajaxice.puzzlaef.puzzle.start_puzzle( function(data){
		Dajax.process(data);
	}, {'username': _with});
};

var initialize = function(id) {
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
	Dajaxice.puzzlaef.main.send_form(Dajax.process,{'form':data});
}

var initiate_play_search = function(){
	
	
	var defaultBounds = new google.maps.LatLngBounds(
	  new google.maps.LatLng(-33.8902, 151.1759),
	  new google.maps.LatLng(-33.8474, 151.2631));

	var input = document.getElementById('search-input');
	var options = {
	  bounds: defaultBounds,
	  types: ['geocode']
	};

	autocomplete = new google.maps.places.Autocomplete(input, options);
	
	
	var new_location_set = function() {
	  var populate_map = function(locations) {
		$("#current-puzzles-wrapper").hide('medium');
		console.log(locations);
		if ($('#play_map_canvas').length == 0){
			$('#page-container').append("<div id='play_map_canvas'></div>");
		}
		
		var mapOptions = {
		  center: new google.maps.LatLng(-33.8688, 151.2195),
		  zoom: 13,
		  mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		var map = new google.maps.Map(document.getElementById('play_map_canvas'),
		  mapOptions);
		
		geocoder = new google.maps.Geocoder();
		if (locations.length == 0){}
			geocoder.geocode( { 'address': $('#search-input').val() }, function(results, status) {
		        if (status == google.maps.GeocoderStatus.OK) {
		          map.setCenter(results[0].geometry.location);
		        } else {
		          alert("Geocode was not successful for the following reason: " + status);
		        }
		});
		
	    for (i = 0; i < locations.length; i++) {  
			var infoWindowContent = '<div style="text-align:center"><strong>' + locations[i].username + '</strong><br>' + locations[i].location + '<div class="button blue" onclick="start_puzzle(\''+ locations[i].username +'\')" style="float:none">Start Puzzlaef</div></div>';
			
			var process_geocode = function(infoWindowContent) {
				return function(results, status){
			      if (status == google.maps.GeocoderStatus.OK) {
			        map.setCenter(results[0].geometry.location);
			        var marker = new google.maps.Marker({
			            map: map,
			            position: results[0].geometry.location
			        });
					var listener = (function(marker) {
				        	return function() {
								var infowindow = new google.maps.InfoWindow();
					          	infowindow.setContent(infoWindowContent);
					          	infowindow.open(map, marker);
				        }
				      })(marker);
					google.maps.event.addListener(marker, 'click', listener);
			      } else {
			        alert("Geocode was not successful for the following reason: " + status);
			      }
				}	
			 };
			
			geocoder.geocode( { 'address': locations[i].location}, process_geocode(infoWindowContent));
	    }
	};
	
	Dajaxice.puzzlaef.main.find_locations(populate_map,{'location':$("#search-input").val()});
};
	google.maps.event.addListener(autocomplete, 'place_changed', new_location_set);
	$("#search-button").click(new_location_set);
};

var change_page = function(event){
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
	if($(".nav-page-element")){
		$(".nav-page-element").click(change_page);
	}
	
	if ($(".registrationForm #my_form")) {
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
	
	
	if (document.getElementById('id_location')){
		 initialize('id_location');
	}
	
	if (document.getElementById('search-input')){
		 initiate_play_search();
	}
	
	$('.fileUpload').fileUploader();
});
