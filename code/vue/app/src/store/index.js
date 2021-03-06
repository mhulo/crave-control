import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '@/services/ApiService.js'
import WsService from '@/services/WsService.js'
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    socket: {
      'started': false,
      'connected': false
    },
    cards: {},
    icons: {},
    devices: {},
    nav: {
      'primary': [
        {
          'name': 'groups',
          'icon': 'mdi-gamepad-circle-outline'
        },
        {
          'name': 'zones',
          'icon': 'mdi-collage' //'fab fa-codepen'
        },
        {
          'name': 'dashboard',
          'icon': 'mdi-monitor-dashboard'
        },
        {
          'name': 'admin',
          'icon': 'mdi-cog-outline'
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
      }
    },
    popup: {
      'show': false,
      'type': null,
      'component': null,
      'params' : {}
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
    SET_IFX(state, ifx_data) {
      if (ifx_data['val'] == null) {
        Vue.delete(state.devices, ifx_data['key'])        
      }
      else if (!(ifx_data['key'] in state.devices)) {
        Vue.set(state.devices, ifx_data['key'], ifx_data['val'])
      }
      else {
        state.devices[ifx_data['key']] = ifx_data['val']
      }
    },
    SET_ICONS(state, icons_data) {
      state.icons = icons_data
    },
    SET_NAV_SELECTED(state, selected_data) {
      state.nav.selected.[selected_data['key']] = selected_data['val']
    },
    SET_NAV_POPUP(state, popup_data) {
      state.popup = popup_data
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
            dispatch('updateNav', { key: 'secondary', val: 0 })
            dispatch('updateIcons')
          }
        })
        .catch(error => {
          console.log('cards api error:', error.response)
        })
    },
    updateIcons({ commit, state, dispatch }) {
      ApiService.getApi('/core/icons_conf/')
        .then(response => {
          commit('SET_ICONS', response.data)
        })
        .catch(error => {
          console.log('icons api error:', error.response)
        })
    },
    updateDevices({ commit, state }, devices) {
      Object.entries(devices).forEach(([k, v]) => {
        if (JSON.stringify(v) != JSON.stringify(state.devices['k'])) {
          commit('SET_IFX', { 'key': k, 'val': v})
        }
      })
    },
    updateNav({ commit, state, getters }, data) {
      let key = data['key']
      let idx = data['val']
      let sec = (Object.keys(getters.navSecondary).length > 0) ?
        getters.navSecondary[idx].name :
        'All'
      let navVal = {}
      navVal.index = idx
      navVal.name = (key == 'primary') ?
        state.nav.primary[idx].name :
        [ state.nav.selected.primary.name, sec]
      commit('SET_NAV_SELECTED', { 'key': key, 'val': navVal })
    },
    updatePopup({ commit, state }, data) {
      let show = true
      if ('show' in data) {
        show = data.show
      }
      else if (('component' in data) && (state.popup.show == true)) {
        if (data.component == state.popup.component) {
          if ('params' in data) {
            if (JSON.stringify(data.params) == JSON.stringify(state.popup.params)) {
              show = false
            }
          }
          else {
            show = false
          }
        }
      }
      let new_data = { ...state.popop, ...data, 'show': show }
      commit('SET_NAV_POPUP', new_data)
    },
    updateVal({ commit }, data) {
      commit('SET_VAL', { 'key' : data.obj,  'val' : data.val })
    },
  },
  getters: {
    cards: state => {
      let cards = { ...state.cards }
      for (const x in cards) {
        cards.[x].card = upperFirst(camelCase(cards.[x].card))
      }
      return cards
    },
    deviceByName: state => name => {
      let deviceData = {}
      let deviceCode = name.split('.')
      if (deviceCode[0] in state.devices) {
        if (state.devices[deviceCode[0]] != '') {
          if (deviceCode[1] in state.devices[deviceCode[0]]) {
            deviceData = state.devices[deviceCode[0]][deviceCode[1]]
          }
        }
      }
      return deviceData
    },
    navSecondary: state => {
      let things = []
      let primary = state.nav.selected.primary.name
      if (Object.keys(state.cards).length > 0) {
        for (const x in state.cards) {
          if (primary in state.cards.[x]) {
            for (const y of state.cards.[x].[primary]) {
              if (!(things.includes(y))) { things.push(y) }
            }
          }
        }
      }
      things.sort()
      return things.map((x, idx) => {
        let active = (
          (primary == state.nav.selected.secondary.name[0]) &&
          (x == state.nav.selected.secondary.name[1])
         ) ? 'active' : ''
        let iconIndex = -1
        if (primary in state.icons) {
          iconIndex = state.icons.[primary].findIndex(y => y.label == x)
        }
        let icon = (iconIndex != -1) ? state.icons.[primary].[iconIndex].icon : 'mdi-power-plug-outline'
        return  {
          'name': x,
          'active': active,
          'icon' : icon
        }
      })
    }
  }
})
