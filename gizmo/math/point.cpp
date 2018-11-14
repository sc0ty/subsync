#include "point.h"
#include <cmath>


Point::Point() : x(0.0f), y(0.0f)
{}

Point::Point(const Point &p) : x(p.x), y(p.y)
{}

Point::Point(float x, float y) : x(x), y(y)
{}

bool Point::operator== (const Point &p) const
{
	return x == p.x && y == p.y;
}

bool Point::operator!= (const Point &p) const
{
	return x != p.x || y != p.y;
}

bool Point::operator< (const Point &p) const
{
	return x == p.x ? y < p.y : x < p.x;
}

float Point::getDistance(const Point &p) const
{
	return sqrt((p.x-x)*(p.x-x) + (p.y-y)*(p.y-y));
}
