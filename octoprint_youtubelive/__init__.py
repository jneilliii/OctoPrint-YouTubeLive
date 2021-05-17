# coding=utf-8
from __future__ import absolute_import

import os
import subprocess
import shlex
import threading
from collections import deque
from threading import Thread

import flask
import octoprint.plugin
from octoprint.access.permissions import Permissions, ADMIN_GROUP
from flask_babel import gettext
from octoprint.util.commandline import CommandlineCaller, CommandlineError


class youtubelive(octoprint.plugin.StartupPlugin,
                  octoprint.plugin.TemplatePlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.SimpleApiPlugin,
                  octoprint.plugin.EventHandlerPlugin):

    def __init__(self):
        # self.client = docker.from_env()
        self.container = None
        self.stream_thread = threading.Thread(target=self.start_stream)
        self.stream_thread.daemon = True

    ##~~ StartupPlugin

    def on_after_startup(self):
        self._logger.info("OctoPrint-YouTubeLive loaded!")

    # try:
    # self.container = self.client.containers.get('YouTubeLive')
    # self._logger.info("%s is streaming " % self.container.name)
    # self._plugin_manager.send_plugin_message(self._identifier, dict(status=True,streaming=True))
    # except Exception as e:
    # self._logger.error(str(e))
    # self._plugin_manager.send_plugin_message(self._identifier, dict(status=True,streaming=False))

    ##~~ TemplatePlugin

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    ##~~ AssetPlugin

    def get_assets(self):
        return dict(
            js=["js/youtubelive.js"],
            css=["css/youtubelive.css"]
        )

    ##~~ SettingsPlugin

    def get_settings_defaults(self):
        return dict(channel_id="",
                    stream_id="",
                    streaming=False,
                    auto_start=False,
                    ffmpeg_cmd_options="-re -f mjpeg -framerate 5 -i http://localhost:8080/?action=stream -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -acodec aac -ab 128k -strict experimental -vcodec h264 -threads 1 -pix_fmt yuv420p -g 10 -vb 700k -framerate 5")

    ##~~ SimpleApiPlugin

    def get_api_commands(self):
        return dict(startStream=[], stopStream=[], checkStream=[])

    def on_api_command(self, command, data):
        if not Permissions.PLUGIN_YOUTUBELIVE_STREAM.can():
            return flask.make_response("Insufficient rights", 403)

        if command == 'startStream':
            self._logger.info("Start stream command received.")
            if not self.stream_thread.isAlive():
                self.stream_thread.start()

        if command == 'stopStream':
            self._logger.info("Stop stream command received.")
            self.stop_stream()

        if command == 'checkStream':
            self._logger.info("Checking stream status.")
            if self.container:
                self._plugin_manager.send_plugin_message(self._identifier, dict(status=True, streaming=True))
            else:
                self._plugin_manager.send_plugin_message(self._identifier, dict(status=True, streaming=False))

    ##-- EventHandlerPlugin

    def on_event(self, event, payload):
        if event == "PrintStarted" and self._settings.get(["auto_start"]):
            if not self.stream_thread.isAlive():
                self.stream_thread.start()

        if event in ["PrintDone", "PrintCancelled"] and self._settings.get(["auto_start"]):
            self.stop_stream()

    ##-- Utility Functions

    def start_stream(self):
        if not self.container:
            filters = []
            if self._settings.global_get(["webcam", "flipH"]):
                filters.append("hflip")
            if self._settings.global_get(["webcam", "flipV"]):
                filters.append("vflip")
            if self._settings.global_get(["webcam", "rotate90"]):
                filters.append("transpose=cclock")
            if len(filters) == 0:
                filters.append("null")
            try:
                # self.container = self.client.containers.run("octoprint/youtubelive:latest",command=[self._settings.global_get(["webcam","stream"]),self._settings.get(["stream_id"]),",".join(filters)],detach=True,privileged=False,devices=["/dev/vchiq"],name="YouTubeLive",auto_remove=True,network_mode="host")
                ffmpeg_cmd = "{} {} -f flv rtmp://a.rtmp.youtube.com/live2/{}".format(
                    self._settings.global_get(["webcam", "ffmpeg"]), self._settings.get(["ffmpeg_cmd_options"]),
                    self._settings.get(["stream_id"]))
                # replace this with actual subprocess command
                FNULL = open(os.devnull, 'w')
                # container = subprocess.Popen(shlex.split(ffmpeg_cmd, posix=(os.name == "posix")), stdout=subprocess.PIPE, stderr=FNULL, universal_newlines=True)
                self.container = CommandlineCaller()
                self.container.on_log_stderr = self.log_stderr
                self.container.on_log_stdout = self.log_stdout
                self.container.on_log_call = self.log_call
                try:
                    self.container.checked_call(ffmpeg_cmd)  # shlex.split(ffmpeg_cmd, posix=(os.name == "posix"))
                except CommandlineError as err:
                    self._logger.debug("Command  \"{}\" returned {}".format(ffmpeg_cmd, err.returncode))
                    self._plugin_manager.send_plugin_message(self._identifier, dict(error=str(err), status=True, streaming=False))
                else:
                    self._logger.debug("Command \"{}\" errored.".format(ffmpeg_cmd))
                    self._plugin_manager.send_plugin_message(self._identifier, dict(error="Couldn't start.", status=True, streaming=False))
            except Exception as e:
                self._logger.debug("Command \"{}\" error: {}".format(ffmpeg_cmd, e))
                self._plugin_manager.send_plugin_message(self._identifier, dict(status=True, streaming=False))
        return

    def log(self, prefix, *lines):
        for line in lines:
            self._logger.debug("{} {}".format(prefix, line))

    def log_stdout(self, *lines):
        self.log(">>>", *lines)

    def log_stderr(self, *lines):
        self.log("!!!", *lines)

    def log_call(self, *lines):
        self.log("---", *lines)
        self._plugin_manager.send_plugin_message(self._identifier, dict(status=True, streaming=True))

    def stop_stream(self):
        if self.container:
            try:
                self.container.kill()
                self.container = None
                self._plugin_manager.send_plugin_message(self._identifier, dict(status=True, streaming=False))
            except Exception as e:
                self._plugin_manager.send_plugin_message(self._identifier,
                                                         dict(error=str(e), status=True, streaming=False))
        else:
            self._plugin_manager.send_plugin_message(self._identifier, dict(status=True, streaming=False))

    ##~~ Access Permissions Hook

    def get_additional_permissions(self, *args, **kwargs):
        return [
            dict(key="STREAM",
                 name="Stream YouTube",
                 description=gettext("Allows control of YouTube streaming."),
                 roles=["admin"],
                 dangerous=True,
                 default_groups=[ADMIN_GROUP])
        ]

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
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = youtubelive()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.access.permissions": __plugin_implementation__.get_additional_permissions,
    }
