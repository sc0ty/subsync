# SubSync assets overview
Assets are downloadable packages used by SubSync. Currently, there are three types of assets:
- speech recognition model;
- dictionary;
- self updater.

Assets available on server are listed in [assets.json](https://github.com/sc0ty/subsync/releases/download/assets/assets.json).

## Dictionary
Used for translation subtitles when reference is in another language.
Languages are encoded in file name as `[lang1]-[lang2].dict`.
It is text file with one phrase per line with translations separated by `|`.
Lines beginning with `#` are omitted (commented out).
Example:
```
# Example dictionary file
phrase1|translation1
phrase2|translation2a|translation2b
```

## Speech recognition model
Used in text-to-speech conversion.
Consist of several files, including acoustic and language model, list of words and JSON description.
Description file is named as `[lang].speech` and contains model parameters.
This is the configuration for pocketsphinx library.
My knowledge about Sphinx models is very limited, I never created one by myself, just using publicly available ones.
If you created such model and want to share, please let me know and I will make asset for SubSync from it.

For more information please refer to CMUSphinx [docs](https://cmusphinx.github.io/wiki/).
