#ifndef __MEDIA_MEDIA__
#define __MEDIA_MEDIA__

#include "general/exception.h"
#include <string>


class FFmpegException : public Exception
{
	public:
		FFmpegException(const std::string &msg, int code) throw();
		virtual ~FFmpegException() throw();
		FFmpegException &averror(int errnum) throw();

		static std::string codeName(int code) throw();
		static std::string codeDescription(int code) throw();
};


#define EXCEPTION_FFMPEG(msg, code) \
	FFmpegException(msg, code).EXCEPTION_ADD_SOURCE

#endif
