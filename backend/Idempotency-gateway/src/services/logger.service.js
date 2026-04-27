class LoggerService {
  constructor() {
    this.logs = [];
  }

  log(event) {
    const entry = {
      timestamp: new Date().toISOString(),
      ...event
    };
    this.logs.push(entry);
    console.log(`[AUDIT LOG] ${JSON.stringify(entry)}`);
  }

  getLogs() {
    return this.logs;
  }
}

module.exports = new LoggerService();