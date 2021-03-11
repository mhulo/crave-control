<template>
  <v-main>
    <div id="outer-container">
      <div class="left-container" v-show="layoutSize == 'large'">
        <NavPrimarySide/>
      </div>
      <div class="middle-container" v-show="layoutSize == 'large'">
        <div class="headerbar">&lt; crave control &gt;</div>
        <div :class="'titlebar '+layoutSize">
          <div>{{ nav.selected.secondary.name[0] }}</div>
          <div class="title-chevron"><v-icon>mdi-chevron-right</v-icon></div>
          <div class="title-thing">{{ nav.selected.secondary.name[1] }}</div>
        </div>
        <div class="things">
          <NavSecondary/>
        </div>
        <div class="infobar">{{ socketState }}</div>
      </div>
      <div class="right-container">
        <div class="headerbar" v-show="layoutSize == 'small'">&lt; crave control &gt;</div>
        <div :class="'titlebar '+layoutSize" v-show="layoutSize == 'small'">{{ nav.selected.secondary.name[0] }} >> {{ nav.selected.secondary.name[1] }}</div>
        <div class="cards">
          <CardList/>
        </div>
        <transition name="slide-popup">
          <div :class="'popup-area '+layoutSize" v-show="popup.show"><MainPopup/></div>
        </transition>
        <div class="bottom-nav" v-show="layoutSize == 'small'">
          <NavPrimaryBottom/>
        </div>
      </div>
    </div>
  </v-main>
</template>

<script>
import NavPrimarySide from '@/components/layout1/NavPrimarySide.vue'
import NavPrimaryBottom from '@/components/layout1/NavPrimaryBottom.vue'
import NavSecondary from '@/components/layout1/NavSecondary.vue'
import MainPopup from '@/components/layout1/MainPopup.vue'
import CardList from '@/components/layout1/CardList.vue'

export default {
  props: {},
  components: {
    NavPrimarySide,
    NavPrimaryBottom,
    NavSecondary,
    MainPopup,
    CardList
  },
  data() {
    return {
      layoutSize: 'small'
    }
  },
  methods: {
    updateSizes() {
      let width = document.getElementById('outer-container').offsetWidth
      this.layoutSize = (width > 940)? 'large' : 'small'
      this.$store.dispatch('updatePopup', { 'show' : false })
    }
  },
  computed: {
    nav() {
      return this.$store.state.nav
    },
    popup() {
      return this.$store.state.popup
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
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateSizes)
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
    transition: all 0.2s ease-out;
  }
  .slide-popup-leave-active {
    transition: all 0.2s ease-in;
  }
  .slide-popup-enter {
    transform: translateY(30px);
  }
  .slide-popup-leave-to {
    transform: translateY(30px);
  }

  #outer-container {
    display: flex;
    height: 100%;
    font-family: 'Montserrat', sans-serif;
  }
  .left-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 50px;
    min-width: 50px;
    background: cyan; 
  }
  .middle-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 240px;
    min-width: 240px;
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
    font-size: 22px;
    padding: 3px 0px 0px 24px;
    color: white;
    background: #1d1d1d;
  }
  .popup-area {
    position: absolute;
    z-index: 1000;
    bottom: 50px;
    width: 100%;
    height: calc(100% - 120px);
    overflow-x: auto;
    background: #252525;
  }
  .popup-area.large {
    width: calc(100% - 290px);
    height: 100%;
    bottom: 0px;
  }
  .titlebar {
    height: 30px;
    width: 100%;
    display: flex;
    color: white;
    padding: 3px 0px 0px 12px;
    font-size: 14px;
    background: #1d1d1d;
  }
  .infobar {
    height: 50px;
    width: 100%;
    color: white;
    font-size: 14px;
    padding: 14px 0px 0px 12px;
    background:#1d1d1d;
  }
  .cards {
    width: 100%;
    min-height: 0px;
    height: 10px;
    flex: 1 1 auto;
    overflow-y: auto;
    background: #252525;
  }
  .things {
    width: 100%;
    flex-grow: 1;
    height: 10px;
    overflow-x: auto;
    background: #1d1d1d;
  }
  .bottom-nav {
    height: 50px;
    width: 100%;
    z-index: 1100;
    background: yellow;
  }
  .titlebar.small {
    color: white;
    display: flex;
    justify-content: center;
  }
  .title-chevron .v-icon {
    width: 24px;
    font-size: 14px;
    padding-bottom: 0px;
    color: white;
    border: 0px red solid;
  }
  .title-thing {
    text-overflow: ellipsis;
  }

</style>
