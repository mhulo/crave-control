<template>
  <div id="sec-nav-outer">
    <div class="sec-nav-title">
      <div>{{ navSelected.primary.name }}</div>
      <!--<div class="things-chevron"><v-icon>mdi-chevron-down</v-icon></div>-->
    </div>
    <div class="sec-nav-buttons">
      <div v-for="(item, key) in navSecondary" :key="'secondary_'+key">
        <button v-ripple :class="'sec-nav-button ' + item.active" v-on:click="handleNavClick(key)">
          <v-icon class="sec-nav-icon">{{ item.icon }}</v-icon>
          {{ item.name }}
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
    handleNavClick(navIndex) {
      this.$store.dispatch('updateNav', { key: 'secondary', val: navIndex })
      this.$store.dispatch('updatePopup', { 'show' : false })
    }
  },
  computed: {
    navSelected() {
      return this.$store.state.nav.selected
    },
    navSecondary() {
      return this.$store.getters.navSecondary
    }
  },
  watch: {},
  mounted() {}
}
</script>

<style>
#sec-nav-outer {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  flex: 1 auto;
  border: 0px;
  padding: 5px 10px;
  border: 0px yellow solid;
}
.sec-nav-title {
  color: white;
  display: flex;
  padding: 5px 12px;
  font-size: 13px;
  font-weight: bold;
  border: 0px orange solid;  
}
.sec-nav-buttons {
  color: white;
  display: flex;
  flex-direction: column;
  overflow-x: auto;
  padding: 0px;
  font-size: 14px;
  border: 0px red solid;  
}
.things-chevron .v-icon {
  width: 24px;
  font-size: 14px;
  padding-left: 0px;
  color: white;
  border: 0px red solid;
}
.sec-nav-button {
  display: flex;
  align-items: center;
  width: 100%;
  overflow: hidden;
  margin-bottom: 0px;
  padding: 5px 5px; 
  color: white;
  border-bottom: 0px rgb(59, 59, 59) solid;
  border-radius: 5px;
  background: #12b2d39;
  font-size: 12px;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
.nav-button-sec.active {}

.sec-nav-button:hover {
  background: #2b2d39;
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
i.v-icon.sec-nav-icon {
  color: white;
  width: 40px;
  height: 44px;
  font-size: 20px;
  transform: translateX(0px);
  transition: 0.4s ease all;
}
</style>
