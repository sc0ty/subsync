#include "general/thread.h"
#include "general/scope.h"
#include "general/logger.h"

using namespace std;


Thread::Thread(Runnable runnable, const string &name) :
	m_thread(&Thread::run, this, runnable, name),
	m_running(true)
{ }

Thread::~Thread()
{
	if (m_thread.joinable())
		m_thread.join();
}

bool Thread::isRunning() const
{
	return m_running;
}

void Thread::run(Runnable runnable, const string &name)
{
	ScopeExit done([this](){ m_running = false; });

	if (!name.empty())
		renameThread(name);

	try
	{
		runnable();
	}
	catch (const std::exception &ex)
	{
		log(LogLevel::LOG_ERROR, "thread", ex.what());
	}
	catch (...)
	{
		log(LogLevel::LOG_ERROR, "thread", "fatal error");
	}
}


bool Sleeper::sleep(float time)
{
	unique_lock<std::mutex> lock(m_mutex);
	auto ms = chrono::milliseconds((int)(time * 1000.f));
	return m_cond.wait_for(lock, ms) == cv_status::timeout;
}

void Sleeper::wake()
{
	unique_lock<std::mutex> lock(m_mutex);
	m_cond.notify_all();
}
