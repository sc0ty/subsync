#include "correlator.h"
#include "math/point.h"
#include "math/line.h"
#include "text/translator.h"
#include "general/thread.h"
#include "general/scope.h"
#include "general/exception.h"
#include <pybind11/pybind11.h>
#include <sstream>
#include <iomanip>
#include <cmath>

using namespace std;
namespace py = pybind11;


Correlator::Correlator(
		float windowSize,
		double minCorrelation,
		float maxDistance,
		unsigned minPointsNo,
		float minWordsSim) :
	m_state(State::idle),
	m_wordsNo(0),
	m_lineFinder(5.0f, windowSize),
	m_windowSize(windowSize),
	m_minCorrelation(minCorrelation),
	m_maxDistanceSqr(maxDistance * maxDistance),
	m_minPointsNo(minPointsNo),
	m_minWordsSim(minWordsSim)
{
}

Correlator::~Correlator()
{
	terminate();
}

void Correlator::pushSubWord(const Word &word)
{
	m_queue.push(WordId::SUB, word);
}

void Correlator::pushRefWord(const Word &word)
{
	m_queue.push(WordId::REF, word);
}

void Correlator::run(const string threadName)
{
	ScopeExit done([this](){ m_state = State::idle; });

	if (!threadName.empty())
		renameThread(threadName);

	Word word;

	while (m_state == State::running || m_state == State::finishing)
	{
		WordId id = m_queue.pop(word);
		if (id == WordId::NONE)
		{
			if (m_state == State::running)
				continue;
			else
				break;
		}

		m_wordsNo++;
		bool newBestLine = false;

		if (id == WordId::SUB)
			newBestLine = addSubtitle(word);
		else if (id == WordId::REF)
			newBestLine = addReference(word);

		if (newBestLine)
			correlate();
	}
}

void Correlator::terminate()
{
	if (m_state != State::idle)
		m_state = State::stopping;

	if (m_thread.joinable())
	{
		m_queue.release();

		py::gil_scoped_release release;
		m_thread.join();
	}

	m_state = State::idle;
}

void Correlator::start(const std::string &threadName)
{
	terminate();

	m_state = State::running;
	m_thread = thread(&Correlator::run, this, threadName);
}

void Correlator::stop(bool force)
{
	if (force && m_state != State::idle)
		m_state = State::stopping;
	if (!force && m_state == State::running)
		m_state = State::finishing;
	m_queue.release();
}

bool Correlator::isRunning() const
{
	return m_state != State::idle;
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

bool Correlator::addSubtitle(const Word &sub)
{
	m_subs.insert(sub);

	auto first = m_refs.lower_bound(Word(sub.time - m_windowSize, 0.0f));
	auto last  = m_refs.upper_bound(Word(sub.time + m_windowSize, 1.0f));
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

bool Correlator::addReference(const Word &ref)
{
	m_refs.insert(ref);

	auto first = m_subs.lower_bound(Word(ref.time - m_windowSize, 0.0f));
	auto last  = m_subs.upper_bound(Word(ref.time + m_windowSize, 1.0f));
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

Points Correlator::correlate() const
{
	double cor;

	Line bestLine = m_lineFinder.getBestLine();
	const Points &points = m_lineFinder.getPoints();
	Points hits = bestLine.getPointsInLine(points, 10.0f*m_maxDistanceSqr);

	Line line(hits, NULL, NULL, &cor);
	float distSqr = line.findFurthestPoint(hits);

	while ((cor < m_minCorrelation || distSqr > m_maxDistanceSqr)
			&& (hits.size() > m_minPointsNo))
	{
		distSqr = line.removeFurthestPoint(hits);
		line = Line(hits, NULL, NULL, &cor);
	}

	if (m_statsCb)
	{
		CorrelationStats stats;

		stats.correlated =
			cor >= m_minCorrelation &&
			hits.size() >= m_minPointsNo &&
			distSqr <= m_maxDistanceSqr;

		stats.factor = cor;
		stats.points = hits.size();
		stats.maxDistance = sqrt(distSqr);
		stats.formula = line;

		if (m_state == State::running || m_state == State::finishing)
			m_statsCb(stats);
	}

	return hits;
}

Correlator::Entrys Correlator::getSubs() const
{
	if (m_state != State::idle)
		throw EXCEPTION("subtitle words cannot be obtained when the correlator is running")
			.module("Correlator");

	return m_subs;
}

Correlator::Entrys Correlator::getRefs() const
{
	if (m_state != State::idle)
		throw EXCEPTION("reference words cannot be obtained when the correlator is running")
			.module("Correlator");

	return m_refs;
}

Points Correlator::getAllPoints() const
{
	return m_lineFinder.getPoints();
}

Points Correlator::getUsedPoints() const
{
	return correlate();
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

