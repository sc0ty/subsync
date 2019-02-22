#include "line.h"
#include <cmath>
#include <sstream>
#include <iomanip>

using namespace std;


Line::Line() : a(1.0f), b(0.0f)
{}

Line::Line(float a, float b) : a(a), b(b)
{}

Line::Line(const Point &p1, const Point &p2)
{
	a = (p1.y - p2.y) / (p1.x - p2.x);
	b = p1.y - a*p1.x;
}

Line::Line(const Points &points, double *da, double *db, double *cor)
{
	if (points.size() < 2)
	{
		a = 1.0f;
		b = 0.0f;
		if (da && db)
		{
			*da = HUGE_VALF;
			*db = HUGE_VALF;
		}
		if (cor)
			*cor = 0.0f;
	}

	double sx  = 0.0;	// sum of x
	double sy  = 0.0;	// sum of y
	double sxy = 0.0;	// sum of x*y
	double sx2 = 0.0;	// sum of x^2
	double sy2 = 0.0;	// sum of y^2

	for (const Point &point : points)
	{
		const double x = point.x;
		const double y = point.y;
		sx += x;
		sy += y;
		sxy += x*y;
		sx2 += x*x;
		sy2 += y*y;
	}

	const double n = points.size();

	const double txy = n*sxy - sx*sy;
	const double tx = n*sx2 - sx*sx;
	const double ty = n*sy2 - sy*sy;

	if ((tx == 0.0) || (ty == 0.0))
	{
		if (cor)
			*cor = 0.0;
		return;
	}

	a =  txy / tx;
	b = (sy - a*sx) / n;

	if (da && db)
	{
		const double t3 = sy2 - a*sxy - b*sy;

		*da = sqrt(n/(n-2) * t3/tx);
		*db = *da * sqrt(sx2/n);
	}

	if (cor)
		*cor = (txy * txy) / (tx * ty);
}

float Line::getDistance(const Point &point) const
{
	return sqrt(getDistanceSqr(point));
}

float Line::getDistanceSqr(const Point &point) const
{
	const float t = b + a*point.x - point.y;
	return (t*t) / (a*a + 1.0f);
}

Points Line::getPointsInLine(const Points &pts) const
{
	Points res;
	for (const Point &point : pts)
	{
		if (point.y == a*point.x + b)
			res.insert(point);
	}
	return res;
}

Points Line::getPointsInLine(const Points &points, float maxDistSqr) const
{
	Points res;

	for (const Point &point : points)
	{
		if (getDistanceSqr(point) <= maxDistSqr)
			res.insert(point);
	}
	return res;
}

size_t Line::countPointsInLine(const Points &points) const
{
	size_t cnt = 0;
	for (const Point &point : points)
	{
		if (point.y == a*point.x + b)
			cnt++;
	}
	return cnt;
}

size_t Line::countPointsInLine(const Points &points, float maxDistSqr) const
{
	size_t cnt = 0;

	for (const Point &point : points)
	{
		if (getDistanceSqr(point) <= maxDistSqr)
			cnt++;
	}
	return cnt;
}

float Line::findFurthestPoint(const Points &points) const
{
	float furthestDistSqr = 0.0f;

	for (const Point &point : points)
	{
		const float distSqr = getDistanceSqr(point);
		if (distSqr > furthestDistSqr)
			furthestDistSqr = distSqr;
	}

	return furthestDistSqr;
}

float Line::removeFurthestPoint(Points &points) const
{
	Points::iterator furthestPoint;
	float furthestDistSqr = 0.0f;

	for (auto point=points.begin(); point!=points.end(); ++point)
	{
		float distSqr = getDistanceSqr(*point);
		if (distSqr > furthestDistSqr)
		{
			furthestPoint = point;
			furthestDistSqr = distSqr;
		}
	}

	if (furthestDistSqr > 0.0f)
		points.erase(furthestPoint);

	return furthestDistSqr;
}

string Line::toString() const
{
	stringstream ss;
	ss << fixed << setprecision(3) << a << "x" << showpos << b;
	return ss.str();
}

