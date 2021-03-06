<template>
  <div id="card-list">
    <div v-for="(val, idx) in filteredCards" :key="idx+'_wrapper'">
      <component :is="val.card" :key="idx" :card="val"/>
      <!--<div :key="idx">stuff</div>-->
      <br/>
    </div>
  </div>
</template>

<script>
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'

export default {
  components: {},
  data() {
    return {
      imported: [],
      cards: {}
    }
  },
  methods: {
    ImportCards() {
      Object.entries(this.$store.state.cards).forEach(([k, v]) => {
        let i = v['card']
        if (!this.imported.includes(i)) {
          this.$options.components[i] = () => import('@/components/cards/' + upperFirst(camelCase(i)) + '.vue')
          this.imported.push(i)
        }
      })
      this.cards = this.stateCards
    },
  },
  computed: {
    stateCards() {
      return this.$store.state.cards
    },
    filteredCards() {
      let cards = this.$store.state.cards
      let filters = this.$store.state.nav.selected.secondary.name
      let filtered = {}
      if (filters[1] != '') {
        Object.entries(cards).forEach(([k, v]) => {
          if (filters[0].toLowerCase() in v) {
            if (v[filters[0].toLowerCase()].includes(filters[1])) {
              filtered[k] = v
            }
          }
        })
      }
      else {
        filtered = cards
      }
      return filtered
    }
  },
  watch: {
    stateCards() {
      this.ImportCards()
    }
  },
  created() {
    console.log('cards created')
    this.$store.dispatch('startSocket')
    this.ImportCards()
    this.$store.dispatch('updateCards')
  },
  mounted() {
  }
}
</script>

<style>
  #card-list {
    background: white;
  }
</style>
