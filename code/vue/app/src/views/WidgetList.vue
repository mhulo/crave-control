<template>
  <v-app>
    <v-main>
      <WidgetCard v-for="(v, k) in $store.state.widgets" :key="k" :widget="v"/>
    </v-main>
  </v-app>
</template>

<script>
import WidgetCard from '@/components/WidgetCard.vue'
import ApiService from '@/services/ApiService.js'

export default {
  components: {
    WidgetCard
  },
  data() {
    return { }
  },
  methods: {
    UpdateDevices() {
      this.$store.dispatch('fetchDevices')
      setTimeout(() => { 
        this.UpdateDevices() 
      }, 1000)
    }
  },
  created() {
    this.$store.dispatch('fetchWidgets')
    this.UpdateDevices()
  }
}
</script>
