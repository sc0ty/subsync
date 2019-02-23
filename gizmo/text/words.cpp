#include "words.h"


Word::Word() : time(0.0f), score(0.0f)
{
}

Word::Word(float time, float score) : time(time), score(score)
{
}

Word::Word(const std::string &text, float time, float score)
	: text(text), time(time), score(score)
{
}

bool Word::operator< (const Word &w) const
{
	return time != w.time ? time < w.time
		: (score != w.score ? score < w.score : text < w.text);
}
