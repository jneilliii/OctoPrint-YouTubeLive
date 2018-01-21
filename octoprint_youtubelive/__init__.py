# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.server import user_permission
import docker

class youtubelive(octoprint.plugin.StartupPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.AssetPlugin,
                octoprint.plugin.SettingsPlugin,
				octoprint.plugin.SimpleApiPlugin):
	
	def __init__(self):
		self.client = docker.from_env()
		try:
			self.container = client.containers.get('YouTubeLive')
		except Exception, e:
			self.container = None
	
	##~~ StartupPlugin
	def on_after_startup(self):
		self._logger.info("OctoPrint-YouTubeLive loaded!")
		if self.container:
			self._plugin_manager.send_plugin_message(self._identifier, dict(status=True,streaming=True))
	
	##~~ TemplatePlugin
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=False)]
		
	##~~ AssetPlugin
	def get_assets(self):
		return dict(
			js=["js/youtubelive.js"],
			css=["css/youtubelive.css"]
		)
		
	##~~ SettingsPlugin
	def get_settings_defaults(self):
		return dict(channel_id="",stream_id="",streaming=False)
		
	##~~ SimpleApiPlugin mixin
	
	def get_api_commands(self):
		return dict(startStream=[],stopStream=[])
		
	def on_api_command(self, command, data):
		if not user_permission.can():
			from flask import make_response
			return make_response("Insufficient rights", 403)
		
		if command == 'startStream':
			self._logger.info("Start stream command received for stream: %s" % self._settings.get(["stream_id"]))
			if not self.container:
				try:
					client.containers.run("alexellis2/streaming:17-5-2017",command="pbea-b3pr-8513-40mh",detach=True,privileged=True,name="YouTubeLive",auto_remove=True)
					self._plugin_manager.send_plugin_message(self._identifier, dict(status=True,streaming=True))
				except Exception, e:
					self._plugin_manager.send_plugin_message(self._identifier, dict(error=str(e),status=True,streaming=False))
			return
		if command == 'stopStream':
			self._logger.info("Stop stream command received.")
			if self.container:
				try:
					container.stop()
					self._plugin_manager.send_plugin_message(self._identifier, dict(status=True,streaming=False))
				except Exception, e:
					self._plugin_manager.send_plugin_message(self._identifier, dict(error=str(e),status=True,streaming=False))

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
