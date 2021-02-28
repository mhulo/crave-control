<template>
  <div id="card-list">
    <div v-for="(val, idx) in this.cards" :key="idx+'_wrapper'">
      <!--<component :is="val.card" :key="idx" :card="val"/>-->
      <div :key="idx">stuff</div>
      <br/>
    </div>
  </div>
</template>

<script>
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'
import WsService from '@/services/WsService.js'

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
    }
  },
  watch: {
    stateCards() {
      this.ImportCards()
    }
  },
  created() {
    console.log('cards created')
    WsService.reConnect()
    this.ImportCards()
    this.$store.dispatch('updateCards')
  },
  mounted() {
    console.log('cards mounted')
  }
}
</script>

<style>
  #card-list {
    background: red;
  }
</style>
