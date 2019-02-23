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
			Word word;

			Entry();
			Entry(WordId id, const Word &word);
		};

	public:
		WordsQueue();
		~WordsQueue();

		void push(WordId id, const Word &word);
		WordId pop(Word &word);
		void release();

		size_t size() const;
		bool empty() const;

	private:
		std::queue<Entry> m_queue;
		mutable std::mutex m_mutex;
		Semaphore m_sem;
};

#endif
