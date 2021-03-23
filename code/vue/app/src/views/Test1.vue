<template>
  <v-main>
    <div class="stl-test">
      <v-slider
        v-model="compVal"
        @change="compChange()"
        max="100"
        min="0"
        thumb-label
      >
      </v-slider>
    </div>
  </v-main>
</template>

<script>
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'
import WsService from '@/services/WsService.js'

export default {
  components: {},
  data() {
    return {
      compVal: 0
    }
  },
  methods: {
    compChange() {
      console.log('changed')
    }
  }
}
</script>

<style>
.stl-test {
  width: 400px;
  height: 200px;
  border: 1px red solid;
  padding: 30px;
}
</style>
