<template>
  <v-app>
    <v-main>
      <div>Message: {{ msg }}</div>
      <div>Slider: {{ newVal }}</div>
      <WidgetCard v-for="widget in widgets" :key="widget.id" :widget="widget"/>
      <v-slider
        key="slider1"
        v-model="newVal"
        @change="myLog()"
        max="100"
        min="0"
        thumb-label
        prepend-icon="mdi-volume-high"
      >
      </v-slider>
    </v-main>
  </v-app>
</template>

<script>
import WidgetCard from '@/components/WidgetCard.vue'
import ApiService from '@/services/ApiService.js'

export default {
  components: {
    WidgetCard
  },
  data() {
    return {
      newVal: 0,
      oldVal: 0,
      widgets: [
        {
          id: 1,
          name: 'room'
        },
        {
          id: 2,
          name: 'stairs'
        }
      ],
      msg: ''
    }
  },
  created() {
    ApiService.getApi('/core/event/status/')
      .then(response => {
        console.log('res:', response)
        this.msg = response.data.core_daemon.message
      })
      .catch(error => {
        console.log('api error:', error.response)
      })
  },
  methods: {
    myLog() {
      if (this.newVal != this.oldVal) {
        console.log('logging ' + this.newVal)
        this.oldVal = this.newVal
      }
    }
  }
}
</script>
