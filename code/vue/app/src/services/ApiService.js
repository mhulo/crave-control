import axios from 'axios'

const apiClient = axios.create({
  //baseURL: 'http://localhost:8888/api',
  baseURL: 'http://' + location.hostname + ':8888/api',
  withCredentials: false, // the default
  headers: { Accept: 'application/json', 'Content-Type': 'application/json' }
})

export default {
   getApi(endpoint) {
    return apiClient.get(endpoint)
  },
  getApi2(endpoint) {
    return apiClient.get(endpoint)
      .then(result => {
        return Promise.resolve(result);
    });
  }
}
