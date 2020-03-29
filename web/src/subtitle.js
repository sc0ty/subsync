export default class Subtitles {

  constructor() {
    this.header = null;
    this.events = [];
  }

  addSubtitle(s) {
    if (s.text.startsWith('[Script Info]')) {
      this.header = s.text;
    } else {
      this.events.push({
        start: s.start,
        end: s.end,
        text: stripTimeCode(s.text) || s.text,
      });
    }
  }

  getSynchronizedSubtitles(formula, format) {
    const formatters = {
      'ass': AdvancedSubStation,
      'srt': SubRip,
      'tmp': TMP,
    }

    const Formatter = formatters[format || 'srt'];
    if (!Formatter) {
      throw {
        message: 'Invalid subtitle format',
        format: format,
      }
    }

    const fmt = new Formatter();
    const res = fmt.parseHeader ? fmt.parseHeader(this.header) : [];
    for (const ev of this.events) {
      const start = Math.max(formula.a * ev.start + formula.b, 0);
      const end = Math.max(formula.a * ev.end + formula.b, 0);
      res.push(fmt.parseEvent(start, end, ev.text));
    }
    return res;
  }

  /*getSortedSubtitles() {
    return this.events.sort((x, y) => {
      if (x.start < y.start) {
        return -1;
      } else if (x.start > y.start) {
        return 1;
      } else {
        return 0;
      }
    });
  }*/

  getMaxChange(formula) {
    if (formula && this.events.length > 0) {
      const getChange = x => Math.abs(formula.a * x + formula.b - x);
      const first = this.events[0].start;
      const last = this.events[this.events.length - 1].end;
      return Math.max(getChange(first), getChange(last));
    }
  }
}

class AdvancedSubStation {

  parseHeader(header) {
    return [ header ];
  }

  parseEvent(start, end, text) {
    return [
      'Dialogue: 0',
      AdvancedSubStation.formatTime(start),
      AdvancedSubStation.formatTime(end),
      text + '\r\n'
    ].join(',');
  }

  static formatTime(t) {
    const h = Math.floor(t / 3600).toString();
    const mm = Math.floor(t / 60 % 60).toString().padStart(2, '0');
    const ss = Math.floor(t % 60).toString().padStart(2, '0');
    const ff = Math.floor(t * 100 % 100).toString().padStart(2, '0');
    return `${h}:${mm}:${ss}.${ff}`;
  }
}

class SubRip {

  constructor() {
    this.cnt = 1;
    this.formatter = makeTagFormatter({
      'n': '\r\n',
      'N': '\r\n',
      'h': ' ',
      'b1': '<b>', 'b0': '</b>',
      'i1': '<i>', 'i0': '</i>',
      'u1': '<u>', 'u0': '</u>',
      's1': '<s>', 's0': '</s>',
    });
  }

  parseEvent(start, end, text) {
    return [
      this.cnt++,
      SubRip.formatTime(start) + ' --> ' + SubRip.formatTime(end),
      this.formatter(stripPrefixes(text)) + '\r\n\r\n',
    ].join('\r\n');
  }

  static formatTime(t) {
    const hh = Math.floor(t / 3600).toString().padStart(2, '0');
    const mm = Math.floor(t / 60 % 60).toString().padStart(2, '0');
    const ss = Math.floor(t % 60).toString().padStart(2, '0');
    const fff = Math.floor(t * 1000 % 1000).toString().padStart(3, '0');
    return `${hh}:${mm}:${ss},${fff}`;
  }
}

class TMP {

  constructor() {
    this.formatter  = makeTagFormatter({
      'n': '|',
      'N': '|',
      'h': ' ',
      'b1': '<b>', 'b0': '</b>',
      'i1': '<i>', 'i0': '</i>',
      'u1': '<u>', 'u0': '</u>',
      's1': '<s>', 's0': '</s>',
    });
  }

  parseEvent(start, end, text) {
    return [
      Math.floor(start / 3600),
      Math.floor(start / 60 % 60).toString().padStart(2, '0'),
      Math.floor(start % 60).toString().padStart(2, '0'),
      this.formatter(stripPrefixes(text)) + '\r\n',
    ].join(':');
  }
}

function makeTagFormatter(tagMap) {
  const regex = /(\\)(N|n|h)|(\{)(\\[^\}]*)(})/g;
  return function(line) {
    return line.replace(regex, (_, simpleSlash, simple, complexBr1, complex, complexBr2) => {
      if (simple) {
        return tagMap[simple] || '';
      } else if (complex) {
        return complex.split('\\').map(tag => tagMap[tag] || '').join('');
      }
      return '';
    });
  }
}

function stripTimeCode(line) {
  const c1 = line.indexOf(',');
  if (c1 != null) {
    const c2 = line.indexOf(',', c1 + 1);
    if (c2) {
      return line.substring(c2 + 1);
    }
  }
}

function stripPrefixes(line) {
  let i = 0;
  let commas = 0;
  for (const c of line) {
    i++;
    if (c === ',') {
      if (++commas === 6) {
        return line.substring(i);
      }
    }
  }
  return line;
}
