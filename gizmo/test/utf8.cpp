#include "catch.hpp"
#include "text/utf8.h"
#include <string>
#include <cstdarg>

using namespace std;



basic_string<uint32_t> mkbstr1(uint32_t cp)
{
	basic_string<uint32_t> res;
	res.push_back(cp);
	return res;
}

basic_string<uint32_t> mkbstr(size_t len, ...)
{
	basic_string<uint32_t> res;
	res.reserve(len);
	va_list vl;
	va_start(vl, len);
	for (size_t i = 0; i < len; i++)
		res.push_back(va_arg(vl, uint32_t));
	va_end(vl);
	return res;
}


TEST_CASE("UTF-8")
{
	SECTION("decode valid codepoints")
	{
		REQUIRE( Utf8::decode("a") == mkbstr1('a') );
		REQUIRE( Utf8::decode("\xc3\xb1") == mkbstr1(0xf1) );
		REQUIRE( Utf8::decode("\xe2\x82\xa1") == mkbstr1(0x20a1) );
		REQUIRE( Utf8::decode("\xf0\x90\x8c\xbc") == mkbstr1(0x1033c) );

		REQUIRE( Utf8::decode("\xc2\x80") == mkbstr1(0x80) );
		REQUIRE( Utf8::decode("\xe0\xa0\x80") == mkbstr1(0x800) );
		REQUIRE( Utf8::decode("\xf0\x90\x80\x80") == mkbstr1(0x10000) );

		REQUIRE( Utf8::decode("\x7f") == mkbstr1(0x7f) );
		REQUIRE( Utf8::decode("\xdf\xbf") == mkbstr1(0x7ff) );
		REQUIRE( Utf8::decode("\xef\xbf\xbf") == mkbstr1(0xffff) );

		REQUIRE( Utf8::decode("\xee\x80\x80") == mkbstr1(0xe000) );
		REQUIRE( Utf8::decode("\xef\xbf\xbd") == mkbstr1(0xfffd) );
		REQUIRE( Utf8::decode("\xf4\x90\x80\x80") == mkbstr1(0x110000) );
	}

	SECTION("encode valid codepoints")
	{
		REQUIRE( Utf8::encode('a') == "a" );
		REQUIRE( Utf8::encode(0xf1) == "\xc3\xb1" );
		REQUIRE( Utf8::encode(0x20a1) == "\xe2\x82\xa1" );
		REQUIRE( Utf8::encode(0x1033c) == "\xf0\x90\x8c\xbc" );

		REQUIRE( Utf8::encode(0x80) == "\xc2\x80" );
		REQUIRE( Utf8::encode(0x800) == "\xe0\xa0\x80" );
		REQUIRE( Utf8::encode(0x10000) == "\xf0\x90\x80\x80" );

		REQUIRE( Utf8::encode(0x7f) == "\x7f" );
		REQUIRE( Utf8::encode(0x7ff) == "\xdf\xbf" );
		REQUIRE( Utf8::encode(0xffff) == "\xef\xbf\xbf" );

		REQUIRE( Utf8::encode(0xe000) == "\xee\x80\x80" );
		REQUIRE( Utf8::encode(0xfffd) == "\xef\xbf\xbd" );
		REQUIRE( Utf8::encode(0x110000) == "\xf4\x90\x80\x80" );
	}

	SECTION("validation")
	{
		SECTION("validate legal sequence")
		{
			REQUIRE( true == Utf8::validate("a") );
			REQUIRE( true == Utf8::validate("\xc3\xb1") );
			REQUIRE( true == Utf8::validate("\xe2\x82\xa1") );
			REQUIRE( true == Utf8::validate("\xf0\x90\x8c\xbc") );

			REQUIRE( true == Utf8::validate("\xc2\x80") );
			REQUIRE( true == Utf8::validate("\xe0\xa0\x80") );
			REQUIRE( true == Utf8::validate("\xf0\x90\x80\x80") );

			REQUIRE( true == Utf8::validate("\x7f") );
			REQUIRE( true == Utf8::validate("\xdf\xbf") );
			REQUIRE( true == Utf8::validate("\xef\xbf\xbf") );

			REQUIRE( true == Utf8::validate("\xee\x80\x80") );
			REQUIRE( true == Utf8::validate("\xef\xbf\xbd") );
			REQUIRE( true == Utf8::validate("\xf4\x90\x80\x80") );
		}

		SECTION("validate illegal sequence")
		{
			REQUIRE( false == Utf8::validate("\xc3\x28") );
			REQUIRE( false == Utf8::validate("\xa0\xa1") );
			REQUIRE( false == Utf8::validate("\xe2\x28\xa1") );
			REQUIRE( false == Utf8::validate("\xe2\x82\x28") );
			REQUIRE( false == Utf8::validate("\xf0\x28\x8c\xbc") );
			REQUIRE( false == Utf8::validate("\xf0\x90\x28\xbc") );
			REQUIRE( false == Utf8::validate("\xf0\x28\x8c\x28") );
			REQUIRE( false == Utf8::validate("\xfe") );
			REQUIRE( false == Utf8::validate("\xff") );
			REQUIRE( false == Utf8::validate("\xfe\xfe\xff\xff") );
			REQUIRE( false == Utf8::validate("\xc0") );
			REQUIRE( false == Utf8::validate("\xc1") );
		}

		SECTION("validate too long sequences")
		{
			REQUIRE( false == Utf8::validate("\xf8\xa1\xa1\xa1\xa1") );
			REQUIRE( false == Utf8::validate("\xfc\xa1\xa1\xa1\xa1\xa1") );
		}

		SECTION("validate over-long sequences")
		{
			REQUIRE( false == Utf8::validate("\xc0\xaf") );
			REQUIRE( false == Utf8::validate("\xe0\x80\xaf") );
			REQUIRE( false == Utf8::validate("\xf0\x80\x80\xaf") );
			REQUIRE( false == Utf8::validate("\xf8\x80\x80\x80\xaf") );
			REQUIRE( false == Utf8::validate("\xfc\x80\x80\x80\x80\xaf") );

			REQUIRE( false == Utf8::validate("\xc1\xbf") );
			REQUIRE( false == Utf8::validate("\xe0\x9f\xbf") );
			REQUIRE( false == Utf8::validate("\xf0\x8f\xbf\xbf") );
			REQUIRE( false == Utf8::validate("\xf8\x87\xbf\xbf\xbf") );
			REQUIRE( false == Utf8::validate("\xfc\x83\xbf\xbf\xbf\xbf") );

			REQUIRE( false == Utf8::validate("\xc0\x80") );
			REQUIRE( false == Utf8::validate("\xe0\x80\x80") );
			REQUIRE( false == Utf8::validate("\xf0\x80\x80\x80") );
			REQUIRE( false == Utf8::validate("\xf8\x80\x80\x80\x80") );
			REQUIRE( false == Utf8::validate("\xfc\x80\x80\x80\x80\x80") );
		}
	}

	SECTION("escape")
	{
		SECTION("escape valid sequences")
		{
			REQUIRE( Utf8::escape("a") == "a" );
			REQUIRE( Utf8::escape("\xc3\xb1") == "\xc3\xb1" );
			REQUIRE( Utf8::escape("\xe2\x82\xa1") == "\xe2\x82\xa1" );
			REQUIRE( Utf8::escape("\xf0\x90\x8c\xbc") == "\xf0\x90\x8c\xbc" );

			REQUIRE( Utf8::escape("\xc2\x80") == "\xc2\x80" );
			REQUIRE( Utf8::escape("\xe0\xa0\x80") == "\xe0\xa0\x80" );
			REQUIRE( Utf8::escape("\xf0\x90\x80\x80") == "\xf0\x90\x80\x80" );

			REQUIRE( Utf8::escape("\x7f") == "\x7f" );
			REQUIRE( Utf8::escape("\xdf\xbf") == "\xdf\xbf" );
			REQUIRE( Utf8::escape("\xef\xbf\xbf") == "\xef\xbf\xbf" );

			REQUIRE( Utf8::escape("\xee\x80\x80") == "\xee\x80\x80" );
			REQUIRE( Utf8::escape("\xef\xbf\xbd") == "\xef\xbf\xbd" );
			REQUIRE( Utf8::escape("\xf4\x90\x80\x80") == "\xf4\x90\x80\x80" );
		}

		SECTION("escape invalid sequences")
		{
			REQUIRE( Utf8::validate( Utf8::escape("\xc3\x28") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xa0\xa1") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xe2\x28\xa1") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xe2\x82\x28") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf0\x28\x8c\xbc") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf0\x90\x28\xbc") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf0\x28\x8c\x28") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xfe") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xff") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xfe\xfe\xff\xff") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xc0") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xc1") ) );
		}

		SECTION("escape too long sequences")
		{
			REQUIRE( Utf8::validate( Utf8::escape("\xf8\xa1\xa1\xa1\xa1") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xfc\xa1\xa1\xa1\xa1\xa1") ) );
		}

		SECTION("escape over-long sequences")
		{
			REQUIRE( Utf8::validate( Utf8::escape("\xc0\xaf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xe0\x80\xaf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf0\x80\x80\xaf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf8\x80\x80\x80\xaf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xfc\x80\x80\x80\x80\xaf") ) );

			REQUIRE( Utf8::validate( Utf8::escape("\xc1\xbf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xe0\x9f\xbf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf0\x8f\xbf\xbf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf8\x87\xbf\xbf\xbf") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xfc\x83\xbf\xbf\xbf\xbf") ) );

			REQUIRE( Utf8::validate( Utf8::escape("\xc0\x80") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xe0\x80\x80") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf0\x80\x80\x80") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xf8\x80\x80\x80\x80") ) );
			REQUIRE( Utf8::validate( Utf8::escape("\xfc\x80\x80\x80\x80\x80") ) );
		}
	}

	SECTION("size")
	{
		SECTION("size of simple strings")
		{
			REQUIRE( Utf8::size("") == 0 );
			REQUIRE( Utf8::size("a") == 1 );
			REQUIRE( Utf8::size("ab") == 2 );
			REQUIRE( Utf8::size("abc") == 3 );
		}

		SECTION("size of mulit-byte strings")
		{
			REQUIRE( Utf8::size("\xc3\xb1") == 1 );
			REQUIRE( Utf8::size("\xe2\x82\xa1") == 1 );
			REQUIRE( Utf8::size("\xf0\x90\x8c\xbc") == 1 );
			REQUIRE( Utf8::size("\xc2\x80") == 1 );
			REQUIRE( Utf8::size("\xe0\xa0\x80") == 1 );
			REQUIRE( Utf8::size("\xf0\x90\x80\x80") == 1 );
			REQUIRE( Utf8::size("\x7f") == 1 );
			REQUIRE( Utf8::size("\xdf\xbf") == 1 );
			REQUIRE( Utf8::size("\xef\xbf\xbf") == 1 );
			REQUIRE( Utf8::size("\xee\x80\x80") == 1 );
			REQUIRE( Utf8::size("\xef\xbf\xbd") == 1 );
			REQUIRE( Utf8::size("\xf4\x90\x80\x80") == 1 );

			REQUIRE( Utf8::size("\xc3\xb1" "\xe2\x82\xa1") == 2 );
			REQUIRE( Utf8::size("\xf0\x90\x8c\xbc" "\xc3\xb1" "\xe2\x82\xa1") == 3 );
			REQUIRE( Utf8::size("\xe0\xa0\x80" "\xc2\x80") == 2 );
			REQUIRE( Utf8::size("\xf0\x90\x80\x80" "\xe0\xa0\x80" "\xc2\x80") == 3 );
			REQUIRE( Utf8::size("\x7f" "\xef\xbf\xbf") == 2 );
			REQUIRE( Utf8::size("\x7f" "\xdf\xbf") == 2 );
			REQUIRE( Utf8::size("\xee\x80\x80" "\xf4\x90\x80\x80") == 2 );
			REQUIRE( Utf8::size("\xef\xbf\xbd" "\xee\x80\x80" "\xf4\x90\x80\x80") == 3);
			REQUIRE( Utf8::size("\xc3\xb1" "\xe2\x82\xa1") == 2 );
			REQUIRE( Utf8::size(
					"\xc3\xb1" "\xe2\x82\xa1" "\xf0\x90\x8c\xbc" "\xc3\xb1" "\xe2\x82\xa1" "\xe0\xa0\x80"
					"\xc2\x80" "\xf0\x90\x80\x80" "\xe0\xa0\x80" "\xc2\x80" "\x7f" "\xef\xbf\xbf" "\x7f"
					"\xdf\xbf" "\xee\x80\x80" "\xf4\x90\x80\x80" "\xef\xbf\xbd" "\xee\x80\x80"
					"\xf4\x90\x80\x80" ) == 19 );
		}

		SECTION("size of invalid strings")
		{
			REQUIRE( Utf8::size( "\xa1") <= 1 );
			REQUIRE( Utf8::size( "\xf8") <= 1 );
			REQUIRE( Utf8::size( "\xf8\xa1") <= 1 );
			REQUIRE( Utf8::size( "\xf8\xa1\xa1") <= 1 );
			REQUIRE( Utf8::size( "\xf8\xa1\xa1\xa1\xa1") <= 2 );
			REQUIRE( Utf8::size( "\xfc\xa1\xa1\xa1\xa1\xa1") <= 2 );
		}
	}

	SECTION("reverse")
	{
		SECTION("reverse simple strings")
		{
			REQUIRE( Utf8::reverse("") == "" );
			REQUIRE( Utf8::reverse("a") == "a" );
			REQUIRE( Utf8::reverse("ab") == "ba" );
			REQUIRE( Utf8::reverse("abc") == "cba" );
		}

		SECTION("reverse multi-byte codepoints")
		{
			REQUIRE( Utf8::reverse("\xc3\xb1") == "\xc3\xb1" );
			REQUIRE( Utf8::reverse("\xe2\x82\xa1") == "\xe2\x82\xa1" );
			REQUIRE( Utf8::reverse("\xf0\x90\x8c\xbc") == "\xf0\x90\x8c\xbc" );

			REQUIRE( Utf8::reverse("\xc2\x80") == "\xc2\x80" );
			REQUIRE( Utf8::reverse("\xe0\xa0\x80") == "\xe0\xa0\x80" );
			REQUIRE( Utf8::reverse("\xf0\x90\x80\x80") == "\xf0\x90\x80\x80" );

			REQUIRE( Utf8::reverse("\x7f") == "\x7f" );
			REQUIRE( Utf8::reverse("\xdf\xbf") == "\xdf\xbf" );
			REQUIRE( Utf8::reverse("\xef\xbf\xbf") == "\xef\xbf\xbf" );

			REQUIRE( Utf8::reverse("\xee\x80\x80") == "\xee\x80\x80" );
			REQUIRE( Utf8::reverse("\xef\xbf\xbd") == "\xef\xbf\xbd" );
			REQUIRE( Utf8::reverse("\xf4\x90\x80\x80") == "\xf4\x90\x80\x80" );
		}

		SECTION("reverse multi-byte strings")
		{
			REQUIRE( Utf8::reverse("\xc3\xb1" "\xe2\x82\xa1") == "\xe2\x82\xa1" "\xc3\xb1" );
			REQUIRE( Utf8::reverse("\xf0\x90\x8c\xbc" "\xc3\xb1" "\xe2\x82\xa1")
					== "\xe2\x82\xa1" "\xc3\xb1" "\xf0\x90\x8c\xbc" );

			REQUIRE( Utf8::reverse("\xe0\xa0\x80" "\xc2\x80") == "\xc2\x80" "\xe0\xa0\x80" );
			REQUIRE( Utf8::reverse("\xf0\x90\x80\x80" "\xe0\xa0\x80" "\xc2\x80")
					== "\xc2\x80" "\xe0\xa0\x80" "\xf0\x90\x80\x80" );

			REQUIRE( Utf8::reverse("\x7f" "\xef\xbf\xbf") == "\xef\xbf\xbf" "\x7f" );
			REQUIRE( Utf8::reverse("\x7f" "\xdf\xbf") == "\xdf\xbf" "\x7f" );

			REQUIRE( Utf8::reverse("\xee\x80\x80" "\xf4\x90\x80\x80") == "\xf4\x90\x80\x80" "\xee\x80\x80" );
			REQUIRE( Utf8::reverse("\xef\xbf\xbd" "\xee\x80\x80" "\xf4\x90\x80\x80")
					== "\xf4\x90\x80\x80" "\xee\x80\x80" "\xef\xbf\xbd" );

			REQUIRE( Utf8::reverse("\xc3\xb1" "\xe2\x82\xa1") == "\xe2\x82\xa1" "\xc3\xb1" );

			REQUIRE( Utf8::reverse(
					"\xc3\xb1" "\xe2\x82\xa1" "\xf0\x90\x8c\xbc" "\xc3\xb1" "\xe2\x82\xa1" "\xe0\xa0\x80"
					"\xc2\x80" "\xf0\x90\x80\x80" "\xe0\xa0\x80" "\xc2\x80" "\x7f" "\xef\xbf\xbf" "\x7f"
					"\xdf\xbf" "\xee\x80\x80" "\xf4\x90\x80\x80" "\xef\xbf\xbd" "\xee\x80\x80"
					"\xf4\x90\x80\x80" )
					==
					"\xf4\x90\x80\x80" "\xee\x80\x80" "\xef\xbf\xbd" "\xf4\x90\x80\x80" "\xee\x80\x80"
					"\xdf\xbf" "\x7f" "\xef\xbf\xbf" "\x7f" "\xc2\x80" "\xe0\xa0\x80" "\xf0\x90\x80\x80"
					"\xc2\x80" "\xe0\xa0\x80" "\xe2\x82\xa1" "\xc3\xb1" "\xf0\x90\x8c\xbc" "\xe2\x82\xa1"
					"\xc3\xb1" );
		}
	}
}
