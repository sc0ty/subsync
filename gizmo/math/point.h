#ifndef __POINT_H__
#define __POINT_H__

#include <set>


struct Point
{
	float x, y;

	Point();
	Point(const Point &p);
	Point(float x, float y);

	bool operator== (const Point &p) const;
	bool operator!= (const Point &p) const;
	bool operator< (const Point &p) const;

	float getDistance(const Point &p) const;
};

typedef std::set<Point> Points;

#endif
