#ifndef __MEDIA_LOGGER_H__
#define __MEDIA_LOGGER_H__

#include "general/logger.h"


namespace media
{
void setDebugLevel(int level);
void setLoggerCallback(logger::LoggerCallback cb);
}

#endif
