#ifndef __NGRAMS_H__
#define __NGRAMS_H__

#include "text/words.h"


class NgramSplitter
{
	public:
		NgramSplitter(size_t size);
		void connectWordsCallback(WordsCallback callback);
		void pushWord(const Word &word);

	private:
		size_t m_size;
		WordsCallback m_wordsCb;
};

#endif
