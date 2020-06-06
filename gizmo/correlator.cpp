#include "correlator.h"
#include "general/thread.h"
#include "general/scope.h"
#include "general/exception.h"
#include <sstream>
#include <iomanip>
#include <cmath>

using namespace std;

#ifdef USE_PYBIND11
#include <pybind11/pybind11.h>
#endif


Correlator::Correlator(
		float windowSize,
		double minCorrelation,
		float maxDistance,
		unsigned minPointsNo,
		float minWordsSim) :
	m_state(State::idle),
	m_wordsNo(0),
	m_sync(windowSize, minCorrelation, maxDistance, minPointsNo, minWordsSim)
{
}

Correlator::~Correlator()
{
	stop(true);
	wait();
}

void Correlator::pushSubWord(const Word &word)
{
	m_queue.push(WordId::SUB, word);
}

void Correlator::pushRefWord(const Word &word)
{
	m_queue.push(WordId::REF, word);
}

void Correlator::pushSubtitle(double start, double end, const char* text)
{
	(void) text;
	m_queue.push(WordId::BUCKET, Word(start, end-start, 0.0f));
}

void Correlator::run(const string threadName)
{
	CorrelationStats bestStats;

	ScopeExit done([this, &bestStats]()
	{
		m_state = State::idle;

		if (m_statsCb)
			m_statsCb(bestStats);
	});

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
			newBestLine = m_sync.addSubWord(word);
		else if (id == WordId::REF)
			newBestLine = m_sync.addRefWord(word);
		else if (id == WordId::BUCKET)
			m_sync.addSubtitle(word.time, word.time+word.duration);

		if (newBestLine)
		{
			CorrelationStats stats = m_sync.correlate();
			if (m_statsCb && (stats.correlated || !bestStats.correlated))
			{
				bestStats = stats;
				m_statsCb(stats);
			}
		}
	}
}

void Correlator::wait()
{
	if (m_thread.joinable())
	{
		m_queue.release();

#ifdef USE_PYBIND11
		pybind11::gil_scoped_release release;
#endif
		m_thread.join();
	}

	m_state = State::idle;
}

void Correlator::start(const std::string &threadName)
{
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

const std::set<Word> &Correlator::getSubs() const
{
	if (m_state != State::idle)
		throw EXCEPTION("subtitle words cannot be obtained when the correlator is running")
			.module("Correlator");

	return m_sync.getSubs();
}

const std::set<Word> &Correlator::getRefs() const
{
	if (m_state != State::idle)
		throw EXCEPTION("reference words cannot be obtained when the correlator is running")
			.module("Correlator");

	return m_sync.getRefs();
}

Points Correlator::getAllPoints() const
{
	if (m_state != State::idle)
		throw EXCEPTION("points cannot be obtained when the correlator is running")
			.module("Correlator");

	return m_sync.getAllPoints();
}

Points Correlator::getUsedPoints() const
{
	if (m_state != State::idle)
		throw EXCEPTION("points cannot be obtained when the correlator is running")
			.module("Correlator");

	return m_sync.getUsedPoints();
}
