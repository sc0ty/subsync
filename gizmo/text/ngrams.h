#ifndef __NGRAMS_H__
#define __NGRAMS_H__

#include "text/words.h"


class NgramSplitter
{
	public:
		NgramSplitter(size_t size);
		void addWordsListener(WordsListener listener);
		bool removeWordsListener(WordsListener listener);
		void pushWord(const Word &word);

	private:
		size_t m_size;
		WordsNotifier m_wordsNotifier;
};

#endif
