<template>
  <div class="stl1">
    <v-slider
      v-model="compVal"
      @change="compChange()"
      max="100"
      min="0"
      color="white"
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
    valKey: String
  },
  data() {
    return {
      compVal: 0,
      compOldVal: null,
      compChgTs: 0,
      cardId: this.$vnode.key
    }
  },
  methods: {
    compChange() {
      if (this.compVal != this.compOldVal) {
        this.compOldVal = this.compVal
        this.compChgTs = Date.now()
        this.$emit('handleUpdate', { [this.valKey] : this.compVal })
        this.$emit('handleCommand', { [this.valKey] : this.compVal })
        setTimeout(() => { this.deviceChange() }, 6000)
      }
    },
    deviceChange() {
      if ((Date.now() - this.compChgTs) > 6000) {
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

.stl1 {
  height: 35px;
  border: 0px red solid;
}
</style>
