$(function () {
	function stlviewerViewModel(parameters) {
		var self = this;
		
		self.filesViewModel = parameters[0];
		self.files = ko.observableArray();
		self.FileList = ko.observableArray();
		self.RenderModes = ko.observableArray([{
						name : 'render as smooth',
						value : 'smooth'
					}, {
						name : 'render as flat',
						value : 'flat'
					}, {
						name : 'render as wireframe',
						value : 'wireframe'
					}, {
						name : 'render as points',
						value : 'point'
					}
				]);

		self.canvas = document.getElementById('cv');
		self.viewer = new JSC3D.Viewer(self.canvas);
		self.models = document.getElementById('stlviewer_file_list');
		self.modes = document.getElementById('render_mode_list');

		self.setRenderMode = function () {
			self.viewer.setRenderMode(self.modes[self.modes.selectedIndex].value);
			self.viewer.update();
		};

		self.loadModel = function () {
			var hash = self.models[self.models.selectedIndex].value;
			if (hash != "") {
				var model = self.findModel(hash);
				self.viewer.replaceSceneFromUrl(model.refs.download);
				self.viewer.setRenderMode(self.modes[self.modes.selectedIndex].value);
				self.viewer.update();
			}
		};

		// find model by hash
		self.findModel = function(hash) {
			var model = self.files.getItem(function(item){return item.hash == hash});
			return model;
		}

		// This will get called before the stlviewerViewModel gets bound to the DOM, but after its depedencies have
		// already been initialized. It is especially guaranteed that this method gets called _after_ the settings
		// have been retrieved from the OctoPrint backend and thus the SettingsViewModel been properly populated.
		self.onBeforeBinding = function () {
			console.log(self.filesViewModel.allItems);
			self.FileList(_.filter(self.files.listHelper.allItems, function(data) { return data["type"] == "model"; }));
			self.viewer.setParameter('SceneUrl', '');
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
		};

		//resize canvas after STL Viewer tab is made active.
		self.onTabChange = function (current, previous) {
			if (current == "#tab_plugin_stlviewer") {
				self.resiveCanvas();
				self.updateFileList();
			}
		};

		//append file list with newly updated stl file.
		//self.onEventUpload = function (file) {
		//	if (file.file.substr(file.file.length - 3).toLowerCase() == "stl") {
		//		self.FileList.push({
		//			name : file.file
		//		});
		//	}
		//};

		self.updateFileList = function () {
			self.FileList(_.filter(self.files, function(data) { return data["type"] == "model"; }));
		};

		self.resiveCanvas = function(){
        	$('canvas#cv').width($('div#tab_plugin_stlviewer').width());
        };
	}

	// This is how our plugin registers itself with the application, by adding some configuration information to
	// the global variable ADDITIONAL_VIEWMODELS
	ADDITIONAL_VIEWMODELS.push([
			// This is the constructor to call for instantiating the plugin
			stlviewerViewModel,

			// This is a list of dependencies to inject into the plugin, the order which you request here is the order
			// in which the dependencies will be injected into your view model upon instantiation via the parameters
			// argument
			["filesViewModel"],

			// Finally, this is the list of all elements we want this view model to be bound to.
			[("#tab_plugin_stlviewer")]
		]);
});
