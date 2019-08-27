#include "catch.hpp"
#include "text/ngrams.h"
#include <vector>

using namespace std;


TEST_CASE("NgramSplitter")
{
	vector<Word> words;
	NgramSplitter splitter = NgramSplitter(3);

	splitter.addWordsListener( [&words](const Word &w) {
		words.push_back(w);
	});

	SECTION("word too short to split")
	{
		splitter.pushWord(Word("ab", 0.0f));
		REQUIRE( words.size() == 0 );
	}

	SECTION("word size equals n-gram size")
	{
		splitter.pushWord(Word("abc", 0.0f));
		REQUIRE( words.size() == 1 );
		REQUIRE( words[0].text == "abc" );
	}

	SECTION("word size longer than n-gram size")
	{
		splitter.pushWord(Word("abcd", 0.0f));
		REQUIRE( words.size() == 2 );
		REQUIRE( words[0].text == "abc" );
		REQUIRE( words[1].text == "bcd" );
	}

	SECTION("split multiple words")
	{
		splitter.pushWord(Word("abcd", 0.0f));
		splitter.pushWord(Word("qwert", 0.0f));
		REQUIRE( words.size() == 5 );
		REQUIRE( words[0].text == "abc" );
		REQUIRE( words[1].text == "bcd" );
		REQUIRE( words[2].text == "qwe" );
		REQUIRE( words[3].text == "wer" );
		REQUIRE( words[4].text == "ert" );
	}

	SECTION("word too short to split (multi-byte codepoints)")
	{
		splitter.pushWord(Word( "\xc3\xb1" "\xe2\x82\xa1", 0.0f));
		REQUIRE( words.size() == 0 );
	}

	SECTION("word size equals n-gram size (multi-byte codepoints)")
	{
		splitter.pushWord(Word( "\xc3\xb1" "\xe2\x82\xa1" "\xef\xbf\xbd" , 0.0f));
		REQUIRE( words.size() == 1 );
		REQUIRE( words[0].text == "\xc3\xb1" "\xe2\x82\xa1" "\xef\xbf\xbd" );
	}

	SECTION("word size longer than n-gram size (multi-byte codepoints)")
	{
		splitter.pushWord(Word( "\xc3\xb1" "\xe2\x82\xa1" "\xef\xbf\xbd" "\xdf\xbf"  , 0.0f));
		REQUIRE( words.size() == 2 );
		REQUIRE( words[0].text == "\xc3\xb1" "\xe2\x82\xa1" "\xef\xbf\xbd" );
		REQUIRE( words[1].text == "\xe2\x82\xa1" "\xef\xbf\xbd" "\xdf\xbf" );
	}

	SECTION("check time for single n-gram")
	{
		splitter.pushWord(Word( "abc", 10.0f, 2.0f ));
		REQUIRE( words.size() == 1 );
		REQUIRE( words[0].time >= 10.0f );
		REQUIRE( words[0].time <= 12.0f );
		REQUIRE( words[0].duration <= 2.0f );
	}

	SECTION("check time for multipel n-grams")
	{
		splitter.pushWord(Word( "abcdef", 10.0f, 4.0f ));
		REQUIRE( words.size() == 4 );
		REQUIRE( words[0].time >= 10.0f );
		REQUIRE( words[1].time > words[0].time );
		REQUIRE( words[2].time > words[1].time );
		REQUIRE( words[3].time > words[2].time );
		REQUIRE( words[3].time <= 14.0f );
		REQUIRE( words[0].duration <= 2.0f );
		REQUIRE( words[1].duration <= 2.0f );
		REQUIRE( words[2].duration <= 2.0f );
		REQUIRE( words[3].duration <= 2.0f );
	}

	SECTION("check time for single n-gram without duration")
	{
		splitter.pushWord(Word( "abc", 10.0f, 0.0f ));
		REQUIRE( words.size() == 1 );
		REQUIRE( words[0].time == Approx(10.0f) );
		REQUIRE( words[0].duration == Approx(0.0f) );
	}

	SECTION("check time for multipel n-grams without duration")
	{
		splitter.pushWord(Word( "abcdef", 10.0f, 0.0f ));
		REQUIRE( words.size() == 4 );
		REQUIRE( words[0].time == Approx(10.0f) );
		REQUIRE( words[1].time == Approx(10.0f) );
		REQUIRE( words[2].time == Approx(10.0f) );
		REQUIRE( words[3].time == Approx(10.0f) );
		REQUIRE( words[0].duration == Approx(0.0f) );
		REQUIRE( words[1].duration == Approx(0.0f) );
		REQUIRE( words[2].duration == Approx(0.0f) );
		REQUIRE( words[3].duration == Approx(0.0f) );
	}
}
