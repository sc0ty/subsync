import gui.downloadwin_layout
import gui.errorwin
import wx
import sys
import asyncio
import threading
import config
import assets
import assets.updater
import assets.downloader
import thread
from settings import settings
from utils import fileSizeFmt

import logging
logger = logging.getLogger(__name__)


class DownloadWin(gui.downloadwin_layout.DownloadWin):
    def __init__(self, parent, title, job):
        super().__init__(parent)
        self.m_textName.SetLabel(title)

        self.loop = None
        self.task = None

        self.thread = threading.Thread(name='Download', target=self.run, args=[job])
        self.thread.start()

    def stop(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.task.cancel)
        if self.thread.isAlive():
            self.thread.join()

    def onButtonCancelClick(self, event):
        self.stop()

    @thread.gui_thread
    def EndModal(self, retCode):
        if self.IsModal():
            return super().EndModal(retCode)

    def run(self, job):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.task = asyncio.ensure_future(self.jobWrapper(job))
        self.loop.run_until_complete(self.task)

    async def jobWrapper(self, job):
        try:
            await job

        except asyncio.CancelledError:
            logger.info('operation cancelled by user')
            self.EndModal(wx.ID_CANCEL)

        except Exception as e:
            logger.error('download failed, %r', e, exc_info=True)
            self.setStatus(_('operation failed'))

            @thread.gui_thread
            def showExceptionDlgAndQuit(excInfo):
                if self.IsModal():
                    gui.errorwin.showExceptionDlg(self, excInfo)
                    self.EndModal(wx.ID_CANCEL)

            showExceptionDlgAndQuit(sys.exc_info())

    async def downloadJob(self, asset):
        downloader = assets.downloader.AssetDownloader(**asset)

        self.setStatus(_('downloading...'))
        fp, hash = await downloader.download(lambda progress:
                self.setStatus(_('downloading'), progress))

        self.setProgress(1)
        self.setStatus(_('verifying...'))
        await downloader.verify(hash)

        self.setStatus(_('processing...'))
        await downloader.install(fp)
        self.setStatus(_('done'))

    @thread.gui_thread
    def setStatus(self, status, progress=None):
        if progress:
            pos, size = progress
            if size:
                self.m_gaugeProgress.SetValue(min(100, int(100.0 * pos / size)))
                msg = '{} {} / {}'.format(status, fileSizeFmt(pos), fileSizeFmt(size))
            else:
                self.m_gaugeProgress.Pulse()
                msg = '{} {}'.format(status, fileSizeFmt(pos))
        else:
            msg = status
        self.m_textDetails.SetLabel(msg)

    @thread.gui_thread
    def setProgress(self, val):
        self.m_gaugeProgress.SetValue(min(100, int(100.0 * val)))


class AssetDownloadWin(DownloadWin):
    def __init__(self, parent, asset):
        super().__init__(parent, asset['title'], job=self.downloadAssetJob(asset))

    async def downloadAssetJob(self, asset):
        await self.downloadJob(asset)
        self.EndModal(wx.ID_OK)


class SelfUpdaterWin(DownloadWin):
    def __init__(self, parent):
        title = _('Application upgrade')
        super().__init__(parent, title, job=self.updateJob())

    def onButtonCancelClick(self, event):
        self.EndModal(wx.ID_CLOSE)

    async def updateJob(self):
        logger.info('new version is available for update')
        if not assets.updater.getLocalUpdate():
            asset = assets.getRemoteAsset(**config.assetupd)
            await self.downloadJob(asset)

        self.setProgress(1)
        self.setStatus(_('update ready'))

        @thread.gui_thread
        def askForUpdateIfVisible():
            if self.IsModal():
                self.askForUpdate(self)

        askForUpdateIfVisible()

    @gui.errorwin.error_dlg
    def startUpdate(self, parent, ask=True):
        if self.thread.is_alive():
            return super().ShowModal() == wx.ID_OK
        elif ask:
            return self.askForUpdate(parent)
        else:
            assets.updater.installLocalUpdate()
            return True

    @gui.errorwin.error_dlg
    def askForUpdate(self, parent=None):
        dlg = wx.MessageDialog(
                parent if parent else self,
                _('New version is ready to be installed. Upgrade now?'),
                _('Upgrade'),
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            self.EndModal(wx.ID_OK)
            assets.updater.installLocalUpdate()
            return True

        else:
            self.EndModal(wx.ID_CANCEL)
            return False

