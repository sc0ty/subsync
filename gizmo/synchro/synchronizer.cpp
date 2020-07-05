#include "synchronizer.h"
#include "text/translator.h"
#include "general/logger.h"
#include <sstream>
#include <iomanip>

using namespace std;


CorrelationStats::CorrelationStats() :
	correlated(false),
	factor(0.0),
	points(0),
	maxDistance(0.0f)
{
}

string CorrelationStats::toString(const char *prefix, const char *suffix) const
{
	stringstream ss;
	ss << prefix << fixed << setprecision(3)
		<< "correlated=" << std::boolalpha << correlated
		<< ", factor="   << 100.0 * factor << "%"
		<< ", points="   << points
		<< ", maxDist="  << maxDistance
		<< ", formula="  << formula.toString()
		<< suffix;
	return ss.str();
}


Synchronizer::Synchronizer(
		float windowSize,
		double minCorrelation,
		float maxDistance,
		unsigned minPointsNo,
		float minWordsSim) :
	m_lineFinder(5.0f, windowSize),
	m_windowSize(windowSize),
	m_minCorrelation(minCorrelation),
	m_maxDistanceSqr(maxDistance * maxDistance),
	m_minPointsNo(minPointsNo),
	m_minWordsSim(minWordsSim)
{
}

bool Synchronizer::addSubWord(const Word &sub)
{
	m_subs.insert(sub);

	auto first = m_refs.lower_bound(Word(sub.time - m_windowSize, 0.0f, 0.0f));
	auto last  = m_refs.upper_bound(Word(sub.time + m_windowSize, 0.0f, 1.0f));
	if (first == m_refs.end())
		first = m_refs.begin();

	bool newBestLine = false;

	for (auto ref = first; ref != last; ++ref)
	{
		float sim = compareWords(sub.text, ref->text);// * sub.score * ref->score;
		if (sim >= m_minWordsSim)
		{
			newBestLine |= m_lineFinder.addPoint(sub.time, ref->time);
		}
	}

	return newBestLine;
}

bool Synchronizer::addRefWord(const Word &ref)
{
	m_refs.insert(ref);

	auto first = m_subs.lower_bound(Word(ref.time - m_windowSize, 0.0f, 0.0f));
	auto last  = m_subs.upper_bound(Word(ref.time + m_windowSize, 0.0f, 1.0f));
	if (first == m_subs.end())
		first = m_subs.begin();

	bool newBestLine = false;

	for (auto sub = first; sub != last; ++sub)
	{
		float sim = compareWords(ref.text, sub->text);// * ref.score * sub->score;
		if (sim >= m_minWordsSim)
		{
			newBestLine |= m_lineFinder.addPoint(sub->time, ref.time);
		}
	}

	return newBestLine;
}

void Synchronizer::addSubtitle(double startTime, double endTime)
{
	(void) startTime;
	m_buckets.insert(endTime);
}

CorrelationStats Synchronizer::correlate() const
{
	const Line bestLine = m_lineFinder.getBestLine();
	const Points &points = m_lineFinder.getPoints();
	Points hits = bestLine.getPointsInLine(points, 10.0f*m_maxDistanceSqr);

	Line line;
	double factor = line.interpolate(hits);
	float distSqr = line.findFurthestPoint(hits);

	while ((factor < m_minCorrelation || distSqr > m_maxDistanceSqr)
			&& hits.size() > m_minPointsNo
			&& countBuckets(hits, m_minPointsNo + 1) > m_minPointsNo)
	{
		distSqr = line.removeFurthestPoint(hits);
		factor = line.interpolate(hits);
	}

	CorrelationStats stats;
	stats.factor = factor;
	stats.points = countBuckets(hits);
	stats.maxDistance = sqrt(distSqr);
	stats.formula = line;

	stats.correlated =
		factor >= m_minCorrelation &&
		distSqr <= m_maxDistanceSqr &&
		stats.points >= m_minPointsNo;

	return stats;
}

unsigned Synchronizer::countBuckets(const Points &pts, unsigned limit) const
{
	if (m_buckets.empty())
		return pts.size();

	set<float> has;

	for (const Point &pt : pts)
	{
		Buckets::const_iterator it = m_buckets.lower_bound(pt.x);
		if (it != m_buckets.end())
		{
			const bool inserted = has.insert(*it).second;
			if (inserted && has.size() >= limit)
				break;
		}
	}

	return has.size();
}

const Synchronizer::Entrys &Synchronizer::getSubs() const
{
	return m_subs;
}

const Synchronizer::Entrys &Synchronizer::getRefs() const
{
	return m_refs;
}

const Points &Synchronizer::getAllPoints() const
{
	return m_lineFinder.getPoints();
}

Points Synchronizer::getUsedPoints() const
{
	const CorrelationStats stats = correlate();
	const Line line(stats.formula.a, stats.formula.b);
	return line.getPointsInLine(m_lineFinder.getPoints(), m_maxDistanceSqr);
}
