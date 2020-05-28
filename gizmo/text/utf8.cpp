#include "utf8.h"
#include "utf8case.h"

#define IS1B(cp)    (((cp) & 0x80) == 0x00)
#define IS2B(cp)    (((cp) & 0xe0) == 0xc0)
#define IS3B(cp)    (((cp) & 0xf0) == 0xe0)
#define IS4B(cp)    (((cp) & 0xf8) == 0xf0)
#define ISCNT(cp)   (((cp) & 0xc0) == 0x80)

#define CNT(b, pos) (((b) & 0x3f) << ((pos) * 6))

#define ENC_CNT(x, no)  (((x>>(no*6)) & 0x3f) | 0x80)

#define DECODE2B(p)  ((((p)[0] & 0x1f) << 6) | CNT((p)[1], 0))
#define DECODE3B(p)  ((((p)[0] & 0x0f) << 12) | CNT((p)[1], 1) | CNT((p)[2], 0))
#define DECODE4B(p)  ((((p)[0] & 0x07) << 18) | CNT((p)[1], 2) | CNT((p)[2], 1) | CNT((p)[3], 0))

using namespace std;


const uint32_t Utf8::iterator::invalid = 0xffffffff;

static uint32_t lowerToUpper(uint32_t lower, uint32_t defval=Utf8::iterator::invalid);
static uint32_t upperToLower(uint32_t upper, uint32_t defval=Utf8::iterator::invalid);


Utf8::iterator::iterator() : m_ptr(NULL)
{}

Utf8::iterator::iterator(const string &str) : m_ptr((const uint8_t*)str.c_str())
{}

Utf8::iterator::iterator(const char *str) : m_ptr((const uint8_t*)str)
{}

uint32_t Utf8::iterator::operator* () const
{
	if (m_ptr == NULL)
		return 0;
	if (IS1B(m_ptr[0]))
		return m_ptr[0];
	if (IS2B(m_ptr[0]) && ISCNT(m_ptr[1]))
		return DECODE2B(m_ptr);
	if (IS3B(m_ptr[0]) && ISCNT(m_ptr[1]) && ISCNT(m_ptr[2]))
		return DECODE3B(m_ptr);
	if (IS4B(m_ptr[0]) && ISCNT(m_ptr[1]) && ISCNT(m_ptr[2])  && ISCNT(m_ptr[3]))
		return DECODE4B(m_ptr);

	return invalid;
}

Utf8::iterator &Utf8::iterator::operator++ ()
{
	if (m_ptr)
		m_ptr++;

	while (m_ptr && ISCNT(*m_ptr))
		m_ptr++;

	return *this;
}

Utf8::iterator &Utf8::iterator::operator-- ()
{
	if (m_ptr)
		m_ptr--;

	while (m_ptr && ISCNT(*m_ptr))
		m_ptr--;

	return *this;
}

Utf8::iterator Utf8::iterator::operator++ (int)
{
	iterator cp = *this;
	operator++();
	return cp;
}

Utf8::iterator Utf8::iterator::operator-- (int)
{
	iterator cp = *this;
	operator--();
	return cp;
}

Utf8::iterator &Utf8::iterator::operator+= (size_t len)
{
	for (; len > 0; len--)
		operator++();

	return *this;
}

Utf8::iterator &Utf8::iterator::operator-= (size_t len)
{
	for (; len > 0; len--)
		operator--();

	return *this;
}

size_t Utf8::iterator::size() const
{
	if (m_ptr == NULL)
		return 0;

	return Utf8::size((char*) m_ptr);
}

unsigned Utf8::iterator::cpSize() const
{
	if (m_ptr == NULL)
		return 0;
	if (IS2B(*m_ptr))
		return 2;
	if (IS3B(*m_ptr))
		return 3;
	if (IS4B(*m_ptr))
		return 4;
	return 1;
}

uint32_t Utf8::iterator::toLower() const
{
	uint32_t cp = operator*();
	return upperToLower(cp, cp);
}

uint32_t Utf8::iterator::toUpper() const
{
	uint32_t cp = operator*();
	return lowerToUpper(cp, cp);
}

bool Utf8::iterator::isLower() const
{
	return lowerToUpper(operator*()) != Utf8::iterator::invalid;
}

bool Utf8::iterator::isUpper() const
{
	return upperToLower(operator*()) != Utf8::iterator::invalid;
}

const char *Utf8::iterator::getRawData() const
{
	return (const char*)m_ptr;
}

unsigned Utf8::iterator::getiteratorSize() const
{
	if (m_ptr)
	{
		if (IS1B(*m_ptr)) return 1;
		if (IS2B(*m_ptr)) return 2;
		if (IS3B(*m_ptr)) return 3;
		if (IS4B(*m_ptr)) return 4;
	}
	return 0;
}

basic_string<uint32_t> Utf8::decode(const string &str)
{
	basic_string<uint32_t> res;
	for (Utf8::iterator it(str); *it; ++it)
		res += *it;

	return res;
}

string Utf8::encode(uint32_t codePoint)
{
	string res;
	if (codePoint <= 0x7f)
	{
		res.reserve(1);
		res = (char)codePoint;
	}
	else if (codePoint <= 0x7ff)
	{
		res.reserve(2);
		res = (char)((codePoint >> 6) | 0xc0);
		res += (char)ENC_CNT(codePoint, 0);
	}
	else if (codePoint <= 0xffff)
	{
		res.reserve(3);
		res = (char)((codePoint >> 12) | 0xe0);
		res += (char)ENC_CNT(codePoint, 1);
		res += (char)ENC_CNT(codePoint, 0);
	}
	else if (codePoint <= 0x1fffff)
	{
		res.reserve(4);
		res = (char)((codePoint >> 18) | 0xf0);
		res += (char)ENC_CNT(codePoint, 2);
		res += (char)ENC_CNT(codePoint, 1);
		res += (char)ENC_CNT(codePoint, 0);
	}

	return res;
}

string Utf8::encode(const basic_string<uint32_t> &codePoints)
{
	string res;
	for (uint32_t codePoint : codePoints)
		res += encode(codePoint);

	return res;
}

string Utf8::toLower(const string &str)
{
	string res;
	for (Utf8::iterator it(str); *it; ++it)
		res += Utf8::encode(it.toLower());

	return res;
}

string toUpper(const string &str)
{
	string res;
	for (Utf8::iterator it(str); *it; ++it)
		res += Utf8::encode(it.toUpper());

	return res;
}

uint32_t lowerToUpper(uint32_t lower, uint32_t defval)
{
	if (lower < g_caseGroup1[0].lower && lower < g_caseGroup1[0].upper &&
		lower < g_caseGroup2[0].lower && lower < g_caseGroup2[0].upper &&
		lower < g_caseSingle[0].lower && lower < g_caseSingle[0].upper)
	{
		if (lower >= 'a' && lower <= 'z')
			return lower - 'a' + 'A';
		else
			return defval;
	}

	for (unsigned i = 0; i < sizeof(g_caseGroup1) / sizeof(Utf8CaseGroup); i++)
	{
		const Utf8CaseGroup &gr = g_caseGroup1[i];
		if (lower >= gr.lower && lower < gr.lower + gr.count)
			return gr.upper + (lower - gr.lower);

		if (lower > gr.lower)
			break;
	}

	for (unsigned i = 0; i < sizeof(g_caseGroup2) / sizeof(Utf8CaseGroup); i++)
	{
		const Utf8CaseGroup &gr = g_caseGroup2[i];
		if ((lower & 1) == (gr.lower & 1) && lower >= gr.lower && lower < gr.lower + 2*gr.count)
			return gr.upper + (lower - gr.lower);

		if (lower > gr.lower)
			break;
	}

	for (unsigned i = 0; i < sizeof(g_caseSingle) / sizeof(Utf8CaseMapping); i++)
	{
		const Utf8CaseMapping &cm = g_caseSingle[i];
		if (cm.lower == lower)
			return cm.upper;

		if (lower > cm.lower)
			break;
	}

	return defval;
}

uint32_t upperToLower(uint32_t upper, uint32_t defval)
{
	if (upper < g_caseGroup1[0].lower && upper < g_caseGroup1[0].upper &&
		upper < g_caseGroup2[0].lower && upper < g_caseGroup2[0].upper &&
		upper < g_caseSingle[0].lower && upper < g_caseSingle[0].upper)
	{
		if (upper >= 'A' && upper <= 'Z')
			return upper - 'A' + 'a';
		else
			return defval;
	}

	for (unsigned i = 0; i < sizeof(g_caseGroup1) / sizeof(Utf8CaseGroup); i++)
	{
		const Utf8CaseGroup &gr = g_caseGroup1[i];
		if (upper >= gr.upper && upper < gr.upper + gr.count)
			return gr.lower + (upper - gr.upper);
	}

	for (unsigned i = 0; i < sizeof(g_caseGroup2) / sizeof(Utf8CaseGroup); i++)
	{
		const Utf8CaseGroup &gr = g_caseGroup2[i];
		if ((upper & 1) == (gr.upper & 1) && upper >= gr.upper && upper < gr.upper + 2*gr.count)
			return gr.lower + (upper - gr.upper);
	}

	for (unsigned i = 0; i < sizeof(g_caseSingle) / sizeof(Utf8CaseMapping); i++)
	{
		const Utf8CaseMapping &cm = g_caseSingle[i];
		if (cm.upper == upper)
			return cm.lower;
	}

	return defval;
}

string Utf8::reverse(const string &str)
{
	string res;
	res.reserve(str.size());

	const auto cps = decode(str);
	const size_t length = cps.size();

	for (size_t i = 0; i < length; i++)
		res += encode(cps[length - i - 1]);

	return res;
}

string Utf8::substr(const Utf8::iterator &begin, const Utf8::iterator &end)
{
	return string(begin.getRawData(), 0, end.getRawData() - begin.getRawData());
}

size_t Utf8::size(const std::string &str)
{
	return size(str.c_str());
}

size_t Utf8::size(const char *str)
{
	size_t sz = 0;

	while (*str)
	{
		if (!ISCNT(*str)) sz++;
		str++;
	}

	return sz;
}

bool Utf8::validate(const string &str)
{
	return Utf8::validate(str.c_str());
}

bool Utf8::validate(const char *str)
{
	const char *p = str;
	while (*p)
	{
		if (IS1B(p[0]))
			p += 1;
		else if (IS2B(p[0]) && ISCNT(p[1]) && (DECODE2B(p) >= 0x80))
			p += 2;
		else if (IS3B(p[0]) && ISCNT(p[1]) && ISCNT(p[2]) && (DECODE3B(p) >= 0x800))
			p += 3;
		else if (IS4B(p[0]) && ISCNT(p[1]) && ISCNT(p[2]) && ISCNT(p[3]) && (DECODE4B(p) >= 0x10000))
			p += 4;
		else
			return false;
	}

	return true;
}

string Utf8::escape(const std::string &str)
{
	return Utf8::escape(str.c_str());
}

string Utf8::escape(const char *str)
{
	string res;
	for (Utf8::iterator it(str); *it; ++it)
	{
		uint32_t cp = *it;
		if (cp == Utf8::iterator::invalid)
			cp = 0xfffd;

		res += Utf8::encode(cp);
	}

	return res;
}

