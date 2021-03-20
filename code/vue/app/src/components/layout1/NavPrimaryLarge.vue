<template>
  <div id="nav-large-outer">
    <div id="nav-large-inner">
      <div class="link-div" v-for="(item, key) in navButtons" :key="'side_'+key">
        <button v-ripple :class="'nav-button ' + item.active" v-on:click="handleNavClick(key)">
          <v-icon class="nav-large-icon">{{ item.icon }}</v-icon>
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
#nav-large-outer {
  height: 100%;
  width: 100%;
  display: flex;
  flex: 1;
  justify-content: center;
  border: 0px blue solid;
}
#nav-large-inner {
  height: 100%;
  display: flex;
  overflow-x: auto;
  border: 0px green solid;
}
.link-div {
  padding: 4px 10px 0px 10px;
  padding-bottom: 0px;
  font-size: 24px;
  border: 0px green solid;
}
.nav-button {
  display: flex;
  align-items: center;
  height: 40px;
  width: 40px;
  overflow: hidden;
  border-radius: 100%;
  /*background: orange;*/
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
.nav-button.active, .nav-button:hover {
  background: rgba(255, 255, 255, 0.1);
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
i.v-icon.nav-large-icon {
  color: rgba(255, 255, 255, 0.5);
  width: 40px;
  height: 44px;
  font-size: 22px;
  transform: translateX(0px);
  transition: 0.4s ease all;
}
.active i.v-icon.nav-large-icon {
  color: white;
}
</style>
