#ifndef __CORRELATOR_H__
#define __CORRELATOR_H__

#include "synchro/synchronizer.h"
#include "text/wordsqueue.h"
#include <set>
#include <string>
#include <thread>
#include <atomic>
#include <cmath>


class Correlator
{
	public:
		typedef std::function<void (CorrelationStats)> StatsCallback;

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

		const std::set<Word> &getSubs() const;
		const std::set<Word> &getRefs() const;

		Points getAllPoints() const;
		Points getUsedPoints() const;

	private:
		void run(const std::string threadName);

	private:
		enum class State
		{
			running,    // normal operation
			finishing,  // will stop after pending words queue exhaustion
			stopping,   // terminating
			idle,       // thread is not running
		};

	private:
		std::atomic<State> m_state;
		std::thread m_thread;

		WordsQueue m_queue;
		std::atomic_size_t m_wordsNo;

		Synchronizer m_sync;
		StatsCallback m_statsCb;
};

#endif
