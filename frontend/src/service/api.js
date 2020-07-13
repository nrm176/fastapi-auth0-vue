import axios from 'axios'
import store from '@/store'
import { getInstance } from '../auth/index'

const api = axios.create({
  baseURL: process.env.VUE_APP_ROOT_API,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  }
})

// common pre-processing
api.interceptors.request.use(async function (config) {
  const authService = getInstance()
  // if exists in local storege, put it on header
  // const token = localStorage.getItem('access_112341325')
  const token = await authService.getTokenSilently()
  if (token) {
    config.headers.Authorization = 'Bearer ' + token
    return config
  }
  return config
}, function (error) {
  return Promise.reject(error)
})

// common error handling
api.interceptors.response.use(function (response) {
  return response
}, function (error) {
  const status = error.response ? error.response.status : 500

  // show message depending on the type of status
  let message
  if (status === 400) {
    // validation failed
    const messages = [].concat.apply([], Object.values(error.response.data))
    console.log(messages)
  } else if (status === 401) {
    // auth error
    const token = localStorage.getItem('access')
    if (token != null) {
      message = 'ログイン有効期限切れ'
    } else {
      message = '認証エラー'
    }
    console.log(message)
    store.dispatch('auth/logout')
    store.dispatch('message/setErrorMessage', { message: message })
  } else if (status === 403) {
    // permission error
    message = '権限エラーです。'
    store.dispatch('message/setErrorMessage', { message: message })
  } else {
    // unexpected error
    message = '想定外のエラーです。'
    store.dispatch('message/setErrorMessage', { message: message })
  }
  return Promise.reject(error)
})

export default api
