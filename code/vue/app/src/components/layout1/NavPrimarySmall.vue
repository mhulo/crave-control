<template>
  <div id="nav-small-outer">
    <div id="nav-small-inner">
      <div class="bottom-link-bg" :style="bgTransform"></div>
      <div v-for="(item, key) in navButtons" :key="'bottom_'+key">
        <a :class="'bottom-link-container ' + item.active" v-on:click="handleNavClick(key)">
          <v-icon class="nav-small-icon">{{ item.icon }}</v-icon>
          <span class="link-text">{{ item.name }}</span>
        </a>
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
      let navPath = '/cards/nav/' + navIndex + '/'
      if (this.$route.path !== navPath) { this.$router.push({ path: navPath }) }
      else { this.$router.push({ path: '/cards/' }) }
    }
  },
  computed: {
    navIndex() {
      let rawIndex = this.$store.state.nav.selected.primary.index
      return (rawIndex < 2) ? rawIndex : 2
    },
    navButtons() {
      let more = {
        'name': 'more',
        'icon': 'mdi-dots-horizontal',
      }
      let primary = [...this.$store.state.nav.primary.slice(0, 2), more]
      return primary.map((x, idx) => {
        (idx == this.navIndex) ? x['active'] = 'active' : x['active'] = ''
        return x
      })
    },
    bgTransform() {
      return `transform: translateX(${100 * this.navIndex}px)`
    }
  },
  watch: {},
  mounted() {}
}
</script>

<style>
#nav-small-outer {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000000;
}
#nav-small-inner {
  position: relative;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Roboto";
}
a {
  cursor: pointer;
  display: flex;
  align-items: center;
  height: 50px;
  width: 100px;
  overflow: hidden;
}
.bottom-link-container {
}
i.v-icon.nav-small-icon {
  width: 40px;
  height: 44px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 20px;
  transform: translateX(30px);
  border: 0px blue solid;
  transition: 0.4s ease all;
}
.link-text {
  color: white;
  margin-left: 1px;
  opacity: 0;
  transition: 0.3s ease all;
  user-select: none;
  height: 44px;
  width: 44px;
  font-size: 13px;
  display: inline-block;
  text-align: center;
  padding-top: 12px;
  z-index: 1;
}
a.active .v-icon.nav-small-icon {
  color: white;
  transform: translateX(7px);
}
a.active .link-text {
  opacity: 1;
  transition-delay: 0.1s;
  padding-left: 0px;
}
.bottom-link-bg {
  position: absolute;
  left: 5px;
  top: 9px;
  background-image: linear-gradient(var(--theme-hl-grad-deg), var(--theme-hl-color-1), var(--theme-hl-color-2));
  border-radius: 18px;
  width: 90px;
  height: 32px;
  z-index: 0;
  transition: 0.4s cubic-bezier(0.7, 0, 0.38, 0.86) all;
}
</style>
