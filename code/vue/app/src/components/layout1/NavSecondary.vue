<template>
  <div id="sec-nav-outer">
    <div class="sec-nav-title">
      <div>{{ upperFirst(navSelected.primary.name) }}</div>
      <div class="things-chevron"><v-icon>mdi-chevron-down</v-icon></div>
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
import upperFirst from 'lodash/upperFirst'

export default {
  props: {},
  components: {},
  data() {
    return {
      upperFirst: upperFirst
    }
  },
  methods: {
    handleNavClick(navIndex) {
      this.$store.dispatch('updateNav', { key: 'secondary', val: navIndex })
      let navPath = '/cards/'
      if (this.$route.path !== navPath) { this.$router.push({ path: navPath }) }
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
  watch: {
    $route(to, from) {
      if ('navIndex' in this.$route.params) {
        let navIndex = parseInt(this.$route.params.navIndex)
        this.$store.dispatch('updateNav', { key: 'primary', val: navIndex })
      }
    }
  },
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
  padding-bottom: 15px;
  border: 0px yellow solid;
}
.sec-nav-title {
  color: white;
  display: flex;
  padding: 20px 15px 5px 15px;
  font-size: 16px;
  border: 0px orange solid;  
}
.sec-nav-buttons {
  color: white;
  display: flex;
  flex-direction: column;
  overflow-x: auto;
  padding-bottom: 20px;
  border: 0px red solid;  
}
.things-chevron .v-icon {
  width: 24px;
  font-size: 16px;
  padding-left: 5px;
  color: white;
  border: 0px red solid;
}
.sec-nav-button {
  display: flex;
  align-items: center;
  width: 100%;
  overflow: hidden;
  padding: 5px 25px; 
  color: white;
  border-bottom: 0px red solid;
  border-radius: 0px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
.active.sec-nav-button {
  color: white;
  background-image: linear-gradient(var(--theme-grad-deg), var(--theme-color-1), var(--theme-color-2));
}
.small .active.sec-nav-button {
  color: white;
  background: rgba(255, 255, 255, 0.15);
}
.sec-nav-button:hover {
  background: rgba(255, 255, 255, 0.1);
  -webkit-transition: background-color 0.3s linear;
  -ms-transition: background-color 0.3s linear;
  transition: background-color 0.3s linear;
}
i.v-icon.sec-nav-icon {
  color: rgba(255, 255, 255, 0.5);
  width: 40px;
  height: 44px;
  font-size: 22px;
  margin-right: 3px;
  transform: translateX(0px);
  transition: 0.4s ease all;
}
.active i.v-icon.sec-nav-icon {
  color: white;
}
</style>
