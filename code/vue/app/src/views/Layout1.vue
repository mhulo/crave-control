<template>
  <v-main>
    <div id="outer-container">
      <div class="left-container" v-show="isLarge">
        <NavPrimarySide/>
      </div>
      <div class="middle-container" v-show="isLarge">
        <div class="headerbar">&lt; logo &gt;</div>
        <div class="titlebar">{{ nav.selected.secondary.name[0] }} >> {{ nav.selected.secondary.name[1] }}</div>
        <div class="things">
          <NavSecondarySide/>
        </div>
        <div class="infobar">{{ socketState }}</div>
      </div>
      <div class="right-container">
        <div class="headerbar" v-show="!isLarge">&lt; logo &gt;</div>
        <div class="titlebar" v-show="!isLarge">{{ nav.selected.secondary.name[0] }} >> {{ nav.selected.secondary.name[1] }}</div>
        <div class="cards">
          <CardList/>
        </div>
        <transition name="slide-popup">
          <div :class="'popup-area '+oStyle" v-show="nav.popup"><MainPopup/></div>
        </transition>
        <div class="bottom-nav" v-show="!isLarge">
          <NavPrimaryBottom/>
        </div>
      </div>
    </div>
  </v-main>
</template>

<script>
import NavPrimarySide from '@/components/layout1/NavPrimarySide.vue'
import NavPrimaryBottom from '@/components/layout1/NavPrimaryBottom.vue'
import NavSecondarySide from '@/components/layout1/NavSecondarySide.vue'
import MainPopup from '@/components/layout1/MainPopup.vue'
import CardList from '@/components/layout1/CardList.vue'

export default {
  props: {},
  components: {
    NavPrimarySide,
    NavPrimaryBottom,
    NavSecondarySide,
    MainPopup,
    CardList
  },
  data() {
    return {
      oHeight: 0,
      oWidth: 0,
      oStyle: 'small',
      isLarge: false
    }
  },
  methods: {
    updateSizes() {
      this.oHeight = document.getElementById('outer-container').offsetHeight
      this.oWidth = document.getElementById('outer-container').offsetWidth
      let oStylePrev = this.oStyle
      this.oStyle = (this.oWidth >= 940) ? 'large' : 'small'
      this.isLarge = (this.oStyle == 'large') ? true : false
      if (oStylePrev != this.oStyle) {
        this.$store.dispatch('updateNavPopup', false)
      }
    }
  },
  computed: {
    nav() {
      return this.$store.state.nav
    },
    socketState() {
      return this.$store.state.socket.connected ? 'connected' : 'disconnected'
    }
  },
  watch: {},
  created() {},
  mounted() {
    this.updateSizes()
    window.addEventListener('resize', this.updateSizes)
  }
}
</script>

<style>
  button:focus {
    outline:0;
  }
  .slide-left-enter-active {
    transition: all .3s ease-out;
  }
  .slide-left-leave-active {
    transition: all .2s ease-in;
  }
  .slide-left-enter {
    transform: translateX(-100px);
  }
  .slide-left-leave-to {
    transform: translateX(-100px);
  }
  .slide-popup-enter-active {
    transition: all 0.5s ease-out;
    max-height: 1000px;
  }
  .slide-popup-leave-active {
    transition: all 0.2s ease-in;
    max-height: 1000px;
  }
  .slide-popup-enter {
    max-height: 50%;
  }
  .slide-popup-leave-to {
    max-height: 0%;
  }

  #outer-container {
    display: flex;
    height: 100%;
  }
  .left-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 50px;
    background: cyan; 
  }
  .middle-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 300px;
    background: orange; 
  }
  .right-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    flex-grow: 1;
    background: green;
  }
  .headerbar {
    height: 40px;
    width: 100%;
    background: pink;
  }
  .popup-area {
    position: absolute;
    bottom: 50px;
    width: 100%;
    height: calc(100% - 120px);
    overflow-x: auto;
    background: lightgreen;
  }
  .popup-area.large {
    height: 100%;
    bottom: 0px;
  }
  .titlebar {
    height: 30px;
    width: 100%;
    background: lightblue;
  }
  .infobar {
    height: 50px;
    width: 100%;
    background: lightblue;
  }
  .cards {
    width: 100%;
    min-height: 0px;
    height: 10px;
    flex: 1 1 auto;
    overflow-y: auto;
    background: grey;
  }
  .things {
    width: 100%;
    flex-grow: 1;
    height: 10px;
    overflow-x: auto;
    background: lightgreen;
  }
  .bottom-nav {
    height: 50px;
    width: 100%;
    background: yellow;
  }
</style>
