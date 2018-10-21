#include "correlator.h"
#include "math/point.h"
#include "math/line.h"
#include "text/utf8.h"
#include "text/translator.h"
#include "general/exception.h"
#include <sstream>
#include <iomanip>

using namespace std;


Correlator::Correlator(
		float windowSize,
		double minCorrelation,
		float maxDistance,
		unsigned minPointsNo,
		float minWordsSim) :
	m_running(false),
	m_wordsNo(0),
	m_lineFinder(5.0f, windowSize),
	m_windowSize(windowSize),
	m_minCorrelation(minCorrelation),
	m_maxDistance(maxDistance),
	m_minPointsNo(minPointsNo),
	m_minWordsSim(minWordsSim)
{
}

Correlator::~Correlator()
{
	terminate();
}

void Correlator::pushSubWord(const string &word, double time)
{
	m_queue.push(WordId::Sub, word, time);
}

void Correlator::pushRefWord(const string &word, double time)
{
	m_queue.push(WordId::Ref, word, time);
}

void Correlator::run()
{
	string word;
	double time;

	while (m_running)
	{
		WordId id = m_queue.pop(word, time);
		m_wordsNo++;

		bool newBestLine = false;

		if (id == WordId::Sub)
			newBestLine = addSubtitle(time, word);
		else if (id == WordId::Ref)
			newBestLine = addReference(time, word);

		if (newBestLine)
			correlate();
	}

	m_threadEndSem.wait();
}

void Correlator::terminate()
{
	m_running = false;

	if (m_thread.joinable())
	{
		m_queue.release();
		m_threadEndSem.post();
		m_thread.join();
	}

	m_threadEndSem.reset();
}

void Correlator::start()
{
	terminate();

	m_running = true;
	m_thread = thread(&Correlator::run, this);
}

void Correlator::stop()
{
	m_running = false;
}

bool Correlator::isRunning() const
{
	return m_running;
}

bool Correlator::isDone() const
{
	return m_queue.empty();
}

float Correlator::getProgress() const
{
	size_t added = m_wordsNo;
	size_t waiting = m_queue.size();
	size_t sum = added + waiting;
	return sum > 0 ? (float) added / (float) sum : 0.0;
}

void Correlator::connectStatsCallback(StatsCallback callback)
{
	m_statsCb = callback;
}

bool Correlator::addSubtitle(double time, const string &word)
{
	m_subs.insert(make_pair(time, word));

	auto first = m_refs.lower_bound(time - m_windowSize);
	auto last  = m_refs.upper_bound(time + m_windowSize);
	if (first == m_refs.end())
		first = m_refs.begin();

	bool newBestLine = false;

	for (auto it = first; it != last; ++it)
	{
		float sim = compareWords(word, it->second);
		if (sim >= m_minWordsSim)
		{
			newBestLine |= m_lineFinder.addPoint(time, it->first);
		}
	}

	return newBestLine;
}

bool Correlator::addReference(double time, const string &word)
{
	m_refs.insert(make_pair(time, word));

	auto first = m_subs.lower_bound(time - m_windowSize);
	auto last  = m_subs.upper_bound(time + m_windowSize);
	if (first == m_subs.end())
		first = m_subs.begin();

	bool newBestLine = false;

	for (auto it = first; it != last; ++it)
	{
		float sim = compareWords(word, it->second);
		if (sim >= m_minWordsSim)
		{
			newBestLine |= m_lineFinder.addPoint(it->first, time);
		}
	}

	return newBestLine;
}

void Correlator::correlate() const
{
	double cor;

	Line bestLine = m_lineFinder.getBestLine();
	const Points &points = m_lineFinder.getPoints();
	Points hits = bestLine.getPointsInLine(points, 5.0f);

	Line line(hits, NULL, NULL, &cor);
	float dist = line.findFurthestPoint(hits);

	while ((cor < m_minCorrelation || dist > m_maxDistance)
			&& (hits.size() > m_minPointsNo))
	{
		dist = line.removeFurthestPoint(hits);
		line = Line(hits, NULL, NULL, &cor);
	}

	if (m_statsCb)
	{
		CorrelationStats stats;

		stats.correlated =
			cor >= m_minCorrelation &&
			hits.size() >= m_minPointsNo &&
			dist <= m_maxDistance;

		stats.factor = cor;
		stats.points = hits.size();
		stats.maxDistance = dist;
		stats.formula = line;

		if (m_running)
			m_statsCb(stats);
	}
}

static Correlator::ElementsVector entrysToVector(Correlator::Entrys entrys)
{
	Correlator::ElementsVector res;
	res.reserve(entrys.size());

	for (auto &element : entrys)
	{
		auto p = pair<double, string>(element.first, element.second);
		res.push_back(p);
	}
	return res;
}

Correlator::ElementsVector Correlator::getSubs() const
{
	if (m_running)
		throw EXCEPTION("subtitle words cannot be obtained when the correlator is running")
			.module("Correlator");

	return entrysToVector(m_subs);
}

Correlator::ElementsVector Correlator::getRefs() const
{
	if (m_running)
		throw EXCEPTION("reference words cannot be obtained when the correlator is running")
			.module("Correlator");

	return entrysToVector(m_refs);
}


/*** CorrelationStats ***/

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

