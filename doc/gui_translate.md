# SubSync GUI translate
SubSync internalization is done with gettext package, using standarised file formats.
Translation files are located in `subsync/locale/[LANG]/LC_MESSAGES` directories, containing two files: `messages.po` and `messages.mo`. First one is text file with translations from which second one (binary) is generated.

In order to create new translation, just copy one of existing `messages.po`, put it in directory according to language 2-letter code, edit po file e.g. with [Poedit](https://poedit.net) and generate `messages.mo` from it.

Language codes are stored in [languages.py](../subsync/data/languages.py). Check if your language is present on `languages2to3`. If not, you may have to add it manually here and also to `languages` dictionary.

If you managed to translate SubSync to different language, please create pull request, or share `messages.po` with me.
