<template>
  <v-app>
    <v-main>
      <div>crave control</div><br>
      <component :is="val.widget" v-for="(val, idx) in $store.state.widgets" :key="idx" :widget="val"/>
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
      setTimeout(() => { this.UpdateDevices() }, 1000)
    },
    ImportWidgets() {
      Object.entries(this.$store.state.widgets).forEach(([k, v]) => {
        let i = v['widget']
        if (!this.imported.includes(i)) {
          this.$options.components[i] = () => import('@/components/' + upperFirst(camelCase(i)) + '.vue')
          this.imported.push(i)
        }
      })
    },
  },
  computed: {
    widgetData() {
      return this.$store.state.widgets
    }
  },
  watch: {
    widgetData()  {
      this.ImportWidgets()
    }
  },
  created() {
    this.$store.dispatch('fetchWidgets')
    this.UpdateDevices()
  }
}
</script>
