# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class stlviewer(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin):
					   
	def on_after_startup(self):
		self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

	def get_settings_defaults(self):
		return dict(url="https://en.wikipedia.org/wiki/Hello_world")

	def get_template_configs(self):
		return [
		]

	def get_assets(self):
		return dict(
			js=["js/stlviewer.js","js/jsc3d.console.js","js/jsc3d.js","js/jsc3d.touch.js","js/sonic.js"],
			css=["css/stlviewer.css"],
			less=["less/stlviewer.less"]
		)

__plugin_name__ = "OctoPrint-STLViewer"
__plugin_implementation__ = stlviewer()
