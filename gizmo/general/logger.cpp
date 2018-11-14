#include "logger.h"
#include "text/utf8.h"
#include <sphinxbase/err.h>
#include <string>

extern "C"
{
#include <libavformat/avformat.h>
}


static LoggerCallback g_loggerCallback = NULL;
static int g_ffmpegLogLevel = AV_LOG_WARNING;
static int g_sphinxLogLevel = ERR_WARN;


static void logCb(LogLevel level, const char *module, const char *msg)
{
	if (Utf8::validate(msg))
	{
		if (g_loggerCallback)
			g_loggerCallback(level, module, msg);
	}
	else
	{
		std::string m = Utf8::escape(msg) + Utf8::encode(0xffff);
		if (g_loggerCallback)
			g_loggerCallback(level, module, m.c_str());
	}
}

static void ffmpegLogCb(void *avcl, int level, const char *fmt, va_list vl)
{
	if (g_loggerCallback && level >= g_ffmpegLogLevel)
	{
		static const int lineSize = 1024;
		char line[lineSize];
		static int printPrefix = 1;
		av_log_format_line(avcl, level, fmt, vl, line, lineSize, &printPrefix);

		LogLevel lvl = LOG_DEBUG;
		if      (level >= AV_LOG_DEBUG)   lvl = LOG_DEBUG;
		else if (level >= AV_LOG_INFO)    lvl = LOG_INFO;
		else if (level >= AV_LOG_WARNING) lvl = LOG_WARNING;
		else if (level >= AV_LOG_ERROR)   lvl = LOG_ERROR;
		else if (level >= AV_LOG_FATAL)   lvl = LOG_CRITICAL;

		logCb(lvl, "ffmpeg", line);
	}
}

static void sphinxLogCb(void *user_data, err_lvl_t level, const char *fmt, ...)
{
	(void) user_data;

	if (g_loggerCallback && level != ERR_INFOCONT && level >= g_sphinxLogLevel)
	{
		static const int lineSize = 1024;
		char line[lineSize];

		va_list args;
		va_start(args, fmt);
		vsnprintf(line, lineSize, fmt, args);
		va_end(args);

		LogLevel lvl = LOG_INFO;
		switch (level)
		{
			case ERR_DEBUG:    lvl = LOG_DEBUG;    break;
			case ERR_INFO:     lvl = LOG_INFO;     break;
			case ERR_INFOCONT: lvl = LOG_INFO;     break;
			case ERR_WARN:     lvl = LOG_WARNING;  break;
			case ERR_ERROR:    lvl = LOG_ERROR;    break;
			case ERR_FATAL:    lvl = LOG_CRITICAL; break;
			default: lvl = LOG_DEBUG;
		}

		logCb(lvl, "sphinx", line);
	}
}

void setDebugLevel(int level)
{
	int ffmpeg = AV_LOG_WARNING;
	int sphinx = ERR_WARN;

	if (level >= LOG_CRITICAL)
	{
		ffmpeg = AV_LOG_FATAL;
		sphinx = ERR_FATAL;
	}
	else if (level >= LOG_ERROR)
	{
		ffmpeg = AV_LOG_ERROR;
		sphinx = ERR_ERROR;
	}
	else if (level >= LOG_WARNING)
	{
		ffmpeg = AV_LOG_WARNING;
		sphinx = ERR_WARN;
	}
	else if (level >= LOG_INFO)
	{
		ffmpeg = AV_LOG_INFO;

		// don't show INFO logs from sphinx here since there are tons of it
		// and they are more like DEBUG logs anyway
		sphinx = ERR_WARN;
	}
	else
	{
		ffmpeg = AV_LOG_DEBUG;
		sphinx = ERR_DEBUG;
	}

	g_ffmpegLogLevel = ffmpeg;
	g_sphinxLogLevel = sphinx;

	av_log_set_level(ffmpeg);
}

void setLoggerCallback(LoggerCallback cb)
{
	g_loggerCallback = cb;
	av_log_set_callback(ffmpegLogCb);

	err_set_callback(sphinxLogCb, NULL);
	err_set_logfp(NULL);
}
