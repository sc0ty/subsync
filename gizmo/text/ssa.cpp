#include "text/ssa.h"
#include "text/utf8.h"

using namespace std;


const char *SSAParser::skipHeader(const char *ssa)
{
	const char *text = ssa;
	unsigned commas = 0;

	while (*text != '\0')
	{
		if (*text++ == ',' && ++commas >= 8)
			break;
	}

	// invalid header, assuming raw data (nothing is skipped)
	if (commas < 8)
		return ssa;

	return text;
}


SSAParser::SSAParser(bool rightToLeft, const char *wordDelimiters) :
	m_rightToLeft(rightToLeft)
{
	if (wordDelimiters)
		setWordDelimiters(wordDelimiters);
}

void SSAParser::setWordDelimiters(const char *delimiters)
{
	for (Utf8::iterator it(delimiters); *it; ++it)
		m_wordDelimiters.insert(*it);
}

void SSAParser::setRightToLeft(bool rtl)
{
	m_rightToLeft = rtl;
}

SSAParser::Words SSAParser::splitWords(const char *ssa) const
{
	list<string> words;
	string word;
	Words::iterator pos = words.begin();

	for (Utf8::iterator it(skipHeader(ssa)); *it; ++it)
	{
		const char *data = it.getRawData();

		if (data[0] == '\\' && data[1] == 'N')
		{
			++it;
			pos = addWord(words, word, pos);
			pos = words.end();
		}
		else if (data[0] == '\n')
		{
			pos = addWord(words, word, pos);
			pos = words.end();
		}
		else if (data[0] == '{' && data[1] == '\\')
		{
			++it;
			while (*it && *it != '}')
				++it;

			pos = addWord(words, word, pos);
		}
		else if (m_wordDelimiters.count(*it))
		{
			pos = addWord(words, word, pos);
		}
		else
		{
			if (m_rightToLeft)
				word = string(data, it.cpSize()) + word;
			else
				word += string(data, it.cpSize());
		}
	}

	addWord(words, word, pos);
	return words;
}

SSAParser::Words::iterator SSAParser::addWord(Words &words, string &word,
		Words::iterator pos) const
{
	if (!word.empty())
	{
		pos = words.insert(pos, word);
		word.clear();
		if (!m_rightToLeft)
			++pos;
	}
	return pos;
}
