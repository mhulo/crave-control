<template>
  <div class="slider-1">
    <v-slider
      v-model="compVal"
      max="100"
      min="0"
      :color="sliderRgb"
      track-color="rgba(255, 255, 255, 0.5)"
    >
    </v-slider>
  </div>
</template>

<script>
export default {
  props: {
    card: Object,
    deviceName: String,
    sliderRgb: String,
    valKey: String
  },
  data() {
    return {
      cardId: this.$vnode.key,
      compVal: 0,
      compChgTimestamp: 0,
      cmdRate: 300,
      cmdTimeStamp: 0,
      cmdVal: null
    }
  },
  methods: {
    compChange(newVal=null) {
      if ((newVal != null) && (newVal != this.deviceVals[this.valKey])) {
        this.cmdVal = newVal
      }
      if (this.cmdVal != null) {
        if ((Date.now() - this.cmdTimeStamp) > this.cmdRate) {
          this.cmdVal = null
          this.cmdTimeStamp = Date.now()
          this.compChgTimestamp = Date.now()
          this.$emit('handleUpdate', { [this.valKey] : this.compVal })
          this.$emit('handleCommand', { [this.valKey] : this.compVal })
          setTimeout(() => { this.deviceChange() }, 6000)
        }
        else {
          let retryDelay = Math.round(this.cmdRate / 2)
          setTimeout(() => { this.compChange() }, retryDelay)
        }
      }
    },
    deviceChange() {
      if ((Date.now() - this.compChgTimestamp) > 6000) {
        if (this.valKey in this.deviceVals) {
          this.compVal = this.deviceVals[this.valKey]
          this.$emit('handleUpdate', { [this.valKey] : this.compVal })
        }
      }
    }
  },
  computed: {
    deviceVals() {
      return this.$store.getters.deviceByName(this.deviceName)
    }
  },
  watch: {
    compVal() {
      this.compChange(this.compVal)
    },
    deviceVals(newData, oldData)  {
      if (JSON.stringify(newData) != JSON.stringify(oldData)) {
        this.deviceChange()
      }
    }
  },
  mounted() {
    this.deviceChange()
  }
}
</script>

<style scoped>

.slider-1 {
  height: 30px;
  width: 100%;
  border: 0px blue solid;
}
</style>
