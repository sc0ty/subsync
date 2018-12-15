#include "exception.h"
#include <iomanip>

extern "C"
{
#include <libavutil/error.h>
#include <libavcodec/avcodec.h>
}


using namespace std;


/*** Exception ***/

Exception::Exception() throw()
{}

Exception::Exception(const string &msg) throw() : msg(msg)
{}

Exception::Exception(const string &msg, const string &detail) throw()
{
	this->msg = msg + ": " + detail;
}

Exception::~Exception() throw()
{}

const char* Exception::what() const throw()
{
	if (str.empty())
	{
		str = msg;
		for (auto it = vals.begin(); it != vals.end(); ++it)
			str += string("\n") + it->first + ": " + it->second;
	}

	return str.c_str();
}

const char *Exception::message() const throw()
{
	return msg.c_str();
}

const map<string, string> &Exception::fields() const throw()
{
	return vals;
}

string &Exception::operator[] (const string &field) throw()
{
	str.clear();
	return vals[field];
}

const string &Exception::operator[] (const string &field) const throw()
{
	return get(field);
}

Exception &Exception::add(const string &field, const string &val) throw()
{
	vals[field] = val;
	str.clear();
	return *this;
}

const string &Exception::get(const string &field) const throw()
{
	auto it = vals.find(field);
	if (it == vals.end())
	{
		static string empty;
		return empty;
	}
	return it->second;
}

Exception &Exception::module(const string &m) throw()
{
	string &mod = vals["module"];
	if (!mod.empty())
		mod += '.';

	mod += m;
	return *this;
}

Exception &Exception::module(const string &m1, const string &m2,
		const string &m3, const string &m4) throw()
{
	module(m1);
	module(m2);
	if (!m3.empty()) module(m3);
	if (!m4.empty()) module(m4);

	return *this;
}

Exception &Exception::code(int code) throw()
{
	return add("code", code);
}

Exception &Exception::file(const string &file) throw()
{
	return add("file", file);
}

Exception &Exception::line(const string &line) throw()
{
	return add("line", line);
}

Exception &Exception::time(double timestamp) throw()
{
	double ip, fp;
	fp = modf(timestamp, &ip) * 1000.0;
	unsigned time = ip;

	char buffer[20];
	snprintf(buffer, sizeof(buffer)/sizeof(char), "%02u:%02u:%02u.%03u",
			time / 3600,
			time % 3600 / 60,
			time % 60,
			(unsigned)fp);

	return add("time", buffer);
}


/*** Helper functions ***/

string makeSourceString(const char *file, int line, const char *func)
{
	stringstream ss;
	ss << file << ":" << line << "  " << func;
	return ss.str();
}

string ffmpegCodeDescription(int code)
{
	string res;
	switch (code)
	{
		case AVERROR_BUG:
		case AVERROR_BUG2:
			res = "internal error";
			break;

		case AVERROR_BUFFER_TOO_SMALL:
			res = "buffer too small";
			break;

		case AVERROR_DECODER_NOT_FOUND:
			res = "decoder not found";
			break;

		case AVERROR_DEMUXER_NOT_FOUND:
			res = "demuxer not found";
			break;

		case AVERROR_ENCODER_NOT_FOUND:
			res = "encoder not found";
			break;

		case AVERROR_EOF:
			res = "eof";
			break;

		case AVERROR_FILTER_NOT_FOUND:
			res = "filter not found";
			break;

		case AVERROR_INVALIDDATA:
			res = "invalid data";
			break;

		case AVERROR_MUXER_NOT_FOUND:
			res = "muxer not found";
			break;

		case AVERROR_OPTION_NOT_FOUND:
			res = "option not found";
			break;

		case AVERROR_PROTOCOL_NOT_FOUND:
			res = "protocol not found";
			break;

		case AVERROR_STREAM_NOT_FOUND:
			res = "stream not found";
			break;
	}

	char buffer[1024];
	if (av_strerror(code, buffer, sizeof(buffer)) == 0)
	{
		if (!res.empty())
			res += ": ";
		res += buffer;
	}

	return res;
}
