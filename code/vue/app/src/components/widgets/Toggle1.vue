<template>
  <div class="stl3">
    <v-switch
      v-model="compVal"
      @change="compChange()"
    >
    </v-switch>
  </div>
</template>

<script>
import ApiService from '@/services/ApiService.js'

export default {
  props: {
    card: Object,
    deviceName: String,
    compKey: String
  },
  data() {
    return {
      compVal: false,
      compOldVal: false,
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
        this.$emit('updated', { 'key': this.compKey, 'val': this.prettyVal })
        console.log('command: ' + this.compCmd + ' --> card value/s: ' + this.prettyVal);
        let cmdUrl = '/core/run_command/?cmd=' + this.compCmd + '&set_key=' + this.compKey + '&set_val=' + this.prettyVal + '&wgt=' + this.cardId + '&z=123'
        ApiService.getApi(cmdUrl)
        setTimeout(() => { this.deviceChange() }, 6000)
      }
    },
    deviceChange() {
      if ((Date.now() - this.compChgTs) > 6000) {
        this.compVal = this.toLogical(this.deviceData[this.compKey])
        this.$emit('updated', { 'key': this.compKey, 'val': this.prettyVal })
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
    deviceData() {
      return this.$store.getters.getDeviceByName(this.deviceName)
    },
    compCmd() {
      if ('command' in this.card) {
        return this.card[command]
      }
      else {
        return 'set_card_val'
      }
    }
  },
  watch: {
    deviceData(newData, oldData)  {
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
  padding-left: 20px;
}
</style>
