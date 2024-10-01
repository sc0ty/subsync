#ifndef __UTF8_H__
#define __UTF8_H__

#include <string>
#include <cstdint>


class Utf8
{
	public:
		class iterator
		{
			public:
				iterator();
				iterator(const std::string &str);
				iterator(const char *str);

				uint32_t operator* () const;

				iterator &operator++ ();
				iterator &operator-- ();

				iterator operator++ (int);
				iterator operator-- (int);

				iterator &operator+= (size_t len);
				iterator &operator-= (size_t len);

				bool operator== (const iterator &it) const;
				bool operator!= (const iterator &it) const;

				// codepoints left to the end of the string
				size_t size() const;

				// current codepoint size
				unsigned cpSize() const;

				uint32_t toLower() const;
				uint32_t toUpper() const;

				bool isLower() const;
				bool isUpper() const;

				const char *getRawData() const;
				unsigned getiteratorSize() const;

				static const uint32_t invalid;

			private:
				const uint8_t *m_ptr;
		};

	public:
		static std::basic_string<uint32_t> decode(const std::string &str);
		static std::string encode(uint32_t codePoint);
		static std::string encode(const std::basic_string<uint32_t> &codePoints);

		static std::string toLower(const std::string &str);
		static std::string toUpper(const std::string &str);

		static std::string reverse(const std::string &str);

		static std::string substr(const iterator &begin, const iterator &end);

		static size_t size(const std::string &str);
		static size_t size(const char *str);

		static bool validate(const std::string &str);
		static bool validate(const char *str);

		static std::string escape(const std::string &str);
		static std::string escape(const char *str);
};

#endif
