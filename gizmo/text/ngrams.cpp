#include "text/ngrams.h"
#include "text/utf8.h"

using namespace std;


NgramSplitter::NgramSplitter(size_t size) : m_size(size)
{
}

void NgramSplitter::addWordsListener(WordsListener listener)
{
	m_wordsNotifier.addListener(listener);
}

bool NgramSplitter::removeWordsListener(WordsListener listener)
{
	return m_wordsNotifier.removeListener(listener);
}

void NgramSplitter::pushWord(const Word &word)
{
	const size_t wordSize = Utf8::size(word.text);

	if (wordSize >= m_size)
	{
		Utf8::iterator beg(word.text);
		Utf8::iterator end = beg;
		end += m_size;

		float time = word.time;
		const float delta = word.duration / (float) wordSize;
		const float duration = delta * (float) m_size;

		while (true)
		{
			m_wordsNotifier.notify(
					Word(Utf8::substr(beg, end), time, duration, word.score));

			if (!*end)
				break;

			++beg;
			++end;
			time += delta;
		}
	}
}
