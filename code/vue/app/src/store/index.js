import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/services/ApiService.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    cards: {},
    devices: {},
    nav: {
      primary: [
        {
          'text': 'Zones',
          'icon': 'mdi-view-dashboard-outline'
        },
        {
          'text': 'Groups',
          'icon': 'mdi-flip-to-front'
        },
        {
          'text': 'Lights',
          'icon': 'mdi-lightbulb-outline'
        },
        {
          'text': 'Battery',
          'icon': 'mdi-battery-outline'
        }
      ],
      selected: {
        'primary': {
          'index' : 0
        }
      },
      popup: false
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
    SET_NAV_SELECTED(state, selected_data) {
      state.nav.selected = selected_data
    },
    SET_NAV_POPUP(state, popup_data) {
      state.nav.popup = popup_data
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
    updateNavSelected({ commit, state }, data) {
      let selected = state.nav.selected
      selected.[data['key']].index = data['val']
      commit('SET_NAV_SELECTED', selected)
    },
    updateNavPopup({ commit, state }, data) {
      commit('SET_NAV_POPUP', data)
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
    }
  }
})
