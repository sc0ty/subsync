#include "catch.hpp"
#include "test/math.h"
#include "math/line.h"

using namespace Catch::Matchers;


#define WA(x) WithinAbs((x), 0.0001)


TEST_CASE("Line")
{
	SECTION("calculating Y value from X")
	{
		REQUIRE_THAT( Line(1.0, 0.0).getY(0.0), WA(0.0) );
		REQUIRE_THAT( Line(1.0, 1.0).getY(0.0), WA(1.0) );
		REQUIRE_THAT( Line(0.0, 1.0).getY(0.0), WA(1.0) );
		REQUIRE_THAT( Line(0.5, 0.0).getY(1.0), WA(0.5) );
		REQUIRE_THAT( Line(0.5, 1.0).getY(1.0), WA(1.5) );
	}

	SECTION("calculating X value from Y")
	{
		REQUIRE_THAT( Line(1.0, 0.0).getX(0.0), WA(0.0) );
		REQUIRE_THAT( Line(1.0, 1.0).getX(1.0), WA(0.0) );
	}

	SECTION("distance between line and point")
	{
		REQUIRE_THAT( Line(1.0, 0.0).getDistance(Point(0.0, 0.0)), WA(0.0) );
		REQUIRE_THAT( Line(0.0, 0.0).getDistance(Point(0.0, 1.0)), WA(1.0) );
	}
}
