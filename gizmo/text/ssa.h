#ifndef __TEXT_SSA__
#define __TEXT_SSA__

#include "words.h"
#include <list>
#include <set>
#include <string>


class SSAParser
{
	public:
		typedef std::list<std::string> WordList;

	public:
		SSAParser(const char *wordDelimiters=NULL, bool rightToLeft=false);

		void setWordDelimiters(const char *delimiters);
		void setRightToLeft(bool rtl=true);

		size_t splitWords(WordList &words, const char *ssa) const;

		static const char *skipHeader(const char *ssa);

	private:
		WordList::iterator addWord(WordList &words, std::string &word,
				WordList::iterator pos) const;

	private:
		bool m_rightToLeft;
		std::set<uint32_t> m_wordDelimiters;
};

#endif
