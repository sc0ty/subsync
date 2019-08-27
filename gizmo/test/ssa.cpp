#include "catch.hpp"
#include "text/ssa.h"


TEST_CASE("SSA Parser")
{
	SSAParser p = SSAParser(" ");
	SSAParser::WordList w;

	SECTION("skipping braces with slash")
	{
		size_t len = p.splitWords(w, "abc{\\def}ghi{{\\c}jkl");
		REQUIRE( len == 10 );
		REQUIRE( w.size() == 3 );
		REQUIRE( w.front() == "abc" );
		w.pop_front();
		REQUIRE( w.front() == "ghi{" );
		REQUIRE( w.back() == "jkl" );
	}

	SECTION("parse single word")
	{
		size_t len = p.splitWords(w, "abc");
		REQUIRE( len == 3 );
		REQUIRE( w.size() == 1 );
		REQUIRE( w.front() == "abc" );
	}

	SECTION("parse two words")
	{
		size_t len = p.splitWords(w, "abc def");
		REQUIRE( len == 6 );
		REQUIRE( w.size() == 2 );
		REQUIRE( w.front() == "abc" );
		REQUIRE( w.back() == "def" );
	}

	SECTION("parse three words")
	{
		size_t len = p.splitWords(w, "abc def ghi");
		REQUIRE( len == 9 );
		REQUIRE( w.size() == 3 );
		REQUIRE( w.front() == "abc" );
		w.pop_front();
		REQUIRE( w.front() == "def" );
		REQUIRE( w.back() == "ghi" );
	}

	SECTION("parse two lines")
	{
		size_t len = p.splitWords(w, "abc\\Ndef");
		REQUIRE( len == 6 );
		REQUIRE( w.size() == 2 );
		REQUIRE( w.front() == "abc" );
		REQUIRE( w.back() == "def" );
	}

	SECTION("parse multiple words in two lines")
	{
		size_t len = p.splitWords(w, "abc def\\Nghi");
		REQUIRE( len == 9 );
		REQUIRE( w.size() == 3 );
		REQUIRE( w.front() == "abc" );
		w.pop_front();
		REQUIRE( w.front() == "def" );
		REQUIRE( w.back() == "ghi" );
	}

	SECTION("right-to-left mode")
	{
		p.setRightToLeft(true);

		SECTION("parse single word")
		{
			size_t len = p.splitWords(w, "abc");
			REQUIRE( len == 3 );
			REQUIRE( w.size() == 1 );
			REQUIRE( w.front() == "cba" );
		}

		SECTION("parse two words")
		{
			size_t len = p.splitWords(w, "abc def");
			REQUIRE( len == 6 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "fed" );
			REQUIRE( w.back() == "cba" );
		}

		SECTION("parse two lines")
		{
			size_t len = p.splitWords(w, "abc\\Ndef");
			REQUIRE( len == 6 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "cba" );
			w.pop_front();
			REQUIRE( w.back() == "fed" );
		}

		SECTION("parse multiple words in two lines")
		{
			size_t len = p.splitWords(w, "abc def\\Nghi");
			REQUIRE( len == 9 );
			REQUIRE( w.size() == 3 );
			REQUIRE( w.front() == "fed" );
			w.pop_front();
			REQUIRE( w.front() == "cba" );
			REQUIRE( w.back() == "ihg" );
		}

	}
}
