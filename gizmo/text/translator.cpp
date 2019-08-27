#include "translator.h"
#include "utf8.h"

using namespace std;


Translator::Translator(const Dictionary &dict) : m_dict(dict), m_minSim(1.0f)
{
}

void Translator::addWordsListener(WordsListener listener)
{
	m_wordsNotifier.addListener(listener);
}

bool Translator::removeWordsListener(WordsListener listener)
{
	return m_wordsNotifier.removeListener(listener);
}

void Translator::setMinWordsSim(float minSim)
{
	m_minSim = minSim;
}

void Translator::pushWord(const Word &word)
{
	const string lword = Utf8::toLower(word.text);
	auto it1 = m_dict.bestGuess(lword);
	auto it2 = it1;

	if (it1 == m_dict.end())
		return;

	while (true)
	{
		float sim = compareWords(lword, it1->first);
		if (sim < m_minSim)
			break;

		for (auto &tr : it1->second)
			m_wordsNotifier.notify(Word(tr, word.time, word.duration, word.score*sim));

		if (it1 == m_dict.begin())
			break;

		--it1;
	}

	for (++it2; it2 != m_dict.end(); ++it2)
	{
		float sim = compareWords(lword, it2->first);
		if (sim < m_minSim)
			break;

		for (auto &tr : it2->second)
			m_wordsNotifier.notify(Word(tr, word.time, word.duration, word.score*sim));
	}
}
