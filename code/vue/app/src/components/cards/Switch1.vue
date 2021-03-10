<template>
  <div class="stl2">
    <div class="stl1">{{ card.label }} :: {{ widgetVals.power.toUpperCase() }}</div>
    <div>{{ card.devices[0] }} | {{ deviceVals.power }}</div>
    <v-icon :color="'black'">mdi-lightbulb-outline</v-icon>
    <Toggle1
      :key="cardId+'_power_toggle'"
      :card="card"
      :deviceName="card.devices[0]"
      valKey="power"
      ref="power_toggle"
      @handleUpdate="handleUpdate"
      @handleCommand="handleCommand"
    />
    <v-btn icon elevation="2" color="'blue'" @click="toggleComp('power_toggle')">
      <v-icon >mdi-swap-horizontal</v-icon>
    </v-btn>
    <v-btn icon elevation="2" color="'blue'" @click="handleExpand()">
      <v-icon >mdi-arrow-expand</v-icon>
    </v-btn>
    <br>
  </div>
</template>

<script>
import ApiService from '@/services/ApiService.js'
import Toggle1 from '@/components/widgets/Toggle1.vue'

export default {
  components: {
    Toggle1
  },
  props: {
    card: Object
  },
  data() {
    return {
      cardId: this.$vnode.key,
      widgetVals: {
        power: 'off'
      }
    }
  },
  methods: {
    handleUpdate(data) {
      this.widgetVals = { ...this.widgetVals, ...data }
    },
    handleCommand(data) {
      let command = ('command' in this.card)? this.card[command] : 'set_device_val'
      let card_params = ('command_params' in this.card)? this.card.command_params : {}
      let params = JSON.stringify({ ...card_params, ...data })
      let devices = JSON.stringify(this.card.devices)
      console.log('cmd: ' + command + ' --> params: ' + params + ', devices: ' + devices)
      let cmdUrl = '/core/run_command/?cmd=' + command + '&params=' + params + '&devices=' + devices
      ApiService.getApi(cmdUrl)
    },
    handleExpand() {
      this.$store.dispatch('updatePopup', {
        'type': 'card',
        'component': this.card.card,
        'params': { 'card': this.card } 
      })
    },
    toggleComp(key) {
      this.$refs[key].compVal = !this.$refs[key].compVal
      this.$refs[key].compChange()
    }
  },
  computed: {
    deviceVals() {
      return this.$store.getters.deviceByName(this.card.devices[0])
    },
    cardVals() {
      return { ...this.deviceVals, ...this.widgetVals }
    }
  }
}
</script>

<style scoped>
.stl1 {
  font-size: 15px;
  color: green;
}

.stl2 {
  font-size: 13px;
  color: black;
  background: white;
  border: 1px green solid;
}
</style>
