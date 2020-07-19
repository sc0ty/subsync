from subsync.translations import _
from subsync.data import languages
from subsync import error


class AssetList(list):
    """List of assets.

    Used mainly to select assets required for synchronization.
    """

    def missing(self):
        """Get missing assets (as new `AssetList`).

        Missing assets are assets that are not available locally nor remotely
        on asset server.
        """
        return AssetList([ a for a in self if a.isMissing() ])

    def hasUpdate(self):
        """Get assets that could be updated (as new `AssetList`).

        These assets are available on asset server and are not installed locally
        or remote version are newer than local (based on version number).
        """
        return AssetList([ a for a in self if a.hasUpdate() ])

    def installed(self):
        """Get assets installed locally and ready to use (as new `AssetList`)."""
        return AssetList([ a for a in self if a.localVersion() ])

    def notInstalled(self):
        """Get assets that are not installed locally (as new `AssetList`)."""
        return AssetList([ a for a in self if not a.localVersion() ])

    def validate(self, localOnly=False):
        """Check if all assets on the list are available.

        Parameters
        ----------
        localOnly: bool, optional
            If `True` this method will check if all assets are installed
            locally, otherwise it will check if assets are available either
            locally or on asset server.

        Raises
        ------
        Error
            At least one asset is not available.
        """
        if localOnly:
            assets = self.notInstalled()
        else:
            assets = self.missing()

        if assets:
            msg = []
            speech = [ asset for asset in assets if asset.type == 'speech' ]
            dicts  = [ asset for asset in assets if asset.type == 'dict' ]

            if speech:
                langs = ', '.join([ languages.getName(a.params[0]) for a in speech ])
                msg += [ _('Synchronization with {} audio is currently not supported.') \
                        .format(langs) ]
            if dicts:
                langs = [ ' - '.join([ languages.getName(p) for p in a.params ]) for a in dicts ]
                msg += [ _('Synchronization between languages {} is currently not supported.') \
                        .format(', '.join(langs)) ]

            msg += [ '', _('missing assets:') ]
            msg += [ ' - ' + asset.getPrettyName() for asset in assets ]
            raise error.Error('\n'.join(msg))

