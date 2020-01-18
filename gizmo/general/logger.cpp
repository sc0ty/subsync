#include "logger.h"
#include "text/utf8.h"
#include <string>
#include <cstdarg>


#define MAX_LOG_SIZE 1024


namespace logger
{

static LoggerCallback g_loggerCallback = NULL;
static int g_logLevel = LOG_WARNING;


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

void setDebugLevel(int level)
{
	g_logLevel = level;
}

void setLoggerCallback(LoggerCallback cb)
{
	g_loggerCallback = cb;
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
