#ifndef __LINEFINDER_H__
#define __LINEFINDER_H__

#include "line.h"
#include "point.h"
#include <cstddef>
#include <cmath>
#include <map>
#include <unordered_map>
#include <vector>


class LineFinder
{
	public:
		LineFinder(float maxError=5.0f, float maxDistance=HUGE_VALF);

		bool addPoint(const Point &point);
		bool addPoint(float x, float y);
		const Points &getPoints() const;

		const Line &getBestLine() const;
		size_t getAlignedPointsNo() const;

	private:
		Points m_points;
		Line m_bestLine;
		size_t m_bestPointsNo;

		std::unordered_map<int /*qx*/, std::map<int /*qy*/, std::vector<Point>>>
			m_quadrants;

		const float m_maxError;
		const float m_maxDistance;
		float m_minX, m_maxX;
};

#endif
