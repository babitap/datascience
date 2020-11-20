import * as Msal from 'msal'
import { config } from '@/app/config'
import { logService } from './log-service'
import { AuthResult } from '../models/auth-result-enum'

class PasswResetService {
  _app = null;

  constructor () {
    const msalConfig = {
      auth: {
        clientId: config.auth.clientId,
        authority: config.auth.authorities.passwReset,
        validateAuthority: false,
        redirectUri: window.location.origin,
      },
    }

    this._app = new Msal.UserAgentApplication(msalConfig)
  }

  resetPassw () {
    return this._app
      .loginPopup()
      .then(function (loginResponse) {
        return AuthResult.SUCCESS
      })
      .catch(function (error) {
        logService.error(error)
        return AuthResult.ERROR
      })
  }
}

export const passwResetService = new PasswResetService()
