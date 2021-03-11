<template>
  <div id="secondary-side-nav-outer">
    <div v-for="(item, key) in navButtons" :key="'secondary_'+key">
      <button v-ripple :class="'nav-button-sec ' + item.active" v-on:click="handleNavClick(key)">
        <v-icon class="sec-nav-icon">{{ item.icon }}</v-icon>
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
      this.$store.dispatch('updateNav', { key: 'secondary', val: navIndex })
      this.$store.dispatch('updatePopup', { 'show' : false })
    }
  },
  computed: {
    navButtons() {
      return this.$store.getters.navSecondary
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
  width: 240px;
  overflow: hidden;
  margin-bottom: 0px;
  padding: 8px 0px 8px 3px; 
  font-size: 14px;
  color: white;
  background: #1d1d1d;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
.nav-button-sec.active {}

.nav-button-sec:hover {
  background: #252525;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
i.v-icon.sec-nav-icon {
  color: white;
  width: 40px;
  height: 44px;
  transform: translateX(0px);
  transition: 0.4s ease all;
}
</style>
