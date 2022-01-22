(function($) {
	CL.typeahead = {};
	
	var $inputField = {},
		$typeaheadUl = {},
		$typeaheadContainer = {},
		bpUserByEmailWsrUrl = "https://w3-services1.w3-969.ibm.com/myw3/unified-profile/v1/search/user?searchConfig=optimized_search&query={q}&userId=&rows=8&timeout=4000&threshold=0",
		defaultTypeaheadRequestPause = 50, // # of MS to wait between typing before making a WSR.
		latestText = "",
		requestCount = 0,
		typeaheadResultsShowing = false,
		makeTypeaheadRequest = (function() {
			var timer = 0;
			return function(callback, ms) {
				var waitTime = ms || defaultTypeaheadRequestPause;
				clearTimeout(timer);
				timer = setTimeout(callback, waitTime);
			};
		})();


	function clearTypeahead () {
		if ($typeaheadUl.length > 0) {
			$typeaheadUl.empty();
		}
	}


	function requestTypeaheadText (forceRequest) {
		var currentSearchTerm = $inputField[0].value;

		if (currentSearchTerm === latestText && !forceRequest) {
			return;
		}

		latestText = currentSearchTerm;

		// If they cleared the search field (there's no value in the text field), remove the typeahead box and stop.
		if (currentSearchTerm === "") {
			makeTypeaheadRequest(function() {
				clearTypeahead();
				showTypeaheadResults(false);
			}, defaultTypeaheadRequestPause + 10);

			return;
		}

		// Call the throttler with our callback function to run to make a typeahead service request.
		makeTypeaheadRequest(function() {
			$.ajax({
				url: bpUserByEmailWsrUrl.replace('{q}', currentSearchTerm),
				dataType: "json",
				searchTerm: currentSearchTerm,
				requestCount: ++requestCount,
				success: function (response) {
					// If this request isn't the latest one (for slow API responses), 
					//  don't update the TA box with it's results.
					if (requestCount !== this.requestCount) {
						return;
					}
					
					if (response === null) {
						showTypeaheadResults(false);
						return;
					}

    				// Format the results into a simply array of terms/strings and 
    				//  call the function to create the typeahead box with our results.
    				var nameListArr = [],
    					i = 0,
    					len = response.results.length;
    
    				if (len === 0) {
    					return;
    				}
    				
    				for (i; i < len; i++) {
    					if (response.results[i].mail) {
    						nameListArr.push(response.results[i].nameFull + ',' + response.results[i].mail[0] + ',' + response.results[i].notesEmail);
    					}
    				}
    				
    				// Call the masthead typeahead API with the term used for *this WSR* 
					//  and the array you created of results to show.
					createTypeaheadContainer(this.searchTerm, nameListArr);
					
				},
				error: function(response) {
					console.error('Error calling typeahead service: ', response);
				}
			});
		});
	}

	// This limits the # that we show in the container.
	function createTypeaheadContainer (searchString, results) {
		var lis = '';

		$.each(results, function () {
			var nameArr = this.split(",");
			lis += '<li><a class="pa2 db hover-white hover-bg-dark-blue" data-name="' + nameArr[0] + '" data-email="' + nameArr[1] + '" href="#">' + nameArr[2] + '</a></li>';
		});

		$typeaheadUl.html(lis);
		
		// If they emptied the field after this WSR ran, clear the typeaheads.
		if ($inputField.val() === "") {
			clearTypeahead();
			showTypeaheadResults(false);
		}
		else {
			// Inject typeahead list on first time we have results.
			if (!$typeaheadContainer.find("ul")[0]) {
				$typeaheadContainer.html($typeaheadUl);
			}

			$typeaheadUl.html(lis);

    		showTypeaheadResults(true);
		}
	}

	function showTypeaheadResults (b) {
		if (b) {
			$typeaheadContainer.addClass("bo-fadein").removeClass("bo-fadeout");
			typeaheadResultsShowing = true;
		}
		else {
			$typeaheadContainer.addClass("bo-fadeout").removeClass("bo-fadein");
			typeaheadResultsShowing = false;
		}
	}


	// Setup and bind fields
	CL.setupTypeaheadWidget = setupTypeaheadWidget;
	function setupTypeaheadWidget (fieldId, listId) {
		$inputField = $("#"+fieldId);
		$typeaheadContainer = $("#custom-typeahead-container");
		$typeaheadUl = $("#"+listId);

		// Bind the results so when you click on one, it replaces the input text with it.
		$typeaheadUl.on("click", function (evt) {
			evt.preventDefault();
			evt.stopPropagation();
			$(evt.target).parent().addClass("highlight");
			setInputFieldValue();
			clearTypeahead();
			showTypeaheadResults(false);
		});

		$inputField.on("input", function () {
			requestTypeaheadText();
		}).on("focus", function () {
			// If there is a value in the field, show the results on FIELD focus only.
			if ($inputField.val() !== "") {
				showTypeaheadResults(true);
			}
		}).on("keydown", function (evt) {
			var keyCode = evt.keyCode;
			
			// DOWN.
			if (keyCode === 40) {
				evt.preventDefault();
				
				$typeaheadUl.find("a:first").focus();
			}
			// ENTER.
			else if (keyCode === 13) {
				evt.preventDefault();
			}
		});
	}


	function setInputFieldValue () {
		userName = $("li.highlight", $typeaheadUl).children("a").data("name");
		userEmail = $("li.highlight", $typeaheadUl).children("a").data("email");
		
		CL.typeahead.userName = userName != "" ? userName : "";
		CL.typeahead.userEmail = userEmail != "" ? userEmail : "";
		
		// Set active dedcendent attr. on field to tell ATs this one is active so they read it since we don't
		//  focus on it, then change the text in the text field.
		$inputField.attr("aria-activedescendant", $("li.highlight", $typeaheadUl).attr("id"));

		$inputField.val(userEmail);
	}

})(jQuery);
