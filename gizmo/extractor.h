#ifndef __EXTRACTOR_H__
#define __EXTRACTOR_H__

#include "media/demux.h"
#include "general/sem.h"
#include "general/exception.h"
#include <functional>
#include <thread>
#include <atomic>
#include <memory>
#include <string>


class Extractor
{
	public:
		typedef std::function<void (void)> EosCallback;
		typedef std::function<void (const Exception &)> ErrorCallback;

	public:
		Extractor(std::shared_ptr<Demux> demux);
		~Extractor();

		const StreamsFormat &getStreamsInfo() const;

		void selectTimeWindow(double beginTime, double endTime);

		void connectEosCallback(EosCallback callback);
		void connectErrorCallback(ErrorCallback callback);

		void start();
		void stop();
		bool isRunning() const;

	private:
		void run();
		void terminate();

	private:
		std::thread m_thread;

		std::atomic_bool m_running;
		std::shared_ptr<Demux> m_demux;

		double m_beginTime;
		double m_endTime;

		EosCallback m_eosCb;
		ErrorCallback m_errorCb;
};

#endif
