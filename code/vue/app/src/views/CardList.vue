<template>
  <v-app>
    <v-main>
      <div>crave control</div><br>
      <div v-for="(val, idx) in $store.state.cards" :key="idx+'_wrapper'">
        <component :is="val.card" :key="idx" :card="val"/>
        <br/>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'
import ApiService from '@/services/ApiService.js'

export default {
  components: {},
  data() {
    return {
      imported: []
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
    cardData() {
      return this.$store.state.cards
    }
  },
  watch: {
    cardData()  {
      this.ImportCards()
    }
  },
  created() {
    this.$store.dispatch('fetchCards')
    this.UpdateDevices()
  }
}
</script>
