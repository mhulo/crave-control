<template>
  <div :class="'popup-outer '+popup.type">
    <div v-if="popup.type == 'nav'" class="popup-nav">
      <component :is="popup.component" key="popup_comp"/>
    </div>
    <div v-else-if="popup.type == 'card'">
      <component
        :is="popup.component"
        key="popup_comp"
        :card="popup.params.card"
        :options="cardOptions"
      />
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
      cards: {},
      cardOptions: {
        'show': 'full'
      }
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
.popup-outer {
  width: 100%;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 0px red solid;
  background: rgba(43, 43, 43, 0.4);
}
.large .popup-outer {
  padding: 30px;
} 
.small .popup-outer {
  padding: 10px;
} 
.small .popup-outer.nav {
  justify-content: flex-end;
  padding: 0px;
  border: 0px red solid;
}
.popup-outer.nav {
  padding: 20px 0px 0px 0px;
  background: rgba(0, 0, 0, 0.4);
}
.popup-nav {
  background: rgba(0,0,0,0.7);
  border: 0px blue solid;
  padding-top: 20px;
  padding-left: 0px;
}

</style>
