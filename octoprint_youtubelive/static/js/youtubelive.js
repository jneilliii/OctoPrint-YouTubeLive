$(function () {
	function youtubeliveViewModel(parameters) {
		var self = this;
		
		self.settingsViewModel = parameters[0];
		self.channel_id = ko.observable();
		self.stream_id = ko.observable();

		// This will get called before the youtubeliveViewModel gets bound to the DOM, but after its depedencies have
		// already been initialized. It is especially guaranteed that this method gets called _after_ the settings
		// have been retrieved from the OctoPrint backend and thus the SettingsViewModel been properly populated.
		self.onBefireBinding = function () {
			self.channel_id(self.settingsViewModel.settings.plugins.youtubelive.channel_id());
			self.stream_id(self.settingsViewModel.settings.plugins.youtubelive.stream_id());
		};

		self.onEventSettingsUpdated = function (payload) {            
            self.channel_id = self.settingsViewModel.settings.plugins.youtubelive.channel_id();
			self.stream_id(self.settingsViewModel.settings.plugins.youtubelive.stream_id());
        };
		
		self.onDataUpdaterPluginMessage = function(plugin, data) {
			if (plugin != "youtubelive") {
				return;
			}
			
			if(data.error) {
				new PNotify({
							title: 'YouTube Live Error',
							text: data.error,
							type: 'error',
							hide: false
							});
			}
			self.processing.remove(data.topic+'|'+data.publishcommand);
        };
		
		self.startStream = function() {
			$.ajax({
                url: API_BASEURL + "plugin/youtubelive",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "startStream"
                }),
                contentType: "application/json; charset=UTF-8"
            })
		}
	}

	// This is how our plugin registers itself with the application, by adding some configuration information to
	// the global variable ADDITIONAL_VIEWMODELS
	ADDITIONAL_VIEWMODELS.push([
			// This is the constructor to call for instantiating the plugin
			youtubeliveViewModel,

			// This is a list of dependencies to inject into the plugin, the order which you request here is the order
			// in which the dependencies will be injected into your view model upon instantiation via the parameters
			// argument
			["settingsViewModel"],

			// Finally, this is the list of all elements we want this view model to be bound to.
			[("#tab_plugin_youtubelive")]
		]);
});
