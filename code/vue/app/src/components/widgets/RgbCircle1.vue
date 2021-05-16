<template>
  <div class="circle-1">
    <div :id="circleId">
    </div>
    <div class="handle-container">
      <svg>
        <defs>
          <g id="handle">
            <circle r="10" fill="rgba(0,0,0,0)" stroke-width="2" stroke="#000"></circle>
          </g>
        </defs>
      </svg>
    </div>
  </div>
</template>

<script>
import iro from '@jaames/iro'

export default {
  props: {
    card: Object,
    options: Object,
    deviceName: String,
    valKey: String
  },
  data() {
    return {
      cardId: this.$vnode.key,
      compVal: 0,
      compChgTimestamp: 0,
      cmdRate: 300,
      cmdTimeStamp: 0,
      cmdVal: null,
      rgbCircle: null
    }
  },
  methods: {
    compChange(newVal = null) {
      if ((newVal != null) && (JSON.stringify(newVal) != JSON.stringify(this.deviceVals[this.valKey]))) {
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
          if (this.rgbCircle != null) {
            this.rgbCircle.color.rgb = this.toCompFormat(this.compVal)
          }
        }
      }
    },
    handleCircleActive() {
      this.deviceChange()
      if (this.options.show == 'full') {
        if (this.rgbCircle == null) {
          this.rgbCircle = new iro.ColorPicker('#'+this.circleId, {
            width: 300,
            color: '#FFF',
            handleRadius: 12,
            handleSvg: '#handle',
            layout: [{ component: iro.ui.Wheel }]
          })
          this.rgbCircle.on('color:change', this.onColorChange)
          setTimeout(() => { this.deviceChange() }, 50)
        }
      }
    },
    onColorChange(color) {
      this.compVal = this.toIfxFormat(color.rgb)
    },
    toCompFormat(val) {
      return { r: val[0], g: val[1], b: val[2] }
    },
    toIfxFormat(val) {
      return [ val.r, val.g, val.b ]
    }
  },
  computed: {
    circleId() {
      return this.cardId + '_rgb_circle_1_' + this.options.show
    },
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
    this.handleCircleActive()
  },
  beforeDestroy() {
    if (this.rgbCircle != null) {
      this.rgbCircle.off('color:change', this.onColorChange)
      this.rgbCircle = null
    }
  }
}
</script>

<style scoped>

.circle-1 {
  width: 100%;
  display: flex;
  justify-content: center;
  padding-bottom: 5px;
  border: 0px red solid;
}
.handle-container {
  display: none;
}
</style>
