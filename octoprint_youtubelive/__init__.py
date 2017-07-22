# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class youtubelive(octoprint.plugin.StartupPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.AssetPlugin,
                octoprint.plugin.SettingsPlugin):
					   
	def on_after_startup(self):
		self._logger.info("OctoPrint-YouTubeLive loaded!")

	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=False)]

	def get_assets(self):
		return dict(
			js=["js/youtubelive.js"],
			css=["css/youtubelive.css"]
		)
		
	def get_settings_defaults(self):
		return dict(channel_id="")	

__plugin_name__ = "YouTube Live"
__plugin_implementation__ = youtubelive()
