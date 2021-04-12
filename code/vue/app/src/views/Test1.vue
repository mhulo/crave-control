<template>
  <v-main>
    <div class="stl-test">
      Crave control<br/>
      ...landing
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
  },
  mounted() {
    setTimeout(() => { 
      window.location.href = '/home/'
    }, 1000)
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
