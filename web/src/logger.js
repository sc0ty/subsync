export default class Logger {

  constructor(parentPrefix, prefix) {
    this.parentPrefix = parentPrefix;
    this.prefix = prefix;
    this.children = [];
    this.updatePrefix();
  }

  get(prefix) {
    const child = new Logger(this.getPrefix(), prefix);
    this.children.push(child);
    return child;
  }

  setPrefix(prefix) {
    this.prefix = prefix;
    this.updatePrefix();
  }

  setParentPrefix(parentPrefix) {
    this.parentPrefix = parentPrefix;
    this.updatePrefix();
  }

  getPrefix() {
    const prefix = [];
    if (this.parentPrefix) {
      prefix.push(this.parentPrefix);
    }
    if (this.prefix) {
      prefix.push(this.prefix);
    }
    return prefix.join(' ');
  }

  updatePrefix() {
    const prefix = this.getPrefix();
    this.log = Function.prototype.bind.call(console.log, console, prefix);
    this.info = Function.prototype.bind.call(console.info, console, prefix);
    this.warn = Function.prototype.bind.call(console.warn, console, prefix);
    this.error = Function.prototype.bind.call(console.error, console, prefix);
    for (let child of this.children) {
      child.setParentPrefix(prefix);
    }
  }
}

Logger.logger = new Logger(null, '[Main]');
