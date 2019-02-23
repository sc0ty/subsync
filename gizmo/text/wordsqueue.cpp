#include "text/wordsqueue.h"

using namespace std;

WordsQueue::WordsQueue()
{}

WordsQueue::~WordsQueue()
{
	release();
}

void WordsQueue::push(WordId id, const Word &word)
{
	{
		unique_lock<mutex> lock(m_mutex);
		m_queue.push(Entry(id, word));
	}
	m_sem.post();
}

WordId WordsQueue::pop(Word &word)
{
	WordId id = WordId::NONE;

	unique_lock<mutex> lock(m_mutex);
	if (m_queue.empty())
	{
		lock.unlock();
		m_sem.wait();
		lock.lock();
	}

	if (!m_queue.empty())
	{
		const Entry &e = m_queue.front();
		id = e.id;
		word = e.word;
		m_queue.pop();
	}

	return id;
}

void WordsQueue::release()
{
	m_sem.post();
}

size_t WordsQueue::size() const
{
	unique_lock<mutex> lock(m_mutex);
	return m_queue.size();
}

bool WordsQueue::empty() const
{
	unique_lock<mutex> lock(m_mutex);
	return m_queue.empty();
}

WordsQueue::Entry::Entry() : id(WordId::NONE)
{}

WordsQueue::Entry::Entry(WordId id, const Word &word)
	: id(id), word(word)
{}

