#include "text/ngrams.h"
#include "text/utf8.h"

using namespace std;


NgramSplitter::NgramSplitter(size_t size) :
	m_size(size),
	m_wordsCb(NULL)
{
}

void NgramSplitter::connectWordsCallback(WordsCallback callback)
{
	m_wordsCb = callback;
}

void NgramSplitter::pushWord(const Word &word)
{
	if (m_wordsCb)
	{
		Utf8::iterator beg(word.text);
		Utf8::iterator end = beg;

		size_t cps;
		for (cps = 0; cps < m_size && *end; cps++)
			++end;

		if (cps >= m_size)
		{
			while (true)
			{
				m_wordsCb(Word(Utf8::substr(beg, end), word.time, word.score));
				if (!*end)
					break;

				++beg;
				++end;
			}
		}
	}
}
