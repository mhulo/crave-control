<template>
  <div class="stl2">
    <div class="stl1">dimmer1 :: {{ widget.label }} :: {{ compVals[compKeys(0)] }}</div>
    <div>{{ widget.devices[0] }} [{{ widgetId }}]</div>
    <Slider1 
      :key="widgetId" 
      :widget="widget" 
      :deviceName="widget.devices[0]" 
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
import Slider1 from '@/components/Slider1.vue'

export default {
  components: {
    Slider1
  },
  props: {
    widget: Object
  },
  data() {
    return {
      widgetId: this.$vnode.key,
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
  border: 1px black solid;
}
</style>
