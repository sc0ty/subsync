#include "synchro/synchronizer.h"
#include "text/words.h"
#include <emscripten/bind.h>
#include <memory>

namespace em = emscripten;
using namespace std;


static em::val convertCorrelationStats(const CorrelationStats &stats)
{
	em::val res = em::val::object();
	res.set("correlated", stats.correlated);
	res.set("factor", stats.factor);
	res.set("points", stats.points);
	res.set("maxDistance", stats.maxDistance);
	em::val formula = em::val::object();
	formula.set("a", stats.formula.a);
	formula.set("b", stats.formula.b);
	res.set("formula", formula);
	return res;
}

static em::val addSubWord(shared_ptr<Synchronizer> s, float time, float duration,
		const string &text)
{
	const bool correlated = s->addSubWord(Word(text, time, duration));
	if (correlated)
		return convertCorrelationStats(s->correlate());
	else
		return em::val::undefined();
}

static em::val addRefWord(shared_ptr<Synchronizer> s, float time, float duration,
		const string &text)
{
	const bool correlated = s->addRefWord(Word(text, time, duration));
	if (correlated)
		return convertCorrelationStats(s->correlate());
	else
		return em::val::undefined();
}

EMSCRIPTEN_BINDINGS(gizmo_correlator)
{
	em::class_<Synchronizer> sync("Synchronizer");
	sync.smart_ptr_constructor<>("Synchronizer",
			&make_shared<Synchronizer, float, double, float, unsigned, float>);
	sync.function("addSubWord", &addSubWord);
	sync.function("addRefWord", &addRefWord);
	sync.function("addSubtitle", &Synchronizer::addSubtitle);
	sync.function("correlate", &Synchronizer::correlate);

	em::class_<CorrelationStats> stats("CorrelationStats");
	stats.property("correlated", &CorrelationStats::correlated);
	stats.property("factor", &CorrelationStats::factor);
	stats.property("points", &CorrelationStats::points);
	stats.property("maxDistance", &CorrelationStats::maxDistance);
	stats.property("formula", &CorrelationStats::formula);

	em::class_<Line> line("Line");
	line.constructor<float, float>();
	line.property("a", &Line::a);
	line.property("b", &Line::b);
	line.function("getX", &Line::getX);
	line.function("getY", &Line::getY);
	line.function("toString", &Line::toString);
}
