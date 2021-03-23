<template>
  <div class="toggle-1">
    <v-switch
      v-model="compVal"
      @change="compChange()"
      color="white"
      dark
      dense
    >
    </v-switch>
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
      compVal: false,
      compOldVal: null,
      compChgTs: 0,
      cardId: this.$vnode.key,
      compStates: {
        'on': true,
        'off': false
      }
    }
  },
  methods: {
    compChange() {
      if (this.compVal != this.compOldVal) {
        this.compOldVal = this.compVal
        this.compChgTs = Date.now()
        this.$emit('handleUpdate', { [this.valKey] : this.prettyVal })
        this.$emit('handleCommand', { [this.valKey] : this.prettyVal })
        setTimeout(() => { this.deviceChange() }, 6000)
      }
    },
    deviceChange() {
      if ((Date.now() - this.compChgTs) > 6000) {
        if (this.valKey in this.deviceVals) {
          this.compVal = this.toLogical(this.deviceVals[this.valKey])
          this.$emit('handleUpdate', { [this.valKey] : this.prettyVal })
        }
      }
    },
    toPretty(val) {
      return Object.keys(this.compStates).find(key => this.compStates[key] === val)
    },
    toLogical(val) {
      return this.compStates[val]
    }
  },
  computed: {
    prettyVal() {
      return this.toPretty(this.compVal)
    },
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
.toggle-1 {
  height: 35px;
  border: 0px blue solid;
}

.toggle-1 .v-input--switch {
  margin: 1px;
}
</style>
