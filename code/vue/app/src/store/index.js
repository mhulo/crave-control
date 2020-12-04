import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: { id: 'abc123', name: 'Adam Jahr' },
    categories: [
      'sustainability',
      'nature',
      'animal welfare',
      'housing',
      'education',
      'food',
      'community'
    ],
    events: [
      { id: 1, title: '...', organiser: '...' },
      { id: 2, title: '...', organiser: '...' },
      { id: 3, title: '...', organiser: '...' },
      { id: 4, title: '...', organiser: '...' }
    ]
  },
  mutations: {},
  actions: {},
  getters: {
    catLength: state => {
      return state.categories.length
    },
    dontTodos: state => {
      return state.todos.filter(todo => todo.done)
    },
    activeTodosCount: state => {
      return state.todos.filter(todo => !todo.done).length
    },
    getEventById: (state) => (id) => {
      return state.events.find(event => event.id === id)
    }
  },
  modules: {}
})
