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
		SSAParser(const char *wordDelimiters=NULL);

		void setWordDelimiters(const char *delimiters);
		void setMode(bool rtl=false, size_t ngram=0);

		Words splitWords(const char *ssa) const;

		static const char *skipHeader(const char *ssa);

	private:
		Words::iterator addWord(Words &words, std::string &word,
				Words::iterator pos) const;

	private:
		bool m_rightToLeft;
		size_t m_ngram;
		std::set<uint32_t> m_wordDelimiters;
};

#endif
