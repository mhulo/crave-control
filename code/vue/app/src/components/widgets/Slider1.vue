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
import ApiService from '@/services/ApiService.js'

export default {
  props: {
    card: Object,
    deviceName: String,
    compKey: String
  },
  data() {
    return {
      compVal: 0,
      compOldVal: 0,
      compChgTs: 0,
      cardId: this.$vnode.key
    }
  },
  methods: {
    compChange() {
      if (this.compVal != this.compOldVal) {
        this.compOldVal = this.compVal
        this.compChgTs = Date.now()
        this.$emit('updated', { 'key': this.compKey, 'val': this.compVal })
        console.log('command: ' + this.compCmd + ' --> card value/s: ' + this.compVal);
        let cmdUrl = '/core/run_command/?cmd=' + this.compCmd + '&set_key=' + this.compKey + '&set_val=' + this.compVal + '&wgt=' + this.cardId + '&z=123'
        ApiService.getApi(cmdUrl)
        setTimeout(() => { this.deviceChange() }, 6000)
      }
    },
    deviceChange() {
      if ((Date.now() - this.compChgTs) > 6000) {
        this.compVal = this.deviceData[this.compKey]
        this.$emit('updated', { 'key': this.compKey, 'val': this.compVal })
      }
    }
  },
  computed: {
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
}
</style>
