#ifndef __CORRELATOR_H__
#define __CORRELATOR_H__

#include "math/linefinder.h"
#include "text/wordsqueue.h"
#include <functional>
#include <mutex>
#include <map>
#include <vector>
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
		typedef std::multimap<double /* time */, std::string /* word */> Entrys;
		typedef std::vector<std::pair<double, std::string>> ElementsVector;

	public:
		Correlator(
				float    windowSize     = HUGE_VALF,
				double   minCorrelation = 0.0,
				float    maxDistance    = HUGE_VALF,
				unsigned minPointsNo    = 0,
				float    minWordsSim    = 0.5);

		virtual ~Correlator();

		void connectStatsCallback(StatsCallback callback);

		void start();
		void stop();

		bool isRunning() const;
		bool isDone() const;
		float getProgress() const;

		void pushSubWord(const std::string &word, double time);
		void pushRefWord(const std::string &word, double time);

		ElementsVector getSubs() const;
		ElementsVector getRefs() const;

	private:
		void run();
		void terminate();

		bool addSubtitle(double time, const std::string &word);
		bool addReference(double time, const std::string &word);

		void correlate() const;

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

		double   m_windowSize;
		double   m_minCorrelation;
		float    m_maxDistance;
		unsigned m_minPointsNo;
		float    m_minWordsSim;
};

#endif