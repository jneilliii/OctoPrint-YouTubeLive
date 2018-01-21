# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os
from octoprint.server import user_permission

class youtubelive(octoprint.plugin.StartupPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.AssetPlugin,
                octoprint.plugin.SettingsPlugin,
				octoprint.plugin.SimpleApiPlugin):
	
	##~~ StartupPlugin
	def on_after_startup(self):
		self._logger.info("OctoPrint-YouTubeLive loaded!")
	
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
		return dict(channel_id="",stream_id="",process="",ffmpeg="nano",streaming=False)
		
	##~~ SimpleApiPlugin mixin
	
	def get_api_commands(self):
		return dict(startStream=[],stopStream=[])
		
	def on_api_command(self, command, data):
		if not user_permission.can():
			from flask import make_response
			return make_response("Insufficient rights", 403)
			
		if command == 'startStream':
			try:			
				from subprocess import Popen
				import sys
				DETACHED_PROCESS = 0x00000008
				cmd = [
					sys.executable,
					self._settings.get(["ffmpeg"])
				]
				if os.name == 'nt':
					self.process = Popen(cmd,shell=False,stdin=None,stdout=None,stderr=None,close_fds=True,creationflags=DETACHED_PROCESS)
				else:
					self.process = Popen(cmd,shell=False,stdin=None,stdout=None,stderr=None,close_fds=True)
				
				self._logger.info("channel: %s stream: %s pid: %s" % (self._settings.get(["channel_id"]),self._settings.get(["stream_id"]),self.process.pid))
				self._plugin_manager.send_plugin_message(self._identifier, dict(streaming=True))
			except Exception, e:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error=str(e),streaming=False))
			return
		if command == 'stopStream':
			try:
				self._logger.info("Stop stream command received, pid: %s" % self._settings.get(["stream_id"]),self.process.pid)
				self._plugin_manager.send_plugin_message(self._identifier, dict(streaming=False))
			except Exception, e:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error=str(e)))

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
