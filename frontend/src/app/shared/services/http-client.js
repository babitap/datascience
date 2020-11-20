import axios from 'axios'
import { config } from '@/app/config'
import store from '@/app/app-state'
import router from '@/app/app-routes'
import { logService } from './log-service'

const httpConfig = {
  baseURL: config.api.baseUrl,
}
const httpClient = axios.create(httpConfig)

const authInterceptor = config => {
  const token = store.getters['user/accessToken']
  if (token != null) {
    config.headers.Authorization = `Bearer ${token}`
    config.headers['Content-Type'] = `application/json`
    //config.headers['Content-Type'] = `application/x-www-form-urlencoded`
  }
  return config
}

const loggerInterceptor = config => {
  /** Add logging here */
  return config
}

/** Adding the request interceptors */
httpClient.interceptors.request.use(authInterceptor)
httpClient.interceptors.request.use(loggerInterceptor)

/** Adding the response interceptors */
httpClient.interceptors.response.use(
  response => {
    if (response.status !== 200) {
      return null
    }
    return response
  },
  error => {
    logService.error(error.response)
    if (error.response.status === 401) {
      store.dispatch('raiseError', 'Unauthorized')
      store.dispatch('user/logout')
      router.push({ path: '/' })
    } else {
      store.dispatch('raiseError', 'Unexpected error happened')
    }
    return Promise.reject(error)
  },
)

export { httpClient }
