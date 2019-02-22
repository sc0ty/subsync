#ifndef __TRANSLATOR_H__
#define __TRANSLATOR_H__

#include "text/words.h"
#include "text/dictionary.h"
#include <string>


class Translator
{
	public:
		Translator(const Dictionary &dictionary);

		void pushWord(const std::string &word, float time);

		void connectWordsCallback(WordsCallback m_wordsCb);
		void setMinWordsSim(float minSim);

	private:
		const Dictionary &m_dict;
		WordsCallback m_wordsCb;
		float m_minSim;
};

#endif
