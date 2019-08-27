#include "catch.hpp"
#include "test/math.h"
#include "math/line.h"


TEST_CASE("Line")
{
	SECTION("calculating Y value from X")
	{
		REQUIRE( Line(1.0, 0.0).getY(0.0) == Approx(0.0) );
		REQUIRE( Line(1.0, 1.0).getY(0.0) == Approx(1.0) );
		REQUIRE( Line(0.0, 1.0).getY(0.0) == Approx(1.0) );
		REQUIRE( Line(0.5, 0.0).getY(1.0) == Approx(0.5) );
		REQUIRE( Line(0.5, 1.0).getY(1.0) == Approx(1.5) );
	}

	SECTION("calculating X value from Y")
	{
		REQUIRE( Line(1.0, 0.0).getX(0.0) == Approx(0.0) );
		REQUIRE( Line(1.0, 1.0).getX(1.0) == Approx(0.0) );
	}

	SECTION("distance between line and point")
	{
		REQUIRE( Line(1.0, 0.0).getDistance(Point(0.0, 0.0)) == Approx(0.0) );
		REQUIRE( Line(0.0, 0.0).getDistance(Point(0.0, 1.0)) == Approx(1.0) );
	}
}
