"""Subtitle Synchronizer"""

from subsync.synchro.synchronizer import Synchronizer
from subsync.synchro.controller import SyncController, SyncJobResult, SyncStatus
from subsync.synchro.task import SyncTask, SyncTaskList
from subsync.synchro.input import InputFile, SubFile, RefFile
from subsync.synchro.output import OutputFile
from subsync.synchro.channels import ChannelsMap

__all__ = [
        'Synchronizer', 'SyncController',
        'SyncTask', 'SyncTaskList',
        'InputFile', 'SubFile', 'RefFile', 'OutputFile',
        'ChannelsMap' ]

__pdoc__ = { key: False for key in [
        'dictionary', 'encdetect', 'pipeline', 'speech', 'synchronizer',
        'wordsdump', 'SyncTaskList',
        ]}
