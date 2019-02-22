#ifndef __WORDSQUEUE_H__
#define __WORDSQUEUE_H__

#include "words.h"
#include "general/sem.h"
#include <string>
#include <queue>


class WordsQueue
{
	private:
		struct Entry
		{
			WordId id;
			std::string word;
			float time;

			Entry();
			Entry(WordId id, const std::string &word, float time);
		};

	public:
		WordsQueue();
		~WordsQueue();

		void push(WordId id, const std::string &word, float time);
		WordId pop(std::string &word, float &time);
		void release();

		size_t size() const;
		bool empty() const;

	private:
		std::queue<Entry> m_queue;
		mutable std::mutex m_mutex;
		Semaphore m_sem;
};

#endif
