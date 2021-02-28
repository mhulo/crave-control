<template>
  <v-main>
    <div id="outer-container">
      <div class="left-container" v-show="oLarge">
        <SideNav/>
      </div>
      <div class="middle-container" v-show="oLarge">
        <div class="headerbar">&lt; logo &gt;</div>
        <div class="titlebar">titlebar</div>
        <div class="things">things</div>
        <div class="infobar">infobar</div>
      </div>
      <div class="right-container">
        <div class="headerbar" v-show="!oLarge">&lt; crave control &gt;</div>
        <div class="infobar" v-show="!oLarge">infobar</div>
        <div class="cards">
          <CardList/>
        </div>
        <transition name="slide-popup">
          <div class="popup-area" v-show="popupKey && !oLarge">popup: {{ popupKey }}</div>
        </transition>
        <div class="bottom-nav" v-show="!oLarge">
          <BottomNav/>
        </div>
      </div>
    </div>
  </v-main>
</template>

<script>
import BottomNav from '@/components/BottomNav.vue'
import SideNav from '@/components/SideNav.vue'
import CardList from '@/components/CardList.vue'

export default {
  props: {},
  components: {
    BottomNav,
    SideNav,
    CardList
  },
  data() {
    return {
      oHeight: 0,
      oWidth: 0,
      oLarge: false
    }
  },
  methods: {
    updateSizes() {
      this.oHeight = document.getElementById('outer-container').offsetHeight
      this.oWidth = document.getElementById('outer-container').offsetWidth
      if (this.oWidth >= 940) { 
        this.oLarge = true
        if (this.popupKey != null) {
          this.$store.dispatch('updateVal', { 'obj' : 'popupKey', 'val' : null })
        }
      }
      else {
        this.oLarge = false
      }
    }
  },
  computed: {
    popupKey() {
      return this.$store.state.popupKey
    },
  },
  watch: {},
  created() {
    console.log('layout created')
  },
  mounted() {
    console.log('layout mounted')
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
    height: calc(100% - 90px);
    background: lightgreen;
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
    background: lightgreen;
  }
  .bottom-nav {
    height: 50px;
    width: 100%;
    background: yellow;
  }
</style>
