#ifndef __LOGGER_H__
#define __LOGGER_H__

#include <functional>


enum LogLevel
{
	LOG_NOTSET   = 0,
	LOG_DEBUG    = 10,
	LOG_INFO     = 20,
	LOG_WARNING  = 30,
	LOG_ERROR    = 40,
	LOG_CRITICAL = 50
};

typedef std::function<void (int, const char*, const char*)> LoggerCallback;

void setDebugLevel(int level);
void setLoggerCallback(LoggerCallback cb);

#endif
