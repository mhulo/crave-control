<template>
  <v-main>
    <div>crave control</div><br>
    <div v-for="(val, idx) in this.cards" :key="idx+'_wrapper'">
      <component :is="val.card" :key="idx" :card="val"/>
      <br/>
    </div>
  </v-main>
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
    UpdateDevices() {
      this.$store.dispatch('fetchDevices')
      setTimeout(() => { this.UpdateDevices() }, 1500)
    },
    ImportCards() {
      Object.entries(this.$store.state.cards).forEach(([k, v]) => {
        let i = v['card']
        if (!this.imported.includes(i)) {
          this.$options.components[i] = () => import('@/components/cards/' + upperFirst(camelCase(i)) + '.vue')
          this.imported.push(i)
        }
      })
    },
  },
  computed: {
    stateCards() {
      return this.$store.state.cards
    }
  },
  watch: {
    stateCards()  {
      this.ImportCards()
      this.cards = this.stateCards
    }
  },
  created() {
    this.$store.dispatch('updateCards')
  },
  mounted() {
    WsService.reConnect()
  }
}
</script>
