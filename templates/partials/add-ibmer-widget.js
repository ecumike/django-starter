	(function () {
		function setupNewIbmerForm (callback) {
			$("#ms-employee-search-button").on('click', function (evt) {
				var $button = $(evt.target);
				
				evt.preventDefault();
				
				var $selectList = $('#ms-employee-search');
				
				if (!$selectList.val()) {
					alert('You can\'t add a ghost.');
					return;
				}

				$.ajax({
					url: $button.data('url'),
					type: 'post',
					dataType: 'json',
					data: {
						'csrfmiddlewaretoken': '{{ csrf_token }}',
						'email': $selectList.val()
					},
					success: function (data) {
						callback(data);
					},
					error: function (data) {
						$("#ms-newuser-msg").html('There was a problem adding that user.');
					}
				});
			});
		}
		window.setupNewIbmerForm = setupNewIbmerForm;
		
		
		function setupEmployeeSearch () {
			$('#ms-employee-search').select2({
				placeholder: $('#ms-employee-search').data('placeholder'),
				minimumInputLength: 1,
				width: '100%',
				ajax: {
					url: 'https://w3-services1.w3-969.ibm.com/myw3/unified-profile/v1/search/user?searchConfig=optimized_search&userId=&rows=8&timeout=4000&threshold=0',
					dataType: 'json',
					data: function (params) {
						return query = {
							query: params.term
						}
					},
					processResults: function (data) {
						var selectOpts = [];
						
						$.each(data.results, function () {
							selectOpts.push({
								id: this.preferredIdentity,
								text: this.notesEmail
							});
						});
						return {
							results: selectOpts
						};
					}
				}
			});
		}
		
		$(function () {
			setupEmployeeSearch();
		});

	})(jQuery);

