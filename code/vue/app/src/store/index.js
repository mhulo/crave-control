import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/services/ApiService.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    widgets: {
      "wgt0002": {
        "widget": "dimmer_1",
        "label": "Nia's Bedroom Lights",
        "devices": [
          "cgate.nias_bedroom_lights"
        ],
        "fave_1": 15,
        "fave_2": 40,
        "groups": [
        "Lights",
        "Upstairs"
        ]
      },
      "wgt0003": {
        "widget": "dimmer_1",
        "label": "Study Lights",
        "devices": [
        "cgate.study_lights"
        ],
        "fave_1": 15,
        "fave_2": 40,
        "groups": [
        "Lights"
        ]
      }
    },
    devices: {}
  },
  mutations: {
    ADD_WIDGET(state, widget) {
      state.widgets.push(widget)
    },
    SET_WIDGETS(state, widgets_data) {
      state.widgets = widgets_data
    },
    SET_DEVICES(state, devices_data) {
      state.devices = devices_data
    }
  },
  actions: {
    fetchWidgets({ commit, state }) {
      ApiService.getApi('/core/widgets_conf/')
        .then(response => {
          if (JSON.stringify(response.data) != JSON.stringify(state.widgets)) {
            commit('SET_WIDGETS', response.data)
          }
        })
        .catch(error => {
          console.log('api error:', error.response)
        })
    },
    fetchDevices({ commit, state }) {
      ApiService.getApi('/core/event/state/')
        .then(response => {
          if (JSON.stringify(response.data) != JSON.stringify(state.devices)) {
            commit('SET_DEVICES', response.data)
          }
        })
        .catch(error => {
          console.log('api error:', error.response)
        })
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
    },

  }
})
