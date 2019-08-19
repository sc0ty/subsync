#ifndef __TEXT_SSA__
#define __TEXT_SSA__

#include <list>
#include <set>
#include <string>


class SSAParser
{
	public:
		typedef std::list<std::string> Words;

	public:
		SSAParser(bool rightToLeft=false, const char *wordDelimiters=NULL);

		void setWordDelimiters(const char *delimiters);
		void setRightToLeft(bool rtl=true);

		Words splitWords(const char *ssa) const;

		static const char *skipHeader(const char *ssa);

	private:
		Words::iterator addWord(Words &words, std::string &word,
				Words::iterator pos) const;

	private:
		bool m_rightToLeft;
		std::set<uint32_t> m_wordDelimiters;
};

#endif
