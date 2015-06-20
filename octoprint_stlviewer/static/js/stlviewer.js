$(function() {
    function stlviewerViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];
        self.settings = parameters[1];
		self.files = parameters[2].listHelper;
		
		self.FileList = ko.observableArray();
		self.RenderModes = ko.observableArray(['render as points','render as wireframe','render as flat','render as smooth']);
		
		self.canvas = document.getElementById('cv');
		self.viewer = new JSC3D.Viewer(self.canvas);
		self.models = document.getElementById('stlviewer_file_list');
		self.modes = document.getElementById('render_mode_list');
		
		self.setRenderMode = function() {
			switch(self.modes.selectedIndex) {
			case 0:
				self.viewer.setRenderMode('point');
				break;
			case 1:
				self.viewer.setRenderMode('wireframe');
				break;
			case 2:
				self.viewer.setRenderMode('flat');
				break;
			case 3:
				self.viewer.setRenderMode('smooth');
				break;
			default:
				self.viewer.setRenderMode('flat');
				break;
			}
			self.viewer.update();
		}	

		self.loadModel = function() {
			self.viewer.replaceSceneFromUrl('/downloads/files/local/' + self.models[self.models.selectedIndex].value);
			self.viewer.update();
		}

        // This will get called before the stlviewerViewModel gets bound to the DOM, but after its depedencies have
        // already been initialized. It is especially guaranteed that this method gets called _after_ the settings
        // have been retrieved from the OctoPrint backend and thus the SettingsViewModel been properly populated.
        self.onBeforeBinding = function() {
			self.FileList(self.files.items());
			//console.log(self.files.items());

			self.viewer.setParameter('SceneUrl', '/downloads/files/local/' + self.models[self.models.selectedIndex].value);
			self.viewer.setParameter('InitRotationX', 20);
			self.viewer.setParameter('InitRotationY', 20);
			self.viewer.setParameter('InitRotationZ', 0);
			self.viewer.setParameter('ModelColor', '#CAA618');
			self.viewer.setParameter('BackgroundColor1', '#000000');
			self.viewer.setParameter('BackgroundColor2', '#6A6AD4');
			self.viewer.setParameter('RenderMode', 'smooth');
			self.viewer.setParameter('ProgressBar', 'on');
			self.viewer.init();
			self.viewer.update();
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
