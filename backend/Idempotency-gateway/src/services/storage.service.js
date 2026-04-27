const EventEmitter = require('events');

class StorageService {
  constructor() {
    this.cache = new Map();
    this.emitter = new EventEmitter();
    this.TTL = 24 * 60 * 60 * 1000;

    setInterval(() => this.cleanup(), 60 * 60 * 1000);
  }

  get(key) {
    const data = this.cache.get(key);
    if (!data) return null;

    if (Date.now() > data.expiresAt) {
      this.cache.delete(key);
      return null;
    }
    return data;
  }

  set(key, value) {
    const expiration = Date.now() + this.TTL;
    const dataWithExpiry = { ...value, expiresAt: expiration };
    
    this.cache.set(key, dataWithExpiry);
    
    if (value.status === 'COMPLETED') {
      this.emitter.emit(`completed:${key}`, dataWithExpiry);
    }
  }

  has(key) {
    const data = this.cache.get(key);
    if (!data) return false;

    if (Date.now() > data.expiresAt) {
      this.cache.delete(key);
      return false;
    }
    return true;
  }

  waitForCompletion(key) {
    return new Promise((resolve) => {
      this.emitter.once(`completed:${key}`, (data) => {
        resolve(data);
      });
    });
  }

  cleanup() {
    const now = Date.now();
    for (const [key, value] of this.cache.entries()) {
      if (now > value.expiresAt) {
        this.cache.delete(key);
      }
    }
  }
}

module.exports = new StorageService();