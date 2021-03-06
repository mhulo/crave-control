import store from '@/store'

export default {
  ws: null,
  count: 0,
  connect() {
    let wsParams = {}
    wsParams['id'] = Date.now()
    wsParams['host'] = location.hostname
    if (location.protocol == 'https:') {
      wsParams['protocol'] = 'wss'
      wsParams['port'] = ''
    }
    else {
      wsParams['protocol'] = 'ws'
      wsParams['port'] = ':8888'
    }

    let wsUrl = (
      wsParams['protocol'] + '://' + 
      wsParams['host'] +
      wsParams['port'] + '/api/core/wss/' +
      wsParams['id'] + '/'
    )

    console.log('websocket connecting..')
    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = ((ev) => {
      console.log('websocket connected')
      store.dispatch('updateSocket', { 'connected': true })
    })

    this.ws.onmessage = ((ev) => {
      this.handleMessage(ev.data)
    })

    this.ws.onclose = ((ev) => {
      console.log('websocket disconnected - code' + ev.code)
      store.dispatch('updateSocket', { 'connected': false })
      setTimeout(() => { this.connect() }, 3000)
    })

    this.ws.onerror = ((ev) => {
      console.log('websocket error')
      this.ws.close()
    })
  },
  handleMessage(data) {
    if (data == 'pong') {
      //pass
    }
    else {
      let jsonData = JSON.parse(data)
      if ('message' in jsonData) {
        console.log('message: ' + jsonData['message']);
      }
      else {
        // message received on websocket from server
        // dispatch action to update state with new data
        store.dispatch('updateDevices', jsonData)
      }
    }
  },
  manage() {
    if (this.ws == null) {
      this.connect()
    }
    else if (this.ws.readyState != 1) {
      this.connect()
    }

    if (this.count > 9) {
      this.count = 0
      this.ws.send('ping')
    }

    setTimeout(() => { this.manage() }, 3000)
  },
  getState() {
    return (this.ws == null)? null : this.ws.readyState
  }
}
