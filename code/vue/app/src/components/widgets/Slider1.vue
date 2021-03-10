<template>
  <div class="stl3">
    <v-slider
      v-model="compVal"
      @change="compChange()"
      max="100"
      min="0"
      thumb-label
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
  font-size: 15px;
  color: blue;
}

.stl3 {
  font-size: 13px;
  color: black;
  padding: 0px 20px 0px 20px;
}
</style>
