import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/services/ApiService.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    cards: {},
    devices: {},
    navData: [
      {
        'text': 'Zones',
        'icon': 'mdi-floor-plan',
        'active': 'active'
      },
      {
        'text': 'Groups',
        'icon': 'mdi-rhombus-split',
        'active': ''
      },
      {
        'text': 'Lights',
        'icon': 'mdi-lightbulb-outline',
        'active': ''
      },
      {
        'text': 'Battery',
        'icon': 'mdi-battery-outline',
        'active': ''
      }
    ],
    popupData: {
      'show': false,
      'source' : null,
      'key' : null
    }
  },
  mutations: {
    SET_VAL(state, set_data) {
      state.[set_data['obj']] = set_data['val']
    },
    SET_CARDS(state, cards_data) {
      state.cards = cards_data
    },
    SET_DEVICES(state, devices_data) {
      state.devices = devices_data
    },
    SET_NAV(state, nav_data) {
      state.navData = nav_data
    },
    SET_POPUP(state, popup_data) {
      state.popupData = popup_data
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
    },
    updateNav({ commit, state }, navKey) {
      let navData = [...state.navData]
      navData.forEach(val => { val.active = '' })
      navData.[navKey].active = 'active'
      commit('SET_NAV', navData)
    },
    updatePopup({ commit, state }, popup) {
      commit('SET_POPUP', popup)
    },
    updateVal({ commit, state }, data) {
      commit('SET_VAL', { 'obj' : data.obj,  'val' : data.val })
    },
  },
  getters: {
    deviceByName: state => name => {
      var deviceData = {}
      var deviceCode = name.split('.')
      if (deviceCode[0] in state.devices) {
        if (deviceCode[1] in state.devices[deviceCode[0]]) {
          deviceData = state.devices[deviceCode[0]][deviceCode[1]]
        }
      }
      return deviceData
    },
    navIndex: state => {
      return state.navData.findIndex(nav => nav.active == 'active')
    }
  }
})
