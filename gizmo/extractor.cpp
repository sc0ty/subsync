#include "extractor.h"
#include "general/thread.h"
#include "general/exception.h"
#include <cfloat>

using namespace std;


Extractor::Extractor(Demux &demux) :
	m_running(false),
	m_demux(demux),
	m_beginTime(0.0),
	m_endTime(DBL_MAX)
{}

Extractor::~Extractor()
{
	terminate();
}

const StreamsFormat &Extractor::getStreamsInfo() const
{
	return m_demux.getStreamsInfo();
}

void Extractor::selectTimeWindow(double begin, double end)
{
	if (begin > end || begin != begin || end != end)
		throw EXCEPTION("invalid time window").module("extractor")
			.add("begin", begin).add("end", end);

	m_beginTime = begin;
	m_endTime = end;
}

void Extractor::connectEosCallback(EosCallback callback)
{
	m_eosCb = callback;
}

void Extractor::connectErrorCallback(ErrorCallback callback)
{
	m_errorCb = callback;
}

void Extractor::start()
{
	terminate();
	m_running = true;
	m_thread = thread(&Extractor::run, this);
}

void Extractor::stop(bool wait)
{
	m_running = false;
	if (wait)
		terminate();
}

bool Extractor::isRunning() const
{
	return m_running;
}

void Extractor::run()
{
	lowerThreadPriority();

	try
	{
		m_demux.seek(m_beginTime);
		m_demux.start();
	}
	catch (Exception &ex)
	{
		m_running = false;

		if (m_errorCb)
		{
			ex.add("terminated", 1);
			m_errorCb(ex);
		}
	}
	catch (const std::exception& ex)
	{
		m_errorCb(EXCEPTION(ex.what()).module("extractor").add("terminated", 1));
	}
	catch (...)
	{
		m_errorCb(EXCEPTION("fatal error").module("extractor").add("terminated", 1));
	}

	while (m_running)
	{
		try
		{
			while (m_running)
			{
				if (!m_demux.step() || (m_demux.getPosition() >= m_endTime))
				{
					m_running = false;
					if (m_eosCb)
						m_eosCb();
				}
			}
		}
		catch (const Exception &ex)
		{
			m_demux.notifyDiscontinuity();

			if (m_errorCb)
				m_errorCb(ex);
		}
		catch (const std::exception& ex)
		{
			m_errorCb(EXCEPTION(ex.what()).module("extractor"));
		}
		catch (...)
		{
			m_errorCb(EXCEPTION("fatal error").module("extractor"));
		}
	}

	m_demux.stop();
	m_threadEndSem.wait();
}

void Extractor::terminate()
{
	m_running = false;

	if (m_thread.joinable())
	{
		m_threadEndSem.post();
		m_thread.join();
	}

	m_threadEndSem.reset();
}

