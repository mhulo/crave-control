<template>
  <div class="stl2">
    <div class="stl1">switch: {{ card.label }}</div>
    <div>{{ card.devices[0] }} [{{ id }}]</div>
    <div>{{ deviceData }}</div>
    <div>Slider: {{ newVal }}</div>
    <v-slider
      key="slider1"
      v-model="newVal"
      @change="handleChange()"
      max="100"
      min="0"
      thumb-label
      prepend-icon="mdi-volume-high"
    >
    </v-slider>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    card: Object
  },
  data() {
    return {
      newVal: 0,
      oldVal: 0,
      id: this.$vnode.key
    }
  },
  methods: {
    handleChange() {
      if (this.newVal != this.oldVal) {
        console.log('card ' + this.card.id + ' -> ' + this.newVal)
        this.oldVal = this.newVal
      }
    }
  },
  computed: {
    deviceData() {
      return this.$store.getters.getDeviceByName(this.card.devices[0])
    }

  },
  watch: {
    deviceData(newData, oldData)  {
      if (JSON.stringify(newData) != JSON.stringify(oldData)) {
        //console.log(this.card.label + ' watch change')
        this.newVal = this.deviceData.brightness
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
}
</style>