import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/services/ApiService.js'
import WsService from '@/services/WsService.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    socket: {
      'started': false,
      'connected': false
    },
    cards: {},
    devices: {},
    nav: {
      'primary': [
        {
          'name': 'Zones',
          'icon': 'mdi-view-dashboard-outline'
        },
        {
          'name': 'Groups',
          'icon': 'mdi-flip-to-front'
        },
        {
          'name': 'Lights',
          'icon': 'mdi-lightbulb-outline'
        },
        {
          'name': 'Battery',
          'icon': 'mdi-battery-outline'
        }
      ],
      'selected': {
        'primary': {
          'index' : 0,
          'name' : ''
        },
        'secondary': {
          'index' : 0,
          'name' : ['','']
        }
      },
      'popup': false
    }
  },
  mutations: {
    SET_VAL(state, set_data) {
      state.[set_data['key']] = set_data['val']
    },
    SET_SOCKET(state, socket_data) {
      for(let x in socket_data) {
        state.socket.[x] = socket_data[x]
      }
    },
    SET_CARDS(state, cards_data) {
      state.cards = cards_data
    },
    SET_DEVICES(state, devices_data) {
      state.devices = devices_data
    },
    SET_NAV_SELECTED(state, selected_data) {
      state.nav.selected = selected_data
    },
    SET_NAV_POPUP(state, popup_data) {
      state.nav.popup = popup_data
    }
  },
  actions: {
    startSocket({ commit, state }) {
      if (!state.socket.started) {
        commit('SET_SOCKET', { 'started': true })
        WsService.manage()
      }
    },
    updateSocket({ commit }, socket) {
      commit('SET_SOCKET', socket)
    },
    updateCards({ commit, state, dispatch }) {
      ApiService.getApi('/core/cards_conf/')
        .then(response => {
          if (JSON.stringify(response.data) != JSON.stringify(state.cards)) {
            commit('SET_CARDS', response.data)
            dispatch('updateNavSelected', { key: 'primary', val: 0 })
            dispatch('updateNavSelected', { key: 'secondary', val: 0 })
          }
        })
        .catch(error => {
          console.log('api error:', error.response)
        })
    },
    updateDevices({ commit, state }, devices) {
      if (JSON.stringify(devices) != JSON.stringify(state.devices)) {
        commit('SET_DEVICES', devices)
      }
    },
    updateNavSelected({ commit, state, getters }, data) {
      let key = data['key']
      let idx = data['val']
      let selected = state.nav.selected
      selected.[key].index = idx
      selected.[key].name = (key == 'primary') ?
        state.nav.primary[idx].name :
        [
          state.nav.selected.primary.name,
          getters.navSecondary[idx].name
        ]
      commit('SET_NAV_SELECTED', selected)
    },
    updateNavPopup({ commit }, data) {
      commit('SET_NAV_POPUP', data)
    },
    updateVal({ commit }, data) {
      commit('SET_VAL', { 'key' : data.obj,  'val' : data.val })
    },
  },
  getters: {
    deviceByName: state => name => {
      let deviceData = {}
      let deviceCode = name.split('.')
      if (deviceCode[0] in state.devices) {
        if (deviceCode[1] in state.devices[deviceCode[0]]) {
          deviceData = state.devices[deviceCode[0]][deviceCode[1]]
        }
      }
      return deviceData
    },
    navSecondary: state => {
      let things = []
      let primary = state.nav.selected.primary.name
      for (const x in state.cards) {
        if (primary.toLowerCase() in state.cards.[x]) {
          for (const y of state.cards.[x].[primary.toLowerCase()]) {
            if (!(things.includes(y))) { things.push(y) }
          }
        }
      }
      things.sort()
      return things.map((x, idx) => {
        let active = (
          (primary == state.nav.selected.secondary.name[0]) &&
          (x == state.nav.selected.secondary.name[1])
         ) ? 'active' : ''
        return  {
          'name': x,
          'active': active
        }
      })
    }
  }
})
