#include "words.h"
#include <sstream>

using namespace std;


Word::Word() : time(0.0f), duration(0.0f), score(0.0f)
{
}

Word::Word(float time, float duration, float score)
	: time(time), duration(duration), score(score)
{
}

Word::Word(const std::string &text, float time, float duration, float score)
	: text(text), time(time), duration(duration), score(score)
{
}

bool Word::operator< (const Word &w) const
{
	if (time != w.time)
		return time < w.time;
	if (duration != w.duration)
		return duration < w.duration;
	if (score != w.score)
		return score < w.score;
	return text < w.text;
}

string Word::toString() const
{
	stringstream ss;
	ss << "<Word " << "time=" << time;
	if (duration) ss << ", duration=" << duration;
	if (score < 1.0f) ss << ", score=" << score;
	ss << ", text=\"" << text << "\">";
	return ss.str();
}
