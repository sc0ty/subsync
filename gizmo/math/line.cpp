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

	double sx  = 0.0f;	// sum of x
	double sy  = 0.0f;	// sum of y
	double sxy = 0.0f;	// sum of x*y
	double sx2 = 0.0f;	// sum of x^2
	double sy2 = 0.0f;	// sum of y^2

	for (auto &point : points)
	{
		double x = point.x;
		double y = point.y;
		sx += x;
		sy += y;
		sxy += x*y;
		sx2 += x*x;
		sy2 += y*y;
	}

	double n = points.size();

	double txy = n*sxy - sx*sy;
	double tx = n*sx2 - sx*sx;
	double ty = n*sy2 - sy*sy;

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
		double t3 = sy2 - a*sxy - b*sy;

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
	float t = b + a*point.x - point.y;
	return (t*t) / (a*a + 1.0f);
}

Points Line::getPointsInLine(const Points &pts) const
{
	Points res;
	for (auto point : pts)
	{
		if (point.y == a*point.x + b)
			res.insert(point);
	}
	return res;
}

Points Line::getPointsInLine(const Points &points, float maxDist) const
{
	Points res;
	float maxDistSqr = maxDist * maxDist;

	for (auto point : points)
	{
		if (getDistanceSqr(point) <= maxDistSqr)
			res.insert(point);
	}
	return res;
}

size_t Line::countPointsInLine(const Points &points) const
{
	size_t cnt = 0;
	for (auto point : points)
	{
		if (point.y == a*point.x + b)
			cnt++;
	}
	return cnt;
}

size_t Line::countPointsInLine(const Points &points, float maxDist) const
{
	size_t cnt = 0;
	float maxDistSqr = maxDist * maxDist;

	for (auto point : points)
	{
		if (getDistanceSqr(point) <= maxDistSqr)
			cnt++;
	}
	return cnt;
}

float Line::findFurthestPoint(Points &points) const
{
	float furthestDist = 0.0f;

	for (auto point=points.begin(); point!=points.end(); ++point)
	{
		float dist = getDistanceSqr(*point);
		if (dist > furthestDist)
			furthestDist = dist;
	}

	return sqrt(furthestDist);
}

float Line::removeFurthestPoint(Points &points) const
{
	Points::iterator furthestPoint;
	float furthestDist = 0.0f;

	for (auto point=points.begin(); point!=points.end(); ++point)
	{
		float dist = getDistanceSqr(*point);
		if (dist > furthestDist)
		{
			furthestPoint = point;
			furthestDist = dist;
		}
	}

	if (furthestDist > 0.0f)
		points.erase(furthestPoint);

	return sqrt(furthestDist);
}

string Line::toString() const
{
	stringstream ss;
	ss << fixed << setprecision(3) << a << "x" << showpos << b;
	return ss.str();
}

