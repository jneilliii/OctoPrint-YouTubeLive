# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class youtubelive(octoprint.plugin.StartupPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.AssetPlugin,
                octoprint.plugin.SettingsPlugin):
	
	##~~ StartupPlugin
	def on_after_startup(self):
		self._logger.info("OctoPrint-YouTubeLive loaded!")
	
	##~~ TemplatePlugin
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]
		
	##~~ AssetPlugin
	def get_assets(self):
		return dict(
			js=["js/youtubelive.js"],
			css=["css/youtubelive.css"]
		)
	
	##~~ SettingsPlugin
	def get_settings_defaults(self):
		return dict(channel_id="")

	##~~ Softwareupdate hook
	def get_update_information(self):
		return dict(
			youtubelive=dict(
				displayName="YouTube Live",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="jneilliii",
				repo="OctoPrint-YouTubeLive",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/jneilliii/OctoPrint-YouTubeLive/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "YouTube Live"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = youtubelive()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
