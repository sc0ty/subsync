#ifndef __THREAD_H__
#define __THREAD_H__

#include <thread>
#include <condition_variable>
#include <mutex>
#include <atomic>
#include <functional>
#include <chrono>
#include <string>


class Thread
{
	public:
		typedef std::function<void()> Runnable;

	public:
		Thread(Runnable runnable, const std::string &name);
		~Thread();

		bool isRunning() const;

		Thread(const Thread&) = delete;
		Thread(Thread&&) = delete;
		Thread& operator= (Thread&&) = delete;
		Thread& operator= (const Thread&) = delete;

	private:
		void run(Runnable runnable, const std::string &name);

	private:
		std::thread m_thread;
		std::atomic_bool m_running;
};


class Sleeper
{
	public:
		bool sleep(float time);
		void wake();

		Sleeper() = default;
		Sleeper(const Sleeper&) = delete;
		Sleeper(Sleeper&&) = delete;
		Sleeper& operator= (Sleeper&&) = delete;
		Sleeper& operator= (const Sleeper&) = delete;

	private:
		std::condition_variable m_cond;
		std::mutex m_mutex;
};


void lowerThreadPriority();
void renameThread(const std::string &name);

#endif
