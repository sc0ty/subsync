#include "text/ssa.h"
#include "text/utf8.h"

using namespace std;


static SSAParser::Words splitNgrams(const SSAParser::Words &words, size_t size);


SSAParser::SSAParser(const char *wordDelimiters) :
	m_rightToLeft(false),
	m_ngram(0)
{
	if (wordDelimiters)
		setWordDelimiters(wordDelimiters);
}

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

void SSAParser::setWordDelimiters(const char *delimiters)
{
	for (Utf8::iterator it(delimiters); *it; ++it)
		m_wordDelimiters.insert(*it);
}

void SSAParser::setMode(bool rtl, size_t ngram)
{
	m_rightToLeft = rtl;
	m_ngram = ngram;
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

	if (m_ngram)
		return splitNgrams(words, m_ngram);
	else
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

static SSAParser::Words splitNgrams(const SSAParser::Words &words, size_t size)
{
	SSAParser::Words res;

	for (const string &word : words)
	{
		Utf8::iterator beg(word);
		Utf8::iterator end = beg;
		end += size;

		while (true)
		{
			res.push_back(Utf8::substr(beg, end));
			if (!*end)
				break;

			++beg;
			++end;
		}
	}

	return res;
}
