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
		typedef std::map<float /* end */, float /* start */> Buckets;

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
		void stop(bool force=false);
		void wait();

		bool isRunning() const;
		float getProgress() const;

		void pushSubWord(const Word &word);
		void pushRefWord(const Word &word);
		void pushSubtitle(double start, double end, const char* text);

		Entrys getSubs() const;
		Entrys getRefs() const;

		Points getAllPoints() const;
		Points getUsedPoints() const;

	private:
		void run(const std::string threadName);

		bool addSubtitle(const Word &word);
		bool addReference(const Word &word);

		CorrelationStats correlate() const;
		unsigned countPoints(const Points &pts) const;

	private:
		enum class State
		{
			running,    // normal operation
			finishing,  // will stop after pending words queue exhaustion
			stopping,   // terminating
			idle,       // thread is not running
		};

	private:
		Entrys m_subs;
		Entrys m_refs;
		Buckets m_buckets;

		std::atomic<State> m_state;
		std::thread m_thread;

		WordsQueue m_queue;
		std::atomic_size_t m_wordsNo;

		LineFinder m_lineFinder;
		bool m_correlated;

		StatsCallback m_statsCb;

		float    m_windowSize;
		double   m_minCorrelation;
		float    m_maxDistanceSqr;
		unsigned m_minPointsNo;
		float    m_minWordsSim;
};

#endif
