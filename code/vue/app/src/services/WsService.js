import store from '@/store'

export default {
  wsConn: null,
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

    console.log('attempting websocket connection..')
    this.wsConn = new WebSocket(wsUrl)

    // connection is open
    this.wsConn.onopen = ((ev) => {  
      console.log('websocket interface connected')
    })

    // message received on websocket from server
    // dispatch action to update state with new data
    this.wsConn.onmessage = ((ev) => {

      if (ev.data == 'pong') {
        //console.log(ev.data+' received');
      } 
      else {
        let data = JSON.parse(ev.data)
        if ('message' in data) {
          console.log('message: ' + ev.data);
        }
        else {
          store.dispatch('updateDevices', data)
        }
      }
    })

    this.wsConn.onerror = ((ev) => {
      console.log('error on websocket interface')
      this.wsConn = null
    })

    this.wsConn.onclose = ((ev) => {
      console.log('disconnected from websocket interface')
      this.wsConn = null
    })
  },
  reConnect() {
    if (this.wsConn == null) {
      this.connect()
    }
    else if (this.wsConn.readyState != 1) {
      this.wsConn == null
      this.connect()
    }
    else {
      this.wsConn.send('ping')
    }
    setTimeout(() => { this.reConnect() }, 5000)
  }
}
