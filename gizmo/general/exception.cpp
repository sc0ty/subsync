#include "exception.h"
#include <iomanip>

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

Exception::Exception(const Exception &ex) throw() : msg(ex.msg), vals(ex.vals)
{}

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


/*** ExceptionTerminated class ***/
ExceptionTerminated::ExceptionTerminated() throw()
{}

ExceptionTerminated::ExceptionTerminated(const Exception &ex) throw()
	: Exception(ex)
{}

ExceptionTerminated::~ExceptionTerminated() throw()
{}


/*** Helper functions ***/

string makeSourceString(const char *file, int line, const char *func) throw()
{
	stringstream ss;
	ss << file << ":" << line << "  " << func;
	return ss.str();
}
