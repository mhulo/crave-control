<template>
  <v-main>
    <div id="outer-container">

      <div class="left-container" v-show="layoutSize=='large'">
        <div class="logobar large">
          &lt; crave control &gt;
        </div>
        <div class="nav-secondary">
          <NavSecondary/>
        </div>

        <div class="nav-large" v-show="layoutSize=='large'">
          <NavPrimaryLarge/>
        </div>

        <div class="infobar">{{ socketState }}</div>
      </div>

      <div :class="'right-container '+layoutSize">
        <div class="logobar small" v-show="layoutSize=='small'">
          &lt; crave control &gt;
        </div>
        <div :class="'headerbar '+layoutSize">
          <div class="things-title">
            <div>{{ upperFirst(nav.selected.secondary.name[0]) }}</div>
            <div class="title-chevron"><v-icon>mdi-chevron-right</v-icon></div>
            <div>{{ nav.selected.secondary.name[1] }}</div>
          </div>
          <div>search..</div>
        </div>
        <div class="cards">
          <CardList/>
        </div>
        <transition name="slide-popup">
          <div :class="'popup-area '+layoutSize" v-show="popup.show"><MainPopup/></div>
        </transition>
        <div class="nav-small" v-show="layoutSize == 'small'">
          <NavPrimarySmall/>
        </div>
      </div>

    </div>
  </v-main>
</template>

<script>
import upperFirst from 'lodash/upperFirst'
import NavPrimaryLarge from '@/components/layout1/NavPrimaryLarge.vue'
import NavPrimarySmall from '@/components/layout1/NavPrimarySmall.vue'
import NavSecondary from '@/components/layout1/NavSecondary.vue'
import MainPopup from '@/components/layout1/MainPopup.vue'
import CardList from '@/components/layout1/CardList.vue'

export default {
  props: {},
  components: {
    NavPrimaryLarge,
    NavPrimarySmall,
    NavSecondary,
    MainPopup,
    CardList
  },
  data() {
    return {
      upperFirst: upperFirst,
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
    background: url('~@/assets/img/bg3.jpg') no-repeat top fixed;
    background-size: cover;
  }
  .left-container {
    height: 100%;
    width: 330px;
    min-width: 330px;
    display: flex;
    flex-direction: column;
    margin: 0px;
    background: rgba(0,0,0,0.75);
    border: 0px red solid;
  }
  .right-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    flex-grow: 1;
    border: 0px orange solid;
  }
  .right-container.large {
    padding-bottom: 10px;
  }
  .logobar {
    height: 40px;
    width: 100%;
    display: flex;
    justify-content: center;
    font-size: 20px;
    font-weight: 500;
    padding-top: 15px;
    color: rgba(255, 255, 255, 0.5);
    border: 0px blue solid;
  }
  .logobar.small {
    height: 40px;
    width: 100%;
    display: flex;
    justify-content: start;
    font-size: 20px;
    font-weight: 500;
    padding: 4px 10px 0px 10px;
    color: white;
    border: 0px blue solid;
  }
  .headerbar {
    height: 60px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 20px;
    font-weight: 400;
    padding: 0px 11px;
    color: rgba(0,0,0,0.7);
    border: 0px blue solid;
  }
  .headerbar.small {
    height: 50px;
    width: 100%;
    font-size: 16px;
    line-height: 26px;
    padding: 0px 15px;
    margin-bottom: 10px;
    color: white;
    background: rgba(0,0,0,0.75);
    border: 0px blue solid;
  }
  .things-title {
    display: flex;
  }
  .nav-large {
    display: flex;
    height: 50px;
    width: 100%;
    min-width: 100%;
    border: 0px red solid;
  }
  .infobar {
    height: 40px;
    width: 100%;
    color: white;
    font-size: 12px;
    padding: 10px 12px;
  }
  .popup-area {
    position: absolute;
    z-index: 1000;
    bottom: 50px;
    width: 100%;
    height: calc(100% - 130px);
    overflow-x: auto;
    background: rgba(0,0,0,0.95);
  }
  .popup-area.large {
    width: calc(100% - 330px);
    height: 100%;
    bottom: 0px;
  }
  .cards {
    width: 100%;
    min-height: 0px;
    height: 10px;
    flex: 1 1 auto;
    overflow-y: auto;
  }
  .nav-secondary {
    width: 100%;
    flex-grow: 1;
    height: 10px;
    border: 0px green solid;
  }
  .nav-small {
    height: 50px;
    width: 100%;
    z-index: 1100;
    border: 0px blue solid;
  }
  .title-chevron .v-icon {
    width: 20px;
    font-size: 14px;
    padding-bottom: 0px;
    color: rgba(0,0,0,0.7);
    border: 0px red solid;
  }
  .small .title-chevron .v-icon {
    color: white;
  }

</style>
