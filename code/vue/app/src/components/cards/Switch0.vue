<template>
  <div class="card-outer">
    <div class="label-row">
      <div class="label-name">
        <div>{{ card.label }} -0-</div>
      </div>
      <div class="label-value">{{ widgetVals.power.toUpperCase() }}</div>
      <div class="label-expand">
        <v-btn icon class="expand-icon" @click="handleExpand()">
          <v-icon v-if="options.show=='full'" class="close">mdi-close</v-icon>
          <v-icon v-else>mdi-chevron-up</v-icon>
        </v-btn>
      </div>
    </div>
    <div class="interface-row">{{ card.devices[0] }} | {{ deviceVals.power }}</div>
    <div class="widget-row">
      <v-btn icon :class="'icon-container '+isOn('power')" @click="toggleComp('power_toggle')">
        <v-icon>{{ cardIcon }}</v-icon>
      </v-btn>
      <div class="widget-container">
        <Toggle1
          :key="cardId+'_power_toggle'"
          :card="card"
          :deviceName="card.devices[0]"
          valKey="power"
          ref="power_toggle"
          @handleUpdate="handleUpdate"
          @handleCommand="handleCommand"
        />
      </div>
    </div>
    <div v-if="options.show=='full'">
      <div class="extras">
        <v-icon>mdi-plus</v-icon>
      </div>
    </div> 
  </div>
</template>

<script>
import ApiService from '@/services/ApiService.js'
import Toggle1 from '@/components/widgets/Toggle1.vue'

export default {
  components: {
    Toggle1
  },
  props: {
    card: Object,
    options: Object
  },
  data() {
    return {
      cardId: this.$vnode.key,
      widgetVals: {
        power: 'off'
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
    isOn(key) {
      return (this.widgetVals[key] == 'on') ? 'active' : ''
    },
    toggleComp(key) {
      this.$refs[key].compVal = !this.$refs[key].compVal
      this.$refs[key].compChange()
    }
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
  padding-left: 10px;
  flex-grow: 1;
  display: inline-block;
  border: 0px red solid;
}
.icon-container i.v-icon{
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
  padding-left: 0px;
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
</style>