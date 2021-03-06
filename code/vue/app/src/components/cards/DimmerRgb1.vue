<template>
  <div class="card-outer">
    <div class="card-details">
      <div class="card-icon">
        <v-btn
          icon
          :class="'icon-container '+isActive('brightness')"
          :style="icon1"
          @click="toggleVal('power')"
        >
          <v-icon>{{ cardIcon }}</v-icon>
        </v-btn>
      </div>
      <div class="details-main">
        <div class="label-row">
          <div class="label-name">
            <div>{{ card.label }}</div>
          </div>
          <div class="label-value">{{ widgetVals.brightness }}%</div>
          <div class="label-expand">
            <v-btn icon class="expand-icon" @click="handleExpand()">
              <v-icon v-if="options.show=='full'" class="close">mdi-close</v-icon>
              <v-icon v-else>mdi-chevron-up</v-icon>
            </v-btn>
          </div>
        </div>
        <div class="interface-row">{{ card.devices[0] }} | {{ deviceVals.brightness }}</div>
        <div class="widget-row">
          <div class="widget-container">
            <Slider1
              :key="cardId+'_brightness_slider'"
              :card="card"
              :deviceName="card.devices[0]"
              :sliderRgb="sliderRgb"
              valKey="brightness"
              ref="brightness_slider"
              @handleUpdate="handleUpdate"
              @handleCommand="handleCommand"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-show="options.show=='full'" class="card-main">
      <div class="plus-minus">
        <v-btn icon class="extras" @click="decrementComp('brightness_slider')">
          <v-icon>mdi-minus</v-icon>
        </v-btn>
        <v-btn icon class="extras" @click="incrementComp('brightness_slider')">
          <v-icon >mdi-plus</v-icon>
        </v-btn>
      </div>
      <div>
        <div class="circle-container">
          <RgbCircle1
            :key="cardId+'_rgb_circle'"
            :card="card"
            :options="options"
            :deviceName="card.devices[0]"
            valKey="rgb"
            ref="rgb_circle"
            @handleUpdate="handleUpdate"
            @handleCommand="handleCommand"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '@/services/ApiService.js'
import Slider1 from '@/components/widgets/Slider1.vue'
import RgbCircle1 from '@/components/widgets/RgbCircle1.vue'

export default {
  components: {
    Slider1,
    RgbCircle1
  },
  props: {
    card: Object,
    options: Object
  },
  data() {
    return {
      cardId: this.$vnode.key,
      widgetVals: {
        'brightness' : 0,
        'rgb' : [0,0,0]
      }
    }
  },
  methods: {
    handleUpdate(data) {
      this.widgetVals = { ...this.widgetVals, ...data }
    },
    handleCommand(data) {
      let command = ('command' in this.card)? this.card[command] : 'set_device_val'
      let card_params = ('command_params' in this.card)? this.card.command_params : {}
      let params = JSON.stringify({ ...card_params, ...data })
      let devices = JSON.stringify(this.card.devices)
      console.log('cmd: ' + command + ' --> params: ' + params + ', devices: ' + devices)
      let cmdUrl = '/core/run_command/?cmd=' + command + '&params=' + params + '&devices=' + devices
      ApiService.getApi(cmdUrl)
    },
    handleExpand() {
      (this.options.show == 'full') ?
        this.$router.push({ path: '/cards/' }) :
        this.$router.push({ path: `/cards/detail/${this.cardId}/` })
    },
    isActive(key) {
      return (this.widgetVals[key] > 0) ? 'active' : ''
    },
    decrementComp(key) {
      this.$refs[key].compVal --
      this.$refs[key].compChange()
    },
    incrementComp(key) {
      this.$refs[key].compVal ++
      this.$refs[key].compChange()
    },
    toggleVal(key) {
      let data = null
      if (key in this.cardVals) {
        if (key == 'power') {
          let val = (this.cardVals[key] == 'on')? 'off' : 'on'
          data = { [key] : val }
        }
      }
      if (data != null) {
        this.handleUpdate(data)
        this.handleCommand(data)
      }
    },
  },
  computed: {
    deviceVals() {
      return this.$store.getters.deviceByName(this.card.devices[0])
    },
    cardVals() {
      return { ...this.deviceVals, ...this.widgetVals }
    },
    cardIcon() {
      return ('icon' in this.card) ? this.card.icon : 'mdi-lightbulb-outline'
    },
    deviceRgb() {
      let rgb = this.widgetVals.rgb
      return `${rgb[0]}, ${rgb[1]}, ${rgb[2]}`
    },
    icon0() {
      // hollow icons with coloured borders
      return (this.widgetVals.brightness > 0) ?
        ({
          color: `rgba(${this.deviceRgb}) !important`,
          border: `1px rgba(${this.deviceRgb}) solid !important`,
          backgroundColor: `rgba(0,0,0,0) !important`
        }) :
        ({
          color: `rgba(255,255,255,0.6) !important`,
          border: `0px rgba(255,255,255,0.6) solid !important`,
          backgroundColor: `rgba(255,255,255,0.1) !important`,
        })
    },
    icon1() {
      //solid icons with coloured background
      return (this.widgetVals.brightness > 0) ?
        ({
          color: `rgba(0,0,0,0.8) !important`,
          border: `0px rgba(255,255,255,0.6) solid !important`,
          backgroundColor: `rgba(${this.deviceRgb}) !important`,

        }) :
        ({
          color: `rgba(255,255,255,0.6) !important`,
          border: `0px rgba(255,255,255,0.6) solid !important`,
          backgroundColor: `rgba(255,255,255,0.1) !important`,
        })
    },
    sliderRgb() {
      return (this.widgetVals.brightness > 0) ?
        //`rgb(${this.deviceRgb})` :
        `rgb(255,255,255)` :
        `rgba(255,255,255,1)`        
    }
  }
}
</script>

<style scoped>
.card-outer {
  color: grey;
  background: rgba(0,0,0,var(--theme-card-opacity));
  padding: 14px;
  border-radius: 10px;
  border: 0px blue solid;
  display: flex;
  flex-direction: column;
}
.card-details {
  border: 0px red solid;
  display: flex;
}
.card-main {
  border: 0px red solid;
  display: flex;
  flex-direction: column;
}

.card-icon {
  width: 45px;
  height: 75px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 0px;
  border: 0px blue solid;
}
.icon-container { 
  display: inline-block;
  display: flex;
  justify-content: center;
  width: 35px;
  height: 35px;
  margin-top: 2px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
}
.icon-container i.v-icon {
  font-size: 22px;
  padding-left: 0px;
}
.details-main {
  height: 100%;
  flex-grow: 1;
  border: 0px green solid;
}
.label-row {
  display: flex;
  font-size: 13px;
  font-weight: 400;
  color: white;
  border: 0px red solid;
}
.label-name {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  border: 0px orange solid;
  padding-bottom: 2px;
}
.label-value {
  font-size: 14px;
  padding-top: 2px;
  border: 0px green solid;
  padding-right: 10px;
}
.label-expand {
  color: white;
  font-size: 14px;
  width: 24px;
  height: 24px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  border: 0px green solid;
}
.interface-row {
  font-size: 11px;
  color: rgba(255,255,255,0.6);
}
.widget-row {
  display: flex;
  padding-top: 5px;
  font-size: 11px;
  border: 0px green solid;
}
.widget-container {
  padding: 0px 2px 0px 2px;
  width: 100%;
  display: inline-block;
  border: 0px red solid;
}
.circle-container {
  display: flex;
  justify-content: center;
  border: 0px blue solid;
}
.active.icon-container {
  /*background: rgba(0,0,0,0);*/
}
.active.icon-container i.v-icon{
  /*color: white;*/
}
.expand-icon i.v-icon {
  font-size: 20px;
  color: white;
}
.v-btn.expand-icon {
  width: 24px;
  height: 24px;
}
i.v-icon.close {
  font-size: 16px;
  color: white;
}
.extras i.v-icon {
  font-size: 20px;
  color: white;
}
.plus-minus {
  display: flex;
  justify-content: space-between;
  padding-left: 47px;
  border: 0px blue solid;
}
</style>
