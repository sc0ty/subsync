#include "extractor.h"
#include "general/thread.h"
#include "general/exception.h"
#include <pybind11/pybind11.h>
#include <cfloat>

using namespace std;
namespace py = pybind11;


Extractor::Extractor(shared_ptr<Demux> demux) :
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
	return m_demux->getStreamsInfo();
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

void Extractor::stop()
{
	m_running = false;
}

bool Extractor::isRunning() const
{
	return m_running;
}

void Extractor::run()
{
	lowerThreadPriority();
	Demux *demux = m_demux.get();

	try
	{
		demux->seek(m_beginTime);
		demux->start();
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
				if (!demux->step() || (demux->getPosition() >= m_endTime))
				{
					m_running = false;
					if (m_eosCb)
						m_eosCb();
				}
			}
		}
		catch (const Exception &ex)
		{
			if (m_running)
				demux->notifyDiscontinuity();

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

	try
	{
		demux->stop();
	}
	catch (...)
	{ }

	m_demux = NULL;
}

void Extractor::terminate()
{
	m_running = false;

	if (m_thread.joinable())
	{
		py::gil_scoped_release release;
		m_thread.join();
	}
}

