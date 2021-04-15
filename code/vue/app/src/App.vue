<template>
  <v-app :style="cssVars">
    <router-view/>
  </v-app>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      // themes
      selected: 'grey1',
      grey1: {
        hlColor1: '#0b1114',
        hlColor2: '#292f31',
        hlGradDeg: '135deg',
        bgColor1: '#0b1114', 
        bgColor2: '#363e41', 
        bgGradDeg: '-45deg',
        sideOpacity: '0.5',
        cardOpacity: '0.4'
      },
      blue1: {
        hlColor1: '#1f1f42', 
        hlCcolor2: '#1c1c5f', 
        hlGradDeg: '45deg',
        bgColor1: '#3c415a', 
        bgColor2: '#000000', 
        bgColor3: '#0b1114', 
        bgGradDeg: '-45deg',
        sideOpacity: '0.6',
        cardOpacity: '0.4'
      },
      blue2: {
        hlColor1: '#3f35d8', 
        hlColor2: '#191558', 
        hlGradDeg: '45deg',
        bgColor1: '#000000', 
        bgColor2: '#3f35d8', 
        bgGradDeg: '-45deg',
        sideOpacity: '0.6',
        cardOpacity: '0.4'
      }
    }
  },
  computed: {
    // dynamic css variables
    cssVars () {
      let theme = this.[this.selected]
      return {
        '--theme-hl-color-1': theme.hlColor1,
        '--theme-hl-color-2': theme.hlColor2,
        '--theme-hl-grad-deg': theme.hlGradDeg,
        '--theme-bg-color-1': theme.bgColor1,
        '--theme-bg-color-2': theme.bgColor2,
        '--theme-bg-grad-deg': theme.bgGradDeg,
        '--theme-side-opacity': theme.sideOpacity,
        '--theme-card-opacity': theme.cardOpacity
      }
    }
  }
}
</script>

<style>
/* static css variables */
@import './assets/css/variables.css';
</style>

