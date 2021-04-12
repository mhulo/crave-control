<template>
  <div class="card-outer">
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
      <v-btn icon :class="'icon-container '+isActive('brightness')" @click="toggleVal('power')">
        <v-icon>{{ cardIcon }}</v-icon>
      </v-btn>
      <div class="widget-container">
        <Slider1
          :key="cardId+'_brightness_slider'"
          :card="card"
          :deviceName="card.devices[0]"
          valKey="brightness"
          ref="brightness_slider"
          @handleUpdate="handleUpdate"
          @handleCommand="handleCommand"
        />
      </div>
    </div>
    <div v-if="options.show=='full'">
      <div class="plus-minus">
        <v-btn icon class="extras" @click="decrementComp('brightness_slider')">
          <v-icon>mdi-minus</v-icon>
        </v-btn>
        <v-btn icon class="extras" @click="incrementComp('brightness_slider')">
          <v-icon >mdi-plus</v-icon>
        </v-btn>
      </div>
    </div>  
  </div>
</template>

<script>
import ApiService from '@/services/ApiService.js'
import Slider1 from '@/components/widgets/Slider1.vue'

export default {
  components: {
    Slider1
  },
  props: {
    card: Object,
    options: Object
  },
  data() {
    return {
      cardId: this.$vnode.key,
      widgetVals: {
        'brightness' : 0
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
    }
  }
}
</script>

<style scoped>
.card-outer {
  color: grey;
  background: rgba(0,0,0,0.75);
  padding: 14px;
  border-radius: 10px;
  border: 0px blue solid;
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
  color: rgba(255,255,255,0.5);
}
.widget-row {
  display: flex;
  padding-top: 5px;
  font-size: 11px;
  border: 0px green solid;
}
.icon-container { 
  display: inline-block;
  display: flex;
  justify-content: center;
  width: 28px;
  height: 28px;
  font-size: 20px;
  margin-top: 2px;
  border: 1px rgba(255, 255, 255, 0.5) solid;
  border-radius: 50%;
}
.widget-container {
  padding: 0px 2px 0px 10px;
  width: 100%;
  display: inline-block;
  border: 0px red solid;
}
.icon-container i.v-icon {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.5);
  padding-left: 0px;
}
.active.icon-container {
  border-color: white;
}
.active.icon-container i.v-icon{
  color: white;
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
  padding-left: 35px;
  border: 0px blue solid;
}
</style>
