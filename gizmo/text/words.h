#ifndef __WORDS_H__
#define __WORDS_H__

#include <functional>
#include <string>


struct Word
{
	std::string text;
	float time;
	float score;

	Word();
	Word(float time, float score);
	Word(const std::string &text, float time, float score=1.0f);

	bool operator< (const Word &w) const;
};


typedef std::function<void (const Word &)> WordsCallback;


enum class WordId
{
	NONE = -1,
	SUB = 0,
	REF = 1,
};

#endif
