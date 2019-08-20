#include "dictionary.h"
#include "utf8.h"
#include <list>

using namespace std;


Dictionary::Dictionary(size_t minLen, bool rightToLeftKey, bool rightToLeftVal,
		size_t ngramsKey, size_t ngramsVal) :
	m_minLenKey(minLen),
	m_minLenVal(minLen),
	m_rightToLeftKey(rightToLeftKey),
	m_rightToLeftVal(rightToLeftVal),
	m_ngramsKey(ngramsKey),
	m_ngramsVal(ngramsVal)
{
	if (ngramsKey) m_minLenKey = ngramsKey;
	if (ngramsVal) m_minLenVal = ngramsVal;
}

static list<string> splitNgrams(const string &word, size_t ngram)
{
	list<string> res;
	if (ngram == 0)
	{
		res.push_back(word);
	}
	else if (Utf8::size(word) >= ngram)
	{
		Utf8::iterator beg(word);
		Utf8::iterator end = beg;
		end += ngram;

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

void Dictionary::add(string key, string val)
{
	if (Utf8::size(key) < m_minLenKey) return;
	if (Utf8::size(val) < m_minLenVal) return;

	if (m_rightToLeftKey) key = Utf8::reverse(key);
	if (m_rightToLeftVal) val = Utf8::reverse(val);

	for (const string &k : splitNgrams(key, m_ngramsKey))
	{
		for (const string &v : splitNgrams(val, m_ngramsVal))
		{
			addRaw(k, v);
		}
	}
}

void Dictionary::addRaw(const std::string &key, const std::string &val)
{
	auto &values = m_entrys[Utf8::toLower(key)];
	for (auto &v : values)
	{
		if (val == v)
			return;
	}
	values.push_back(val);
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

Dictionary::Entrys::const_iterator Dictionary::begin() const
{
	return m_entrys.begin();
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

