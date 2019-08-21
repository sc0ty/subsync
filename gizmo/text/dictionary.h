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
		void add(const std::string &key, const std::string &value);
		size_t size() const;

		const std::vector<std::string> &translate(const std::string &text) const;

		Entrys::const_iterator bestGuess(const std::string &text) const;
		Entrys::const_iterator begin() const;
		Entrys::const_iterator end() const;

	private:
		Entrys m_entrys;
};


float compareWords(const std::string &word1, const std::string &word2);

#endif
