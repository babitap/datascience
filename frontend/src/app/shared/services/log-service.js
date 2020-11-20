class LogService {
  constructor () {
    this.initLogger()
  }

  /**
   * @description Initializing the configuration
   */
  initLogger () {
    if (process.env.NODE_ENV !== 'production') {
      this.log = console.log.bind(console)
      this.debug = console.debug.bind(console)
      this.info = console.info.bind(console)
      this.warn = console.warn.bind(console)
      this.error = console.error.bind(console)
    } else {
      this.log = this.debug = this.info = this.warn = this.error = () => {}
    }
  }
}

export const logService = new LogService()
