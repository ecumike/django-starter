////////////////////////
//	Core namespace util.
////////////////////////
MA.namespace = function() {
	var scope = arguments[0],
		ln = arguments.length,
		i, value, split, x, xln, parts, object;

	for (i = 1; i < ln; i++) {
		value = arguments[i];
		parts = value.split(".");
		object = scope[parts[0]] = Object(scope[parts[0]]);
		for (x = 1, xln = parts.length; x < xln; x++) {
			object = object[parts[x]] = Object(object[parts[x]]);
		}
	}
	return object;
};


(function($){
	
	var bpImageUrl = 'https://w3-services1.w3-969.ibm.com/myw3/unified-profile-photo/v1/image/{email}?s=100';
	
	function loadUserImage () {
		$(".custom-userimage").each(function () {
			var $img = $(this),
				email = $img.data('email');
			
			if (!email) {
				$img.attr('src', MA.urls.cdnPath + 'unknownuser.png');
				return;
			}
			
			this.onerror = function () {
				$img.attr('src', MA.urls.cdnPath + 'unknownuser.png');
			};
			
			$img.attr('src', bpImageUrl.replace('{email}', email));
		});
	}

	$(function () {
		loadUserImage();
	});
	
})(jQuery);

