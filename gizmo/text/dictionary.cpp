#include "dictionary.h"
#include "utf8.h"

using namespace std;


void Dictionary::add(const string &key, const string &value)
{
	auto &values = m_entrys[key];
	for (auto &v : values)
	{
		if (value == v)
			return;
	}
	values.push_back(value);
}

size_t Dictionary::size() const
{
	return m_entrys.size();
}

const vector<string> &Dictionary::translate(const string &text) const
{
	Entrys::const_iterator entry = m_entrys.find(text);
	if (entry == m_entrys.end())
	{
		static const vector<string> empty;
		return empty;
	}

	return entry->second;
}

Dictionary::Entrys::const_iterator Dictionary::bestGuess(const string &text) const
{
	Entrys::const_iterator it = m_entrys.lower_bound(text);
	if (it == m_entrys.end())
		it = m_entrys.upper_bound(text);

	return it;
}

Dictionary::Entrys::const_iterator Dictionary::end() const
{
	return m_entrys.end();
}


float compareWords(const string &word1, const string &word2)
{
	Utf8::iterator w1(word1);
	Utf8::iterator w2(word2);
	float sim = 0.f;
	float len = 0.f;

	while (*w1)
	{
		if (*w1 == *w2)
			sim += 2.0f;
		else if (w1.toLower() == w2.toLower())
			sim += 1.5f;
		else
			break;

		len += 2.f;
		++w1;
		++w2;
	}

	return sim / (len + w1.size() + w2.size());
}

