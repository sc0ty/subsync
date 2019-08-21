#include "catch.hpp"
#include "text/ssa.h"


TEST_CASE("SSA Parser")
{
	SECTION("parsing SSA special sequences")
	{
		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ").splitWords(w, "abc{\\def}ghi");
			REQUIRE( len == 6 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "abc" );
			REQUIRE( w.back() == "ghi" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ").splitWords(w, "abc{{\\c}ghi");
			REQUIRE( len == 7 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "abc{" );
			REQUIRE( w.back() == "ghi" );
		}
	}

	SECTION("SSA words split left-to-right")
	{
		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ").splitWords(w, "abc");
			REQUIRE( len == 3 );
			REQUIRE( w.size() == 1 );
			REQUIRE( w.front() == "abc" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ").splitWords(w, "abc def");
			REQUIRE( len == 6 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "abc" );
			REQUIRE( w.back() == "def" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ").splitWords(w, "abc\\Ndef");
			REQUIRE( len == 6 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "abc" );
			REQUIRE( w.back() == "def" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ").splitWords(w, "abc def ghi");
			REQUIRE( len == 9 );
			REQUIRE( w.size() == 3 );
			REQUIRE( w.front() == "abc" );
			w.pop_front();
			REQUIRE( w.front() == "def" );
			REQUIRE( w.back() == "ghi" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ").splitWords(w, "abc def\\Nghi");
			REQUIRE( len == 9 );
			REQUIRE( w.size() == 3 );
			REQUIRE( w.front() == "abc" );
			w.pop_front();
			REQUIRE( w.front() == "def" );
			REQUIRE( w.back() == "ghi" );
		}
	}

	SECTION("SSA words split right-to-left")
	{
		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ", true).splitWords(w, "abc");
			REQUIRE( len == 3 );
			REQUIRE( w.size() == 1 );
			REQUIRE( w.front() == "cba" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ", true).splitWords(w, "abc def");
			REQUIRE( len == 6 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "fed" );
			REQUIRE( w.back() == "cba" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ", true).splitWords(w, "abc\\Ndef");
			REQUIRE( len == 6 );
			REQUIRE( w.size() == 2 );
			REQUIRE( w.front() == "cba" );
			w.pop_front();
			REQUIRE( w.back() == "fed" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ", true).splitWords(w, "abc\\Ndef ghi");
			REQUIRE( len == 9 );
			REQUIRE( w.size() == 3 );
			REQUIRE( w.front() == "cba" );
			w.pop_front();
			REQUIRE( w.front() == "ihg" );
			REQUIRE( w.back() == "fed" );
		}

		{
			SSAParser::WordList w;
			size_t len = SSAParser(" ", true).splitWords(w, "abc def\\Nghi");
			REQUIRE( len == 9 );
			REQUIRE( w.size() == 3 );
			REQUIRE( w.front() == "fed" );
			w.pop_front();
			REQUIRE( w.front() == "cba" );
			REQUIRE( w.back() == "ihg" );
		}
	}
}
