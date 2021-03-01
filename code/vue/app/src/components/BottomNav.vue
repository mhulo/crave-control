<template>
  <div id="bottom-nav-outer">
    <div id="bottom-nav-inner">
      <div class="bottom-link-bg" :style="bgTransform"></div>
      <div v-for="(link, key) in bottomNavData" :key="'bottom+'+key">
        <a :class="'bottom-link-container ' + link.active" v-on:click="handleNavClick(key)">
          <v-icon class="bottom-nav-icon">{{ link.icon }}</v-icon>
          <span class="link-text">{{ link.text }}</span>
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
      let popupShow = true
      if ((navIndex == this.navIndex) && (this.$store.state.popupData.show == true)) {
        popupShow = false
      }
      let popupData = {
        'show': popupShow,
        'source' : 'nav',
        'key' : this.navData.[navIndex].text
      }
      this.$store.dispatch('updatePopup', popupData)
      this.$store.dispatch('updateNav', navIndex)
    }
  },
  computed: {
    navData() {
      return this.$store.state.navData
    },
    navIndex() {
      let rawIndex = this.$store.getters.navIndex
      return (rawIndex < 2) ? rawIndex : 2
    },
    bottomNavData() {
      let moreActive = (this.navIndex < 2) ? '' : 'active'
      let moreData = {
        'text': 'More',
        'icon': 'mdi-dots-horizontal',
        'active': moreActive
      }
      return [
        ...this.$store.state.navData.slice(0, 2),
        moreData
      ]
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
#bottom-nav-outer {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #432fbf;
  border: 0px;
}
#bottom-nav-inner {
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
  font-size: 24px;
}
i.v-icon.bottom-nav-icon {
  color: #9386ea;
  width: 40px;
  height: 44px;
  transform: translateX(30px);
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
a.active .v-icon.bottom-nav-icon {
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
  top: 8px;
  background: #5e4ecb;
  border-radius: 18px;
  width: 90px;
  height: 35px;
  z-index: 0;
  transition: 0.4s cubic-bezier(0.7, 0, 0.38, 0.86) all;
}
</style>
