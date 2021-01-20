<template>
  <div class="stl2">
    <div class="stl1">{{ card.label }} :: {{ compVals[compKeys(0)] }}%</div>
    <div>{{ card.devices[0] }} | {{ deviceData.brightness }}</div>
    <v-icon :color="'black'">mdi-lightbulb-outline</v-icon>
    <Slider1
      :key="cardId"
      :card="card"
      :deviceName="card.devices[0]"
      :compKey="compKeys(0)"
      :ref="compKeys(0)"
      @updated="handleUpdate"
    />
    <v-icon :color="'blue'" @click="decrement(compKeys(0))">mdi-minus</v-icon>
    <v-icon :color="'blue'" @click="increment(compKeys(0))">mdi-plus</v-icon>
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
      compVals: {
        brightness: 0
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
    decrement(key) {
      this.$refs[key].compVal --
      this.$refs[key].compChange()
    },
    increment(key) {
      this.$refs[key].compVal ++
      this.$refs[key].compChange()
    }
  },
  computed: {
    deviceData() {
      return {
        'brightness': this.$store.getters.getDeviceByName(this.card.devices[0]).brightness
      }
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
  border: 1px blue solid;
}
</style>
