<template>
  <div id="popup-outer">
    <div>popup: {{ nav.selected.primary.name }}</div>
    <div v-for="(item, key) in navButtons" :key="'secondary_'+key">
    <button v-ripple :class="'nav-button-sec ' + item.active" v-on:click="handleNavClick(key)">
      {{ item.name }}
    </button>
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
    handleNavClick(navIndex) {
      this.$store.dispatch('updateNavSelected', { key: 'secondary', val: navIndex })
    }
  },
  computed: {
    nav() {
      return this.$store.state.nav
    },
    navButtons() {
      return this.$store.getters.navSecondary
    }
  },
  watch: {},
  mounted() {}
}
</script>

<style>
#popup-outer {
  width: 100%;
  height: 100%;
  border: 0px;
  padding-top: 18px;
}
#side-nav-inner {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
}
.link-div {
  padding-left: 7px;
  padding-bottom: 18px;
  font-size: 24px;
  border: 0px green solid;

}
.nav-button-sec {
  display: flex;
  align-items: center;
  height: 36px;
  width: 200px;
  overflow: hidden;
  margin-bottom: 10px;
  background: orange;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
.nav-button-sec.active, .nav-button-sec:hover {
  background: red;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
i.v-icon.side-nav-icon {
  color: #9386ea;
  width: 40px;
  height: 44px;
  transform: translateX(0px);
  transition: 0.4s ease all;
}
</style>
