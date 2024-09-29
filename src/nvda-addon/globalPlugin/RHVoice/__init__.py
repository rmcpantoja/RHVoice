# Copyright (C) 2022 Alexander Linkov <kvark128@yandex.ru>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import wx
import gui
import globalVars
import globalPluginHandler
import addonHandler
from synthDrivers import RHVoice
from .downloader import VoiceDownloader

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		if globalVars.appArgs.secure:
			return
		if not RHVoice.SynthDriver.check():
			wx.CallLater(2000, self.onNoVoicesInstalled)
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.rhvoiceUi = self.toolsMenu.Append(
			wx.ID_ANY, _("RHVoice downloader"),
			_("Download and update languages and voices")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onUI, self.rhvoiceUi)

	def onUI(self, evt):
		gui.mainFrame.popupSettingsDialog(VoiceDownloader)

	def onNoVoicesInstalled(self):
		# Translators: title of the message box for the user
		title = _("RHVoice Warning")
		message = _(
			# Translators: message shown to the user if there are no installed voices
			"To use RHVoice, at least one voice add-on must be installed in your NVDA copy.\n"
			"If you don't have voices installed yet, you can download one using the downloader under NVDA's tools menu\n"
			"Do you want to open the voice downloader now?"
		)
		style = wx.YES|wx.NO|wx.ICON_WARNING
		if gui.messageBox(message, title, style) == wx.YES:
			gui.mainFrame.popupSettingsDialog(VoiceDownloader)