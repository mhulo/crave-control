<template>
  <div id="side-nav-outer">
    <div id="side-nav-inner">
      <div class="link-div" v-for="(item, key) in navButtons" :key="'side_'+key">
        <button v-ripple :class="'nav-button ' + item.active" v-on:click="handleNavClick(key)">
          <v-icon class="side-nav-icon">{{ item.icon }}</v-icon>
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
      this.$store.dispatch('updateNav', { key: 'primary', val: navIndex })
    }
  },
  computed: {
    navButtons() {
      let primary = [ ...this.$store.state.nav.primary ]
      let selected = { ...this.$store.state.nav.selected }
      return primary.map((x, idx) => {
        (idx == selected.primary.index) ? x['active'] = 'active' : x['active'] = ''
        return x
      })
    }
  },
  watch: {},
  mounted() {}
}
</script>

<style>
#side-nav-outer {
  width: 100%;
  display: flex;
  flex-direction: column;
  min-height: 10px;
  height: 10px;
  flex: 1;
  justify-content: center;
  border: 0px black solid;
}
#side-nav-inner {
  width: 100%;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  overflow-x: auto;
  border: 0px blue solid;
}
.link-div {
  padding-left: 7px;
  padding-bottom: 18px;
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
  /*background: orange;*/
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
.nav-button.active, .nav-button:hover {
  /*background: #2b2d39;*/
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
i.v-icon.side-nav-icon {
  color: #a3a3a3;
  width: 40px;
  height: 44px;
  font-size: 20px;
  transform: translateX(0px);
  transition: 0.4s ease all;
}
.active i.v-icon.side-nav-icon {
  color: white;
}
</style>
