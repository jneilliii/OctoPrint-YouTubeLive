# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class stlviewer(octoprint.plugin.StartupPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.AssetPlugin):
					   
	def on_after_startup(self):
		self._logger.info("STL Viewer loaded!")

	def get_template_configs(self):
		return []

	def get_assets(self):
		return dict(
			js=["js/stlviewer.js","js/jsc3d.js","js/jsc3d.touch.js"]
		)

__plugin_name__ = "STL Viewer"
__plugin_implementation__ = stlviewer()
