#include "catch.hpp"
#include "math/point.h"
#include "math/line.h"
#include "math/linefinder.h"
#include <sstream>
#include <iomanip>


namespace Catch
{
	template<> struct StringMaker<Point>
	{
		static std::string convert(Point const &p)
		{
			std::stringstream ss;
			ss << "Point(" << std::fixed << std::setprecision(3) << p.x << ", " << p.y << ")";
			return ss.str();
		}
	};

	template<> struct StringMaker<Line>
	{
		static std::string convert(Line const &line)
		{
			return std::string("Line(") + line.toString() + ")";
		}
	};

	template<> struct StringMaker<LineFinder>
	{
		static std::string convert(LineFinder const &lf)
		{
			std::stringstream ss;
			ss << "LineFinder(" << lf.getBestLine().toString()
				<< "; pts=" << lf.getAlignedPointsNo()
				<< "/" << lf.getPoints().size() << ")";
			return ss.str();
		}
	};
}
