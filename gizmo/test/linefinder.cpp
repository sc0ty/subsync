#include "catch.hpp"
#include "test/math.h"
#include "math/linefinder.h"
#include <cmath>
#include <sstream>

using namespace std;
using namespace Catch::Matchers;


#define EPSILON 0.0001


static LineFinder mkLineFinder(const Points &pts, float ymul=1.f, float yadd=0.f)
{
	LineFinder lf;
	for (const Point &p : pts)
		lf.addPoint(p.x, p.y*ymul+yadd);
	return lf;
}


class IsBestLine : public Catch::MatcherBase<LineFinder>
{
	private:
		float a, b;
		size_t no;

	public:
		IsBestLine(float a, float b, size_t no)
			: a(a), b(b), no(no) { }

		IsBestLine(float a, float b, const Points &pts)
			: a(a), b(b), no(pts.size()) { }

		virtual bool match(const LineFinder &lf) const override
		{
			const Line line = lf.getBestLine();
			return abs(line.a - a) <= EPSILON && abs(line.b - b) <= EPSILON
				&& lf.getAlignedPointsNo() == no;
		}

		virtual string describe() const override
		{
			stringstream ss;
			ss << "finds line " << Line(a, b).toString()
				<< " pts: " << no;
			return ss.str();
		}
};


TEST_CASE("LineFinder")
{
	Points pts1;
	pts1.insert( Point(3.0, 3.0) );
	pts1.insert( Point(4.0, 4.0) );
	pts1.insert( Point(7.0, 7.0) );
	pts1.insert( Point(15.5, 15.5) );
	pts1.insert( Point(20.0, 20.0) );
	pts1.insert( Point(24.0, 24.0) );
	pts1.insert( Point(60.0, 60.0) );
	pts1.insert( Point(100.0, 100.0) );

	Points pts2, pts3, pts4, pts5, pts6;
	for (float i = 10.0; i < 1000; i+=10.0)
	{
		pts2.insert( Point(i,     i    ) );
		pts3.insert( Point(i+0.1, i+0.1) );
		pts4.insert( Point(i-0.1, i-0.1) );
		pts5.insert( Point(i+0.1, i+0.1) );
		pts5.insert( Point(i-0.1, i-0.1) );
		pts6.insert( Point(i,     i    ) );
		pts6.insert( Point(i+0.1, i+0.1) );
		pts6.insert( Point(i-0.1, i-0.1) );
	}

	Points err2;
	err2.insert( Point(100.0, 200.0) );
	err2.insert( Point(200.0, 100.0) );

	Points pts2e2 = pts2, pts3e2 = pts3, pts4e2 = pts4, pts5e2 = pts5, pts6e2 = pts6;
	for (int i = 0; i < 5; i++)
	{
		pts2e2.insert(err2.begin(), err2.end());
		pts3e2.insert(err2.begin(), err2.end());
		pts4e2.insert(err2.begin(), err2.end());
		pts5e2.insert(err2.begin(), err2.end());
		pts6e2.insert(err2.begin(), err2.end());
	}

	SECTION("finding exact line")
	{
		REQUIRE( mkLineFinder(pts2).getPoints() == pts2 );
		REQUIRE( mkLineFinder(pts3).getPoints() == pts3 );
		REQUIRE( mkLineFinder(pts4).getPoints() == pts4 );
		REQUIRE( mkLineFinder(pts5).getPoints() == pts5 );
		REQUIRE( mkLineFinder(pts6).getPoints() == pts6 );

		REQUIRE_THAT( mkLineFinder(pts1), IsBestLine(1.0, 0.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2), IsBestLine(1.0, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3), IsBestLine(1.0, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4), IsBestLine(1.0, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5), IsBestLine(1.0, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6), IsBestLine(1.0, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 2.0), IsBestLine(2.0, 0.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 2.0), IsBestLine(2.0, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 2.0), IsBestLine(2.0, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 2.0), IsBestLine(2.0, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 2.0), IsBestLine(2.0, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 2.0), IsBestLine(2.0, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 0.5), IsBestLine(0.5, 0.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 0.5), IsBestLine(0.5, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 0.5), IsBestLine(0.5, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 0.5), IsBestLine(0.5, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 0.5), IsBestLine(0.5, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 0.5), IsBestLine(0.5, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 9.0), IsBestLine(9.0, 0.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 9.0), IsBestLine(9.0, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 9.0), IsBestLine(9.0, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 9.0), IsBestLine(9.0, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 9.0), IsBestLine(9.0, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 9.0), IsBestLine(9.0, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 0.2), IsBestLine(0.2, 0.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 0.2), IsBestLine(0.2, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 0.2), IsBestLine(0.2, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 0.2), IsBestLine(0.2, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 0.2), IsBestLine(0.2, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 0.2), IsBestLine(0.2, 0.0, pts6) );


		REQUIRE_THAT( mkLineFinder(pts1, 1.0, 10.0), IsBestLine(1.0, 10.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 1.0, 10.0), IsBestLine(1.0, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 1.0, 10.0), IsBestLine(1.0, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 1.0, 10.0), IsBestLine(1.0, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 1.0, 10.0), IsBestLine(1.0, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 1.0, 10.0), IsBestLine(1.0, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 2.0, 10.0), IsBestLine(2.0, 10.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 2.0, 10.0), IsBestLine(2.0, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 2.0, 10.0), IsBestLine(2.0, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 2.0, 10.0), IsBestLine(2.0, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 2.0, 10.0), IsBestLine(2.0, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 2.0, 10.0), IsBestLine(2.0, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 0.5, 10.0), IsBestLine(0.5, 10.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 0.5, 10.0), IsBestLine(0.5, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 0.5, 10.0), IsBestLine(0.5, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 0.5, 10.0), IsBestLine(0.5, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 0.5, 10.0), IsBestLine(0.5, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 0.5, 10.0), IsBestLine(0.5, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 9.0, 10.0), IsBestLine(9.0, 10.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 9.0, 10.0), IsBestLine(9.0, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 9.0, 10.0), IsBestLine(9.0, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 9.0, 10.0), IsBestLine(9.0, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 9.0, 10.0), IsBestLine(9.0, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 9.0, 10.0), IsBestLine(9.0, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 0.2, 10.0), IsBestLine(0.2, 10.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 0.2, 10.0), IsBestLine(0.2, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 0.2, 10.0), IsBestLine(0.2, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 0.2, 10.0), IsBestLine(0.2, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 0.2, 10.0), IsBestLine(0.2, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 0.2, 10.0), IsBestLine(0.2, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 1.0, 60.0), IsBestLine(1.0, 60.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 1.0, 60.0), IsBestLine(1.0, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 1.0, 60.0), IsBestLine(1.0, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 1.0, 60.0), IsBestLine(1.0, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 1.0, 60.0), IsBestLine(1.0, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 1.0, 60.0), IsBestLine(1.0, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 2.0, 60.0), IsBestLine(2.0, 60.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 2.0, 60.0), IsBestLine(2.0, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 2.0, 60.0), IsBestLine(2.0, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 2.0, 60.0), IsBestLine(2.0, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 2.0, 60.0), IsBestLine(2.0, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 2.0, 60.0), IsBestLine(2.0, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 0.5, 60.0), IsBestLine(0.5, 60.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 0.5, 60.0), IsBestLine(0.5, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 0.5, 60.0), IsBestLine(0.5, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 0.5, 60.0), IsBestLine(0.5, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 0.5, 60.0), IsBestLine(0.5, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 0.5, 60.0), IsBestLine(0.5, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 9.0, 60.0), IsBestLine(9.0, 60.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 9.0, 60.0), IsBestLine(9.0, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 9.0, 60.0), IsBestLine(9.0, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 9.0, 60.0), IsBestLine(9.0, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 9.0, 60.0), IsBestLine(9.0, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 9.0, 60.0), IsBestLine(9.0, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts1, 0.2, 60.0), IsBestLine(0.2, 60.0, pts1) );
		REQUIRE_THAT( mkLineFinder(pts2, 0.2, 60.0), IsBestLine(0.2, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3, 0.2, 60.0), IsBestLine(0.2, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4, 0.2, 60.0), IsBestLine(0.2, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5, 0.2, 60.0), IsBestLine(0.2, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6, 0.2, 60.0), IsBestLine(0.2, 60.0, pts6) );
	}

	SECTION("finding line with invalid point")
	{
		REQUIRE_THAT( mkLineFinder(pts2e2), IsBestLine(1.0, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2), IsBestLine(1.0, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2), IsBestLine(1.0, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2), IsBestLine(1.0, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2), IsBestLine(1.0, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 2.0), IsBestLine(2.0, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 2.0), IsBestLine(2.0, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 2.0), IsBestLine(2.0, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 2.0), IsBestLine(2.0, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 2.0), IsBestLine(2.0, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 0.5), IsBestLine(0.5, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 0.5), IsBestLine(0.5, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 0.5), IsBestLine(0.5, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 0.5), IsBestLine(0.5, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 0.5), IsBestLine(0.5, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 9.0), IsBestLine(9.0, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 9.0), IsBestLine(9.0, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 9.0), IsBestLine(9.0, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 9.0), IsBestLine(9.0, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 9.0), IsBestLine(9.0, 0.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 0.2), IsBestLine(0.2, 0.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 0.2), IsBestLine(0.2, 0.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 0.2), IsBestLine(0.2, 0.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 0.2), IsBestLine(0.2, 0.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 0.2), IsBestLine(0.2, 0.0, pts6) );


		REQUIRE_THAT( mkLineFinder(pts2e2, 1.0, 10.0), IsBestLine(1.0, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 1.0, 10.0), IsBestLine(1.0, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 1.0, 10.0), IsBestLine(1.0, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 1.0, 10.0), IsBestLine(1.0, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 1.0, 10.0), IsBestLine(1.0, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 2.0, 10.0), IsBestLine(2.0, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 2.0, 10.0), IsBestLine(2.0, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 2.0, 10.0), IsBestLine(2.0, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 2.0, 10.0), IsBestLine(2.0, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 2.0, 10.0), IsBestLine(2.0, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 0.5, 10.0), IsBestLine(0.5, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 0.5, 10.0), IsBestLine(0.5, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 0.5, 10.0), IsBestLine(0.5, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 0.5, 10.0), IsBestLine(0.5, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 0.5, 10.0), IsBestLine(0.5, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 9.0, 10.0), IsBestLine(9.0, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 9.0, 10.0), IsBestLine(9.0, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 9.0, 10.0), IsBestLine(9.0, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 9.0, 10.0), IsBestLine(9.0, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 9.0, 10.0), IsBestLine(9.0, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 0.2, 10.0), IsBestLine(0.2, 10.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 0.2, 10.0), IsBestLine(0.2, 10.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 0.2, 10.0), IsBestLine(0.2, 10.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 0.2, 10.0), IsBestLine(0.2, 10.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 0.2, 10.0), IsBestLine(0.2, 10.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 1.0, 60.0), IsBestLine(1.0, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 1.0, 60.0), IsBestLine(1.0, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 1.0, 60.0), IsBestLine(1.0, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 1.0, 60.0), IsBestLine(1.0, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 1.0, 60.0), IsBestLine(1.0, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 2.0, 60.0), IsBestLine(2.0, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 2.0, 60.0), IsBestLine(2.0, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 2.0, 60.0), IsBestLine(2.0, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 2.0, 60.0), IsBestLine(2.0, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 2.0, 60.0), IsBestLine(2.0, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 0.5, 60.0), IsBestLine(0.5, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 0.5, 60.0), IsBestLine(0.5, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 0.5, 60.0), IsBestLine(0.5, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 0.5, 60.0), IsBestLine(0.5, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 0.5, 60.0), IsBestLine(0.5, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 9.0, 60.0), IsBestLine(9.0, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 9.0, 60.0), IsBestLine(9.0, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 9.0, 60.0), IsBestLine(9.0, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 9.0, 60.0), IsBestLine(9.0, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 9.0, 60.0), IsBestLine(9.0, 60.0, pts6) );

		REQUIRE_THAT( mkLineFinder(pts2e2, 0.2, 60.0), IsBestLine(0.2, 60.0, pts2) );
		REQUIRE_THAT( mkLineFinder(pts3e2, 0.2, 60.0), IsBestLine(0.2, 60.0, pts3) );
		REQUIRE_THAT( mkLineFinder(pts4e2, 0.2, 60.0), IsBestLine(0.2, 60.0, pts4) );
		REQUIRE_THAT( mkLineFinder(pts5e2, 0.2, 60.0), IsBestLine(0.2, 60.0, pts5) );
		REQUIRE_THAT( mkLineFinder(pts6e2, 0.2, 60.0), IsBestLine(0.2, 60.0, pts6) );
	}
}
