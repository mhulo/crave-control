<template>
  <div id="side-nav-outer">
    <div id="side-nav-inner">
      <!--<div class="link-bg" :style="bgTransform"></div>-->
      <div class="link-div" v-for="(link, key) in navData" :key="'side_'+key">
        <button :class="'nav-button ' + link.active" v-on:click="handleNavClick(key)">
          <v-icon class="nav-icon">{{ link.icon }}</v-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: {},
  components: {},
  data() {
    return {}
  },
  methods: {
    handleNavClick(navKey) {
      let navData = [...this.$store.state.navData]
      if (navData.[navKey].text == this.$store.state.popupKey) {
        this.$store.dispatch('updateVal', { 'obj' : 'popupKey', 'val' : null })
      }
      else {
        navData.forEach(val => { val.active = '' })
        navData.[navKey].active = 'active'
        this.$store.dispatch('updateVal', { 'obj' : 'navData', 'val' : navData })
        this.$store.dispatch('updateVal', { 'obj' : 'popupKey', 'val' : navData.[navKey].text })
      }
    }
  },
  computed: {
    navData() {
      return this.$store.state.navData
    }
  },
  watch: {},
  mounted() {}
}
</script>

<style>
#side-nav-outer {
  width: 100%;
  height: 10px;
  flex: 1 1 auto;
  overflow-y: auto;
  border: 0px;
  padding-top: 10px;
}
#side-nav-inner {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
}
.link-div {
  padding-left: 7px;
  padding-bottom: 15px;
  font-size: 24px;
  border: 0px green solid;

}
.nav-button {
  display: flex;
  align-items: center;
  height: 36px;
  width: 36px;
  overflow: hidden;
  border-radius: 100%;
  background: orange;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
.nav-button.active, .nav-button:hover {
  background: red;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
i.v-icon.nav-icon {
  color: #9386ea;
  width: 40px;
  height: 44px;
  transform: translateX(0px);
  transition: 0.4s ease all;
}
</style>
