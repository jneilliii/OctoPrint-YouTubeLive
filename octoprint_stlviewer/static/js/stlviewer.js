$(function() {
    function stlviewerViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];
        self.settings = parameters[1];
		self.files = parameters[2].listHelper;
		
		self.FileList = ko.observable();
		
		self.setRenderMode = function() {
			if(logoTimerID > 0)
				return;
			var modes = document.getElementById('render_mode_list');
			switch(modes.selectedIndex) {
			case 0:
				viewer.setRenderMode('point');
				break;
			case 1:
				viewer.setRenderMode('wireframe');
				break;
			case 2:
				viewer.setRenderMode('flat');
				break;
			case 3:
				viewer.setRenderMode('smooth');
				break;
			default:
				viewer.setRenderMode('flat');
				break;
			}
			viewer.update();
		}	

		self.loadModel function() {
			if(logoTimerID > 0) {
				clearInterval(logoTimerID);
				logoTimerID = 0;
				viewer.enableDefaultInputHandler(true);
			}
			var models = $('select#files_template_model');
			viewer.replaceSceneFromUrl('/downloads/files/local/' + models[models.selectedIndex].value);
			viewer.update();
		}		

        // This will get called before the HelloWorldViewModel gets bound to the DOM, but after its depedencies have
        // already been initialized. It is especially guaranteed that this method gets called _after_ the settings
        // have been retrieved from the OctoPrint backend and thus the SettingsViewModel been properly populated.
        self.onBeforeBinding = function() {
			self.FileList(self.files.items());
			console.log(self.files.items());
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration information to
    // the global variable ADDITIONAL_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        stlviewerViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request here is the order
        // in which the dependencies will be injected into your view model upon instantiation via the parameters
        // argument
        ["loginStateViewModel", "settingsViewModel", "gcodeFilesViewModel"],

        // Finally, this is the list of all elements we want this view model to be bound to.
        [("#tab_plugin_stlviewer")]
    ]);
});
