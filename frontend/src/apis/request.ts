import HttpRequest from '@yige/request'
import { message } from 'ant-design-vue'

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()

const baseUrl = configuredBaseUrl
  ? configuredBaseUrl.replace(/\/$/, '')
  : ''

const httpRequest = new HttpRequest({
  baseUrl,
  timeout: 600000,
  errCb: (err) => {
    if (err?.message === 'canceled') {
      return
    }
    message.error(err?.msg || err?.message || '请求失败')
  },
  isValidStatus: (data) => {
    if (typeof data?.success === 'boolean') {
      return data.success
    }
    if (typeof data?.status === 'number') {
      return data.status === 1
    }
    return true
  },
})

export default httpRequest
