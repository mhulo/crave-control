<template>
  <div id="popup-outer">
    <div v-if="popup.type == 'nav'" class="popup-nav">
      <component :is="popup.component" key="popup_comp"/>
    </div>
    <div v-else-if="popup.type == 'card'">
      <component :is="popup.component" key="popup_comp" :card="popup.params.card"/>
    </div>
  </div>
</template>

<script>
import NavSecondary from '@/components/layout1/NavSecondary.vue'

export default {
  props: {},
  components: {
    NavSecondary
  },
  data() {
    return {
      imported: [],
      cards: {}
    }
  },
  methods: {
    importCards() {
      Object.entries(this.$store.getters.cards).forEach(([k, v]) => {
        let i = v['card']
        if (!this.imported.includes(i)) {
          this.$options.components[i] = () => import('@/components/cards/' + i + '.vue')
          this.imported.push(i)
        }
      })
      this.cards = this.stateCards
    },
  },
  computed: {
    stateCards() {
      return this.$store.getters.cards
    },
    popup() {
      return this.$store.state.popup
    },
    title() {
      let title = ''
      if (this.popup.type == 'nav') {
        let nav = this.$store.state.nav
        title = (nav.selected.primary.index < 2) ?
          nav.selected.primary.name :
          'More'
      }
      return title
    }
  },
  watch: {
    stateCards() {
      this.importCards()
    }
  },
  created() {
    this.importCards()
  },
  mounted() {}
}
</script>

<style>
#popup-outer {
  width: 100%;
  min-height: 100%;
  display: flex;
  flex-direction:column;
  border: 0px;
}
.large #popup-outer {
  justify-content:center;
  padding: 30px;
} 
.small #popup-outer {
  justify-content:flex-end;
  padding-top: 20px;
  padding-bottom: 20px;
}
.popup-nav {
  border: 0px blue solid;
  background: #141414;
}
</style>
