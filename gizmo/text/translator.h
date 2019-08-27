#ifndef __TRANSLATOR_H__
#define __TRANSLATOR_H__

#include "text/words.h"
#include "text/dictionary.h"
#include <string>


class Translator
{
	public:
		Translator(const Dictionary &dictionary);

		void pushWord(const Word &word);

		void addWordsListener(WordsListener listener);
		bool removeWordsListener(WordsListener listener);

		void setMinWordsSim(float minSim);

	private:
		const Dictionary &m_dict;
		WordsNotifier m_wordsNotifier;
		float m_minSim;
};

#endif
