import axios from 'axios'
import qs from 'qs'

export const ajax = axios.create({
  headers: {
    source: 'h5',
    icode: 'J2F9901156E6358B0',
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  /**
   * 对请求的参数进行格式化处理
   */
  transformRequest: function (data, headers) {
    return qs.stringify(data)
  },
  // 携带上次cookie
  withCredentials: true
})
ajax.interceptors.request.use(function (config) {
  // 请求发起之前做些什么
  console.log('请求拦截到了')
  window.app.$toast.loading({
    message: '加载中...',
    forbidClick: true,
    loadingType: 'spinner'
  })
  return config
}, function (error) {
  // 对请求错误做些什么
  window.app.$toast.clear()
  return Promise.reject(error)
})
ajax.interceptors.response.use(function (response) {
  // 对数据响应做点什么
  console.log('响应拦截到了')
  window.app.$toast.clear()
  return response
}, function (error) {
  // 对响应错误做点什么
  if (error.response.status === 401) {
    window.app.$notify({
      message: '未登录，即将跳转到登录页面',
      type: 'danger'
    })
    window.app.$router.replace({name: 'accountlogin'})
  } else if (error.response.status === 500) {
    // window.alert('服务器正忙')
    window.app.$notify({
      message: '服务器正忙',
      type: 'danger'
    })
  } else if (error.response.status === 400) {
    const data = error.response.data
    let msg = data.error_msg ? data.error_msg : '参数错误'
    if (data.error_list) {
      const keys = Object.keys(data.error_list)
      const errObj = data.error_list[keys[0]][0]
      msg = `${errObj.message},${errObj.code}`
      window.app.$notify(msg)
    }
  }
  window.app.$toast.clear()
  return Promise.reject(error)
})
