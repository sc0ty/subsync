#ifndef __WORDS_H__
#define __WORDS_H__

#include "general/notifier.h"
#include <functional>
#include <string>
#include <vector>


struct Word
{
	std::string text;
	float time;
	float duration;
	float score;

	Word();
	Word(float time, float duration, float score);
	Word(const std::string &text, float time, float duration=0.0f,
			float score=1.0f);

	bool operator< (const Word &w) const;
	std::string toString() const;
};


typedef std::function<void (const Word &)> WordsListener;
typedef Notifier<const Word &> WordsNotifier;


enum class WordId
{
	NONE = -1,
	SUB = 0,
	REF = 1,
};

#endif
