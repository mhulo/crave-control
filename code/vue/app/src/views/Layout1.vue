<template>
  <v-main>
    <div id="outer-container">
      <div class="left-container" v-show="layoutSize == 'large'">
        <NavPrimarySide/>
      </div>
      <div class="middle-container" v-show="layoutSize == 'large'">
        <div class="logobar">&lt; crave control &gt;</div>
        <div class="middle-wrapper">
          <div class="middle-wrapper-inner">
            <div class="things">
              <NavSecondary/>
            </div>
            <div class="infobar">{{ socketState }}</div>
          </div>
        </div>
      </div>
      <div class="right-container">
        <div class="searchbar">
          <div>search..</div>
          <div>{{ nav.selected.secondary.name[0] }} >> {{ nav.selected.secondary.name[1] }}</div>
        </div>
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
    /*background: red;*/
    background: url('~@/assets/img/bg3.jpg') no-repeat center center fixed;
  }
  .left-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 50px;
    min-width: 50px;
  }
  .middle-container {
    height: 100%;
    width: 240px;
    min-width: 240px;
    display: flex;
    flex-direction: column;
  }
  .middle-wrapper {
    width: 100%;
    flex-grow: 1;
    display: flex;
    padding: 0px 0px 10px 0px;
  }
  .middle-wrapper-inner {
    width: 100%;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    border: 0px blue solid;
    background: rgba(0,0,0,0.6);
    overflow: hidden;
  }
  .right-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    flex-grow: 1;
    padding-bottom: 10px;
    border: 0px orange solid;
  }
  .logobar {
    height: 30px;
    width: 100%;
    display: flex;
    justify-content: center;
    font-size: 20px;
    font-weight: 500;
    line-height: 26px;
    color: white;
    border: 0px blue solid;
  }
  .searchbar {
    height: 30px;
    width: 100%;
    display: flex;
    justify-content: space-between;
    font-size: 16px;
    line-height: 26px;
    padding: 0px 11px;
    color: white;
    border: 0px blue solid;
  }
  .headerbar {
    height: 30px;
    width: 100%;
    font-size: 20px;
    line-height: 26px;
    padding: 0px 15px;
    color: white;
    border: 0px blue solid;
  }
  .popup-area {
    position: absolute;
    z-index: 1000;
    bottom: 50px;
    width: 100%;
    height: calc(100% - 130px);
    overflow-x: auto;
    background: #252525;
  }
  .popup-area.large {
    width: calc(100% - 290px);
    height: 100%;
    bottom: 0px;
  }
  .titlebar {
    width: 100%;
    displax: flex;
    color: white;
    padding: 0px 15px;
    font-size: 14px;
    border: 0px blue solid;
  }
  .titlebar-inner {
    width: 100%;
    display: flex;
    justify-content: center;
    color: white;
    padding: 5px 10px;
    font-size: 12px;
    border-radius: 5px;
    background-image: linear-gradient(155deg, #184886, #30176b);
    border: 0px red solid;
  }
  .infobar {
    height: 40px;
    width: 100%;
    color: white;
    font-size: 12px;
    padding: 10px 12px;
  }
  .cards {
    width: 100%;
    min-height: 0px;
    height: 10px;
    flex: 1 1 auto;
    overflow-y: auto;
  }
  .things {
    width: 100%;
    flex-grow: 1;
    height: 10px;
    border: 0px green solid;
  }
  .bottom-nav {
    height: 50px;
    width: 100%;
    z-index: 1100;
  }
  .titlebar.small {
    color: white;
    padding: 5px 15px;
    display: flex;
    justify-content: center;
  }
  .title-chevron .v-icon {
    width: 20px;
    font-size: 14px;
    padding-bottom: 0px;
    color: white;
    border: 0px red solid;
  }
  .title-thing {
    text-overflow: ellipsis;
  }

</style>
