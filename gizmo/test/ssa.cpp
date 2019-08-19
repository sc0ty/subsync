#include "catch.hpp"
#include "text/ssa.h"
#include <string>

using namespace std;


static const string getWord(const SSAParser::Words &words, size_t no)
{
	for (const string &word : words)
	{
		if (no-- == 0)
			return word;
	}
	throw string("index out of range");
}


TEST_CASE("SSA Parser")
{
	SECTION("parsing SSA special sequences")
	{
		SSAParser p;
		SSAParser::Words w;

		w = p.splitWords("abc{\\def}ghi");
		REQUIRE( w.size() == 2 );
		REQUIRE( getWord(w, 0) == "abc" );
		REQUIRE( getWord(w, 1) == "ghi" );

		w = p.splitWords("abc{{\\c}ghi");
		REQUIRE( w.size() == 2 );
		REQUIRE( getWord(w, 0) == "abc{" );
		REQUIRE( getWord(w, 1) == "ghi" );

		w = SSAParser(false, " \t\n.,!?[]{}():<>|\\/\"#$%-+`").splitWords("-'Cause the cops say he's dead--");
		REQUIRE( w.size() == 6 );
	}

	SECTION("SSA words split left-to-right")
	{
		SSAParser p(false, " ");
		SSAParser::Words w;

		w = p.splitWords("abc");
		REQUIRE( w.size() == 1 );
		REQUIRE( getWord(w, 0) == "abc" );

		w = p.splitWords("abc def");
		REQUIRE( w.size() == 2 );
		REQUIRE( getWord(w, 0) == "abc" );
		REQUIRE( getWord(w, 1) == "def" );

		w = p.splitWords("abc\\Ndef");
		REQUIRE( w.size() == 2 );
		REQUIRE( getWord(w, 0) == "abc" );
		REQUIRE( getWord(w, 1) == "def" );

		w = p.splitWords("abc def ghi");
		REQUIRE( w.size() == 3 );
		REQUIRE( getWord(w, 0) == "abc" );
		REQUIRE( getWord(w, 1) == "def" );
		REQUIRE( getWord(w, 2) == "ghi" );

		w = p.splitWords("abc def\\Nghi");
		REQUIRE( w.size() == 3 );
		REQUIRE( getWord(w, 0) == "abc" );
		REQUIRE( getWord(w, 1) == "def" );
		REQUIRE( getWord(w, 2) == "ghi" );
	}

	SECTION("rSSA words split right-to-left")
	{
		SSAParser p(true, " ");
		SSAParser::Words w;

		w = p.splitWords("abc");
		REQUIRE( w.size() == 1 );
		REQUIRE( getWord(w, 0) == "cba" );

		w = p.splitWords("abc def");
		REQUIRE( w.size() == 2 );
		REQUIRE( getWord(w, 0) == "fed" );
		REQUIRE( getWord(w, 1) == "cba" );

		w = p.splitWords("abc\\Ndef");
		REQUIRE( w.size() == 2 );
		REQUIRE( getWord(w, 0) == "cba" );
		REQUIRE( getWord(w, 1) == "fed" );

		w = p.splitWords("abc\\Ndef ghi");
		REQUIRE( w.size() == 3 );
		REQUIRE( getWord(w, 0) == "cba" );
		REQUIRE( getWord(w, 1) == "ihg" );
		REQUIRE( getWord(w, 2) == "fed" );

		w = p.splitWords("abc def\\Nghi");
		REQUIRE( w.size() == 3 );
		REQUIRE( getWord(w, 0) == "fed" );
		REQUIRE( getWord(w, 1) == "cba" );
		REQUIRE( getWord(w, 2) == "ihg" );
	}
}
