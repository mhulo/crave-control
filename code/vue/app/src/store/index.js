import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/services/ApiService.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    cards: {},
    devices: {}
  },
  mutations: {
    SET_CARDS(state, cards_data) {
      state.cards = cards_data
    },
    SET_DEVICES(state, devices_data) {
      state.devices = devices_data
    }
  },
  actions: {
    updateCards({ commit, state }) {
      ApiService.getApi('/core/cards_conf/')
        .then(response => {
          if (JSON.stringify(response.data) != JSON.stringify(state.cards)) {
            commit('SET_CARDS', response.data)
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
    }
  },
  getters: {
    getDeviceByName: state => name => {
      var deviceData = {}
      var deviceCode = name.split('.')
      if (deviceCode[0] in state.devices) {
        if (deviceCode[1] in state.devices[deviceCode[0]]) {
          deviceData = state.devices[deviceCode[0]][deviceCode[1]]
        }
      }
      return deviceData
    }
  }
})
