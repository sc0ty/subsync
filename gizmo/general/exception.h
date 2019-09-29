#ifndef __EXCEPTION_H__
#define __EXCEPTION_H__

#include "current_function.h"

#include <stdexcept>
#include <string>
#include <map>
#include <sstream>


class Exception : public std::exception
{
	public:
		Exception() throw();
		Exception(const std::string &msg) throw();
		Exception(const std::string &msg, const std::string &detail) throw();
		Exception(const Exception &ex) throw();
		virtual ~Exception() throw();

		virtual const char* what() const throw();
		const char *message() const throw();
		const std::map<std::string, std::string> &fields() const throw();

		std::string &operator[] (const std::string &field) throw();
		const std::string &operator[] (const std::string &field) const throw();

		Exception &add(const std::string &field, const std::string &val) throw();

		template <typename T>
			Exception &add(const std::string &field, const T &val) throw()
			{
				std::stringstream ss;
				ss << val;
				return add(field, ss.str());
			}

		Exception &module(const std::string &m) throw();
		Exception &module(const std::string &m1, const std::string &m2,
				const std::string &m3="", const std::string &m4="") throw();
		Exception &code(int code) throw();
		Exception &averror(int errnum) throw();
		Exception &file(const std::string &file) throw();
		Exception &line(const std::string &line) throw();
		Exception &time(double timestamp) throw();

		const std::string &get(const std::string &field) const throw();

	private:
		std::string msg;
		std::map<std::string, std::string> vals;

		mutable std::string str;
		mutable std::string fieldsStr;
};


class ExceptionTerminated : public Exception
{
	public:
		ExceptionTerminated() throw();
		ExceptionTerminated(const Exception &ex) throw();
		virtual ~ExceptionTerminated() throw();
};


std::string makeSourceString(const char *file, int line, const char *func) throw();
std::string ffmpegCodeDescription(int code) throw();

#define EXCEPTION_ADD_SOURCE \
	add("source", makeSourceString(__FILE__, __LINE__, BOOST_CURRENT_FUNCTION))

#define EXCEPTION(msg) \
	Exception(msg).EXCEPTION_ADD_SOURCE

#define EXCEPTION_FFMPEG(msg, val) \
	Exception(msg, ffmpegCodeDescription(val)).averror(val).EXCEPTION_ADD_SOURCE

#endif
