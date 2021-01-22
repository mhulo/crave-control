<template>
  <div class="stl2">
    <div class="stl1">{{ card.label }} :: {{ compVals[compKeys(0)].toUpperCase() }}</div>
    <div>{{ card.devices[0] }} | {{ deviceData[compKeys(0)] }}</div>
    <v-icon :color="'black'">mdi-lightbulb-outline</v-icon>
    <Toggle1
      :key="cardId"
      :card="card"
      :deviceName="card.devices[0]"
      :compKey="compKeys(0)"
      :ref="compKeys(0)"
      @updated="handleUpdate"
    />
    <v-btn icon elevation="2" color="'blue'" @click="toggle(compKeys(0))">
      <v-icon >mdi-swap-horizontal</v-icon>
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
      compVals: {
        power: 'off'
      }
    }
  },
  methods: {
    compKeys(idx) {
      return Object.keys(this.compVals)[idx]
    },
    handleUpdate(update) {
      this.compVals[update.key] = update.val
    },
    toggle(key) {
      this.$refs[key].compVal = !(this.$refs[key].compVal)
      this.$refs[key].compChange()
    },
  },
  computed: {
    deviceData() {
      return {
        'power': this.$store.getters.getDeviceByName(this.card.devices[0]).power
      }
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
  border: 1px green solid;
}
</style>
