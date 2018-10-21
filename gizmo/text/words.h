#ifndef __WORDS_H__
#define __WORDS_H__

#include <functional>
#include <string>


typedef std::function<void (
		const std::string & /* word */,
		double /* timestamp */ )>
WordsCallback;


enum class WordId
{
	None = -1,
	Sub = 0,
	Ref = 1,
};

#endif
