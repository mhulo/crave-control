<template>
  <div class="stl2">
    <div class="stl1">{{ card.label }} :: {{ widgetVals.brightness }}%</div>
    <div>{{ card.devices[0] }} | {{ deviceVals.brightness }}</div>
    <v-icon :color="'black'">mdi-lightbulb-outline</v-icon>
    <Slider1
      :key="cardId+'_brightness_slider'"
      :card="card"
      :deviceName="card.devices[0]"
      valKey="brightness"
      ref="brightness_slider"
      @handleUpdate="handleUpdate"
      @handleCommand="handleCommand"
    />
    <v-btn icon elevation="2" color="'blue'" @click="decrementComp('brightness_slider')">
      <v-icon >mdi-minus</v-icon>
    </v-btn>
    <v-btn icon elevation="2" color="'blue'" @click="incrementComp('brightness_slider')">
      <v-icon >mdi-plus</v-icon>
    </v-btn>
    <v-btn icon elevation="2" color="'blue'" @click="toggleVal('power')">
      <v-icon >mdi-power</v-icon>
    </v-btn>
    <v-btn icon elevation="2" color="'blue'" @click="handleExpand()">
      <v-icon >mdi-arrow-expand</v-icon>
    </v-btn>
    <br>
  </div>
</template>

<script>
import ApiService from '@/services/ApiService.js'
import Slider1 from '@/components/widgets/Slider1.vue'

export default {
  components: {
    Slider1
  },
  props: {
    card: Object
  },
  data() {
    return {
      cardId: this.$vnode.key,
      widgetVals: {
        'brightness' : 0
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
    decrementComp(key) {
      this.$refs[key].compVal --
      this.$refs[key].compChange()
    },
    incrementComp(key) {
      this.$refs[key].compVal ++
      this.$refs[key].compChange()
    },
    toggleVal(key) {
      let data = null
      if (key in this.cardVals) {
        if (key == 'power') {
          let val = (this.cardVals[key] == 'on')? 'off' : 'on'
          data = { [key] : val }
        }
      }
      if (data != null) {
        this.handleUpdate(data)
        this.handleCommand(data)
      }
    },
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
  color: blue;
}

.stl2 {
  font-size: 13px;
  color: black;
  background: white;
  border: 1px blue solid;
}
</style>
