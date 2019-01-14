# Dictionary scripts
Various Python scripts used to generate SubSync dictionaries.

## Dictionary converters
Scripts converting various dictionaries to SubSync _dict_ files.

1. Wiktionary dicts

`convert_wikdict.py SRC_DIR DST_DIR VERSION [MIN_KEYS]`

2. IATE dicts

`convert_iate.py SRC_PATH DST_DIR VERSION [MIN_KEYS]`

3. svobodneslovniky.cz dict (English/Czech dictionary)

`convert_svobodneslovniky.py SRC_PATH DST_DIR VERSION`

## Dictionary merger
Merges multiple dicts of the same languages to single _dict_ file.

`merge_dicts.py SRC_DIR1 [SRC_DIR2] [SRC_DIR3...] DST_DIR MIN_KEYS`

## Conversion example
Using above scripts to generate output dicts
```
convert_wikdict.py wikidict dict/wikidict 1.0.0
convert_iate.py IATE_export_07112018.tbx dict/iate 1.0.0
convert_svobodneslovniky.py en-cs.txt dict/svobodneslovniky 1.0.0
merge_dicts.py dict/wikidict dict/iate dict/svobodneslovniky dict/out 10000
```
