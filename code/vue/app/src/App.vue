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
        color1: '#1d2225', 
        color2: '#1d2225', 
        sideOpacity: '0.6',
        cardOpacity: '0.4',
        gradDeg: '45deg',
        bgColor1: '#0b1114', 
        bgColor2: '#363e41', 
        bgGradDeg: '-45deg'
      },
      blue1: {
        color1: '#1f1f42', 
        color2: '#1c1c5f', 
        sideOpacity: '0.6',
        cardOpacity: '0.4',
        gradDeg: '45deg',
        bgColor1: '#3c415a', 
        bgColor2: '#000000', 
        bgColor3: '#0b1114', 
        bgGradDeg: '-45deg'
      },
      blue2: {
        color1: '#3f35d8', 
        color2: '#191558', 
        sideOpacity: '0.6',
        cardOpacity: '0.4',
        gradDeg: '45deg',
        bgColor1: '#000000', 
        bgColor2: '#3f35d8', 
        bgGradDeg: '-45deg'
      }
    }
  },
  computed: {
    // dynamic css variables
    cssVars () {
      let theme = this.[this.selected]
      return {
        '--theme-color-1': theme.color1,
        '--theme-color-2': theme.color2,
        '--theme-side-opacity': theme.sideOpacity,
        '--theme-card-opacity': theme.cardOpacity,
        '--theme-grad-deg': theme.gradDeg,
        '--theme-bg-color-1': theme.bgColor1,
        '--theme-bg-color-2': theme.bgColor2,
        '--theme-bg-grad-deg': theme.bgGradDeg
      }
    }
  }
}
</script>

<style>
/* static css variables */
@import './assets/css/variables.css';
</style>

