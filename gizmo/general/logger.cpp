#include "logger.h"
#include "text/utf8.h"
#include <pocketsphinx/err.h>
#include <pocketsphinx.h>
#include <string>
#include <cstdarg>

extern "C"
{
#include <libavformat/avformat.h>
}


#define MAX_LOG_SIZE 1024


namespace logger
{

static LoggerCallback g_loggerCallback = NULL;
static int g_logLevel = LOG_WARNING;
static int g_ffmpegLogLevel = AV_LOG_WARNING;
static int g_sphinxLogLevel = ERR_WARN;


void log(LogLevel level, const char *module, const char *msg)
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
	if (g_loggerCallback && level <= g_ffmpegLogLevel)
	{
		char line[MAX_LOG_SIZE];
		static int printPrefix = 1;
		av_log_format_line(avcl, level, fmt, vl, line, MAX_LOG_SIZE, &printPrefix);

		LogLevel lvl = LOG_DEBUG;
		if      (level >= AV_LOG_DEBUG)   lvl = LOG_DEBUG;
		else if (level >= AV_LOG_INFO)    lvl = LOG_INFO;
		else if (level >= AV_LOG_WARNING) lvl = LOG_WARNING;
		else if (level >= AV_LOG_ERROR)   lvl = LOG_ERROR;
		else if (level >= AV_LOG_FATAL)   lvl = LOG_CRITICAL;

		log(lvl, "ffmpeg", line);
	}
}

static void sphinxLogCb(void *user_data, err_lvl_t level, const char *fmt, ...)
{
	(void) user_data;

	if (g_loggerCallback && level >= g_sphinxLogLevel)
	{
		char line[MAX_LOG_SIZE];
		va_list args;
		va_start(args, fmt);
		vsnprintf(line, MAX_LOG_SIZE, fmt, args);
		va_end(args);

		LogLevel lvl = LOG_INFO;
		switch (level)
		{
			case ERR_DEBUG:    lvl = LOG_DEBUG;    break;
			case ERR_INFO:     lvl = LOG_DEBUG;    break;
			case ERR_WARN:     lvl = LOG_WARNING;  break;
			case ERR_ERROR:    lvl = LOG_ERROR;    break;
			case ERR_FATAL:    lvl = LOG_CRITICAL; break;
			default: lvl = LOG_DEBUG;
		}

		log(lvl, "sphinx", line);
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
		ffmpeg = AV_LOG_VERBOSE;

		// don't show INFO logs from sphinx here since there are tons of it
		// and they are more like DEBUG logs anyway
		sphinx = ERR_WARN;
	}
	else
	{
		ffmpeg = AV_LOG_DEBUG;
		sphinx = ERR_DEBUG;
	}

	g_logLevel = level;
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

static void vlog(LogLevel level, const char *module, const char *fmt, va_list args)
{
	if (level >= g_logLevel)
	{
		char line[MAX_LOG_SIZE];
		vsnprintf(line, MAX_LOG_SIZE, fmt, args);
		const std::string m = std::string("gizmo.") + module;
		log(level, m.c_str(), line);
	}
}

void debug(const char *module, const char *fmt, ...)
{
	va_list va;
	va_start(va, fmt);
	vlog(LOG_DEBUG, module, fmt, va);
	va_end(va);
}

void info(const char *module, const char *fmt, ...)
{
	va_list va;
	va_start(va, fmt);
	vlog(LOG_INFO, module, fmt, va);
	va_end(va);
}

void warn(const char *module, const char *fmt, ...)
{
	va_list va;
	va_start(va, fmt);
	vlog(LOG_WARNING, module, fmt, va);
	va_end(va);
}

void error(const char *module, const char *fmt, ...)
{
	va_list va;
	va_start(va, fmt);
	vlog(LOG_ERROR, module, fmt, va);
	va_end(va);
}

}
