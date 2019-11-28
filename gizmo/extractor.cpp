#include "extractor.h"
#include "general/thread.h"
#include "general/scope.h"
#include "general/exception.h"
#include <pybind11/pybind11.h>
#include <cfloat>

using namespace std;
namespace py = pybind11;


Extractor::Extractor(shared_ptr<Demux> demux) :
	m_state(State::idle),
	m_demux(demux),
	m_beginTime(0.0),
	m_endTime(DBL_MAX)
{}

Extractor::~Extractor()
{
	stop();
	wait();
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

void Extractor::start(const string &threadName)
{
	m_state = State::running;
	m_thread = thread(&Extractor::run, this, threadName);
}

void Extractor::stop()
{
	if (m_state == State::running)
		m_state = State::stopping;
}

bool Extractor::isRunning() const
{
	return m_state != State::idle;
}

void Extractor::run(string threadName)
{
	ScopeExit done([this](){ m_state = State::idle; });

	lowerThreadPriority();

	if (!threadName.empty())
		renameThread(threadName);

	Demux *demux = m_demux.get();

	try
	{
		demux->seek(m_beginTime);
		demux->start();

		while (m_state == State::running)
		{
			try
			{
				while (m_state == State::running)
				{
					if (!demux->step() || (demux->getPosition() >= m_endTime))
						m_state = State::stopping;
				}
			}
			catch (const Exception &ex)
			{
				if (m_state == State::running)
					demux->notifyDiscontinuity();

				if (m_errorCb && ex.get("averror") != "AVERROR_EXIT")
					m_errorCb(ex);
			}
		}
	}
	catch (const Exception &ex)
	{
		if (m_errorCb && ex.get("averror") != "AVERROR_EXIT")
			m_errorCb(ex);
	}
	catch (const std::exception& ex)
	{
		if (m_errorCb)
			m_errorCb(EXCEPTION(ex.what()).module("extractor"));
	}
	catch (...)
	{
		if (m_errorCb)
			m_errorCb(EXCEPTION("fatal error").module("extractor"));
	}

	try
	{
		demux->stop();
	}
	catch (...)
	{ }

	m_demux = NULL;
	m_state = State::idle;

	try
	{
		if (m_eosCb)
			m_eosCb();
	}
	catch (...)
	{ }
}

void Extractor::wait()
{
	if (m_thread.joinable())
	{
		py::gil_scoped_release release;
		m_thread.join();
	}

	m_state = State::idle;
}

