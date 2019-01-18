import subsync.gui.layout.settingswin
from subsync.gui.filedlg import showSaveFileDlg
from subsync.settings import Settings
from subsync import config
import multiprocessing
import wx


class SettingsWin(subsync.gui.layout.settingswin.SettingsWin):
    def __init__(self, parent, settings, cache=None):
        super().__init__(parent)
        self.m_outputCharEnc.SetString(0, _('same as input subtitles'))

        if not config.assetupd:
            self.m_textUpdates.Hide()
            self.m_autoUpdate.Hide()
            self.m_askForUpdate.Hide()

        self.setSettings(settings)

        self.cache = cache
        self.m_buttonClearCache.Enable(cache and not cache.isEmpty())

    def setSettings(self, settings):
        self.settings = Settings(settings)

        self.m_jobsNo.SetValue(max(multiprocessing.cpu_count(), 2))

        for field, key, val in self.settingsFieldsGen():
            if val != None:
                field.SetValue(val)

        jobsNo = self.settings.jobsNo
        self.m_checkAutoJobsNo.SetValue(jobsNo == None)
        self.m_jobsNo.Enable(jobsNo != None)

        logLevel = self.settings.logLevel / 10
        if logLevel >= 0 and logLevel < self.m_choiceLogLevel.GetCount():
            self.m_choiceLogLevel.SetSelection(logLevel)

        logFile = self.settings.logFile
        self.m_checkLogToFile.SetValue(logFile != None)
        self.m_textLogFilePath.Enable(logFile != None)
        self.m_buttonLogFileSelect.Enable(logFile != None)
        self.m_textLogFilePath.SetValue(logFile if logFile else '')

        logBlacklist = self.settings.logBlacklist
        if logBlacklist == None:
            logBlacklist = []
        self.m_textLogBlacklist.SetValue('\n'.join(logBlacklist))

    def getSettings(self):
        for field, key, val in self.settingsFieldsGen():
            setattr(self.settings, key, field.GetValue())

        if self.m_checkAutoJobsNo.IsChecked():
            self.settings.jobsNo = None

        logLevel = self.m_choiceLogLevel.GetSelection()
        if logLevel != wx.NOT_FOUND:
            self.settings.logLevel = logLevel * 10

        if self.m_checkLogToFile.IsChecked():
            self.settings.logFile = self.m_textLogFilePath.GetValue()
        else:
            self.settings.logFile = None

        logBlacklist = self.m_textLogBlacklist.GetValue().split()
        if len(logBlacklist) > 0:
            self.settings.logBlacklist = logBlacklist
        else:
            self.settings.logBlacklist = None

        return self.settings

    def settingsFieldsGen(self):
        for key, val in self.settings.items().items():
            field = 'm_' + key
            if hasattr(self, field):
                yield getattr(self, field), key, val

    def onCheckAutoJobsNoCheck(self, event):
        auto = self.m_checkAutoJobsNo.IsChecked()
        self.m_jobsNo.Enable(not auto)

    def onCheckLogToFileCheck(self, event):
        enabled = self.m_checkLogToFile.IsChecked()
        self.m_textLogFilePath.Enable(enabled)
        self.m_buttonLogFileSelect.Enable(enabled)

    def onButtonLogFileSelectClick(self, event):
        path = showSaveFileDlg(self)
        if path != None:
            self.m_textLogFilePath.SetValue(path)

    def onButtonRestoreDefaultsClick(self, event):
        dlg = wx.MessageDialog(
                self,
                _('Are you sure you want to reset settings to defaults?'),
                _('Restore defaults'),
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            self.setSettings(Settings())

    def onButtonClearCache(self, event):
        if self.cache:
            self.cache.clear()
        self.m_buttonClearCache.Disable()

