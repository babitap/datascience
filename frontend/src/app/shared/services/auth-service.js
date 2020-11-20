import * as Msal from 'msal'
import { config } from '@/app/config'
import { logService } from './log-service'
import { AuthResult } from '../models/auth-result-enum'

/**
 * @description Represents functionality for user authentication
 */
class AuthService {
  _app = null;

  constructor () {
    const msalConfig = {
      auth: {
        clientId: config.auth.clientId,
        authority: config.auth.authorities.signin,
        validateAuthority: false,
        redirectUri: window.location.origin,
        postLogoutRedirectUri: window.location.origin,
      },
      cache: {
        cacheLocation: 'localStorage',
        storeAuthStateInCookie: false, // disable cookie for msal since cookies created by msal are NOT httpOnly and Secure
      },
    }

    this._app = new Msal.UserAgentApplication(msalConfig)
  }

  /**
   * @description User's signin functionality
   */
  signIn () {
    const request = {
      scopes: config.auth.b2cScopes,
    }

    const self = this
    return this._app
      .loginPopup(request)
      .then(function (loginResponse) {
        const user = self._app.getAccount()
        return user ? AuthResult.SUCCESS : AuthResult.ERROR
      })
      .catch(function (error) {
        if (error.errorMessage.indexOf('AADB2C90118') >= 0) {
          return AuthResult.PASSW_RESET
        }
        return AuthResult.ERROR
      })
  }

  /**
   * @description User's signout functionality
   */
  logout () {
    this._app.logout()
  }

  /**
   * @description Gets a token
   */
  getToken () {
    const tokenRequest = {
      scopes: config.auth.b2cScopes,
    }

    // eslint-disable-next-line handle-callback-err
    return this._app.acquireTokenPopup(tokenRequest)
      .then(function (tokenResponse) {
        console.log(tokenResponse)
        return tokenResponse
      })
      .catch(function (error) {
        logService.error('Failed token acquisition', error)
      })
  }
}

export const authService = new AuthService()
