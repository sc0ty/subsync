#ifndef __CORRELATOR_H__
#define __CORRELATOR_H__

#include "math/linefinder.h"
#include "text/wordsqueue.h"
#include <set>
#include <string>
#include <thread>
#include <atomic>
#include <cmath>


struct CorrelationStats
{
	bool     correlated;
	double   factor;
	unsigned points;
	float    maxDistance;
	Line     formula;

	CorrelationStats();
	std::string toString(
			const char *prefix="<CorrelationStats ",
			const char *suffix=">") const;
};


class Correlator
{
	public:
		typedef std::function<void (CorrelationStats)> StatsCallback;
		typedef std::set<Word> Entrys;

	public:
		Correlator(
				float    windowSize     = HUGE_VALF,
				double   minCorrelation = 0.0,
				float    maxDistance    = HUGE_VALF,
				unsigned minPointsNo    = 0,
				float    minWordsSim    = 0.5);

		~Correlator();

		void connectStatsCallback(StatsCallback callback);

		void start(const std::string &threadName="");
		void stop();

		bool isRunning() const;
		bool isDone() const;
		float getProgress() const;

		void pushSubWord(const Word &word);
		void pushRefWord(const Word &word);

		Entrys getSubs() const;
		Entrys getRefs() const;

		Points getAllPoints() const;
		Points getUsedPoints() const;

	private:
		void run(const std::string threadName);
		void terminate();

		bool addSubtitle(const Word &word);
		bool addReference(const Word &word);

		Points correlate() const;

	private:
		Entrys m_subs;
		Entrys m_refs;

		std::atomic_bool m_running;
		std::thread m_thread;
		Semaphore m_threadEndSem;

		WordsQueue m_queue;
		std::atomic_size_t m_wordsNo;

		LineFinder m_lineFinder;

		StatsCallback m_statsCb;
		CorrelationStats m_stats;

		float    m_windowSize;
		double   m_minCorrelation;
		float    m_maxDistanceSqr;
		unsigned m_minPointsNo;
		float    m_minWordsSim;
};

#endif
