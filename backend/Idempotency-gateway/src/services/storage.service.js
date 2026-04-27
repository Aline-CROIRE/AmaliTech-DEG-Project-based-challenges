const EventEmitter = require('events');

class StorageService {
  constructor() {
    this.cache = new Map();
    this.emitter = new EventEmitter();
  }

  get(key) {
    return this.cache.get(key);
  }

  set(key, value) {
    this.cache.set(key, value);
    if (value.status === 'COMPLETED') {
      this.emitter.emit(`completed:${key}`, value);
    }
  }

  has(key) {
    return this.cache.has(key);
  }

  waitForCompletion(key) {
    return new Promise((resolve) => {
      this.emitter.once(`completed:${key}`, (data) => {
        resolve(data);
      });
    });
  }
}

module.exports = new StorageService();