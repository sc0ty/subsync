#include "text/wordsqueue.h"

using namespace std;

WordsQueue::WordsQueue()
{}

WordsQueue::~WordsQueue()
{
	release();
}

void WordsQueue::push(WordId id, const string &word, double time)
{
	{
		unique_lock<mutex> lock(m_mutex);
		m_queue.push(Entry(id, word, time));
	}
	m_sem.post();
}

WordId WordsQueue::pop(string &word, double &time)
{
	WordId id = WordId::None;

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
		time = e.time;
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

WordsQueue::Entry::Entry() : id(WordId::None)
{}

WordsQueue::Entry::Entry(WordId id, const string &word, double time)
	: id(id), word(word), time(time)
{}

