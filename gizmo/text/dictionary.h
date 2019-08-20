#ifndef __DICTIONARY_H__
#define __DICTIONARY_H__

#include <map>
#include <vector>
#include <string>


class Dictionary
{
	public:
		typedef std::map< std::string, std::vector<std::string> > Entrys;

	public:
		Dictionary(size_t minLen,
				bool rightToLeftKey=false,
				bool rightToLeftVal=false,
				size_t ngramsKey=0,
				size_t ngramsVal=0);

		void add(std::string key, std::string value);
		size_t size() const;

		const std::vector<std::string> &translate(const std::string &text) const;

		Entrys::const_iterator bestGuess(const std::string &text) const;
		Entrys::const_iterator begin() const;
		Entrys::const_iterator end() const;

	private:
		void addRaw(const std::string &key, const std::string &value);

	private:
		Entrys m_entrys;

		size_t m_minLenKey;
		size_t m_minLenVal;
		bool m_rightToLeftKey;
		bool m_rightToLeftVal;
		size_t m_ngramsKey;
		size_t m_ngramsVal;
};


float compareWords(const std::string &word1, const std::string &word2);

#endif
