WIKDICT_TEMP_DIR = $(TEMP_DIR)/wikdict
WIKDICT_PART_DIR = $(PART_DIR)/wikdict
PARTS += $(WIKDICT_PART_DIR)

WIKDICT_PAIRS = \
				bg-de bg-el bg-en bg-es bg-fi bg-fr bg-id bg-it bg-ja bg-la \
				bg-lt bg-mg bg-nl bg-no bg-pl bg-pt bg-ru bg-sv bg-tr de-bg \
				de-el de-en de-es de-fi de-fr de-id de-it de-ja de-la de-lt \
				de-mg de-nl de-no de-pl de-pt de-ru de-sv de-tr el-bg el-de \
				el-en el-es el-fi el-fr el-id el-it el-ja el-la el-lt el-mg \
				el-nl el-no el-pl el-pt el-ru el-sv el-tr en-bg en-de en-el \
				en-es en-fi en-fr en-id en-it en-ja en-la en-lt en-mg en-nl \
				en-no en-pl en-pt en-ru en-sv en-tr es-bg es-de es-el es-en \
				es-fi es-fr es-id es-it es-ja es-la es-lt es-mg es-nl es-no \
				es-pl es-pt es-ru es-sv es-tr fi-bg fi-de fi-el fi-en fi-es \
				fi-fr fi-id fi-it fi-ja fi-la fi-lt fi-mg fi-nl fi-no fi-pl \
				fi-pt fi-ru fi-sv fi-tr fr-bg fr-de fr-el fr-en fr-es fr-fi \
				fr-id fr-it fr-ja fr-la fr-lt fr-mg fr-nl fr-no fr-pl fr-pt \
				fr-ru fr-sv fr-tr id-bg id-de id-el id-en id-es id-fi id-fr \
				id-it id-ja id-la id-lt id-mg id-nl id-no id-pl id-pt id-ru \
				id-sv id-tr it-bg it-de it-el it-en it-es it-fi it-fr it-id \
				it-ja it-la it-lt it-mg it-nl it-no it-pl it-pt it-ru it-sv \
				it-tr ja-bg ja-de ja-el ja-en ja-es ja-fi ja-fr ja-id ja-it \
				ja-la ja-lt ja-mg ja-nl ja-no ja-pl ja-pt ja-ru ja-sv ja-tr \
				la-bg la-de la-el la-en la-es la-fi la-fr la-id la-it la-ja \
				la-lt la-mg la-nl la-no la-pl la-pt la-ru la-sv la-tr lt-bg \
				lt-de lt-el lt-en lt-es lt-fi lt-fr lt-id lt-it lt-ja lt-la \
				lt-mg lt-nl lt-no lt-pl lt-pt lt-ru lt-sv lt-tr mg-bg mg-de \
				mg-el mg-en mg-es mg-fi mg-fr mg-id mg-it mg-ja mg-la mg-lt \
				mg-nl mg-no mg-pl mg-pt mg-ru mg-sv mg-tr nl-bg nl-de nl-el \
				nl-en nl-es nl-fi nl-fr nl-id nl-it nl-ja nl-la nl-lt nl-mg \
				nl-no nl-pl nl-pt nl-ru nl-sv nl-tr no-bg no-de no-el no-en \
				no-es no-fi no-fr no-id no-it no-ja no-la no-lt no-mg no-nl \
				no-pl no-pt no-ru no-sv no-tr pl-bg pl-de pl-el pl-en pl-es \
				pl-fi pl-fr pl-id pl-it pl-ja pl-la pl-lt pl-mg pl-nl pl-no \
				pl-pt pl-ru pl-sv pl-tr pt-bg pt-de pt-el pt-en pt-es pt-fi \
				pt-fr pt-id pt-it pt-ja pt-la pt-lt pt-mg pt-nl pt-no pt-pl \
				pt-ru pt-sv pt-tr ru-bg ru-de ru-el ru-en ru-es ru-fi ru-fr \
				ru-id ru-it ru-ja ru-la ru-lt ru-mg ru-nl ru-no ru-pl ru-pt \
				ru-sv ru-tr sv-bg sv-de sv-el sv-en sv-es sv-fi sv-fr sv-id \
				sv-it sv-ja sv-la sv-lt sv-mg sv-nl sv-no sv-pl sv-pt sv-ru \
				sv-tr tr-bg tr-de tr-el tr-en tr-es tr-fi tr-fr tr-id tr-it \
				tr-ja tr-la tr-lt tr-mg tr-nl tr-no tr-pl tr-pt tr-ru tr-sv \

WIKDICT_SQL = $(patsubst %,$(WIKDICT_TEMP_DIR)/%.sqlite3,$(WIKDICT_PAIRS))

download: $(WIKDICT_SQL)
convert: wikdict


wikdict: $(WIKDICT_SQL)
	@mkdir -p $(WIKDICT_PART_DIR)
	$(SCRIPTS_DIR)/wikdict_convert.py $(WIKDICT_TEMP_DIR) $(WIKDICT_PART_DIR) $(DICT_VERSION)

$(WIKDICT_SQL): 
	@mkdir -p $(WIKDICT_TEMP_DIR)
	wget -nv -O $@ http://download.wikdict.com/dictionaries/sqlite/2/$(notdir $@)
