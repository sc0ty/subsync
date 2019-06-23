#ifndef __SCOPE_H__
#define __SCOPE_H__

#include <functional>


class ScopeExit
{
	public:
		ScopeExit(std::function<void()> fn) : m_fn(fn)
		{ }

		~ScopeExit()
		{
			m_fn();
		}

		ScopeExit(const ScopeExit&) = delete;
		ScopeExit(ScopeExit&&) = delete;
		ScopeExit& operator= (const ScopeExit&) = delete;
		ScopeExit& operator= (ScopeExit&&) = delete;

	private:
		std::function<void()> m_fn;
};

#endif
