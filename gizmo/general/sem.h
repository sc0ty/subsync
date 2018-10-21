#ifndef __SEM_H__
#define __SEM_H__

#include <mutex>
#include <condition_variable>


class Semaphore
{
	public:
		Semaphore (int count = 0) : m_count(count)
	{}

		inline void post()
		{
			std::unique_lock<std::mutex> lock(m_mutex);
			m_count++;
			m_cond.notify_one();
		}

		inline void wait()
		{
			std::unique_lock<std::mutex> lock(m_mutex);
			while(m_count == 0) m_cond.wait(lock);
			m_count--;
		}

		inline void reset()
		{
			std::unique_lock<std::mutex> lock(m_mutex);
			m_count = 0;
		}

	private:
		std::mutex m_mutex;
		std::condition_variable m_cond;
		int m_count;
};

#endif
