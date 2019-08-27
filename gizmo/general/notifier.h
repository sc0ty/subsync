#ifndef __GENERAL_NOTIFIER_H__
#define __GENERAL_NOTIFIER_H__

#include <functional>
#include <vector>


template <typename... T>
class Notifier
{
public:
	typedef std::function<void (T...)> Listener;

	void addListener(Listener listener)
	{
		m_listeners.push_back(listener);
	}

	bool removeListener(Listener listener=nullptr)
	{
		if (listener == nullptr)
		{
			const bool hasListeners = !m_listeners.empty();
			m_listeners.clear();
			return hasListeners;
		}

		for (typename std::vector<Listener>::iterator it = m_listeners.begin();
				it != m_listeners.end(); ++it)
		{
			if (it->template target<Listener>() == listener.template target<Listener>())
			{
				m_listeners.erase(it);
				return true;
			}
		}

		return false;
	}

	void notify(T... args)
	{
		for (Listener listener : m_listeners)
			listener(args...);
	}

private:
	std::vector<Listener> m_listeners;
};

#endif
