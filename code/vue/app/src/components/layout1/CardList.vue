<template>
  <div id="card-list">
    <div :class="'card-wrapper '+layoutCols" v-for="(val, key) in filteredCards" :key="key+'_wrapper'">
      <component :is="val.card" :key="key" :card="val"/>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      layoutCols: 'cols-1',
      imported: [],
      cards: {}
    }
  },
  methods: {
    updateSizes() {
      let width = document.getElementById('card-list').offsetWidth
      this.layoutCols = (width > 1300) ? 'cols-3'
        : (width > 650) ? 'cols-2'
        : 'cols-1'
    },
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
    filteredCards() {
      let cards = this.$store.getters.cards
      let filters = this.$store.state.nav.selected.secondary.name
      let filtered = {}
      if (filters[1] != '') {
        Object.entries(cards).forEach(([k, v]) => {
          if (filters[0].toLowerCase() in v) {
            if (v[filters[0].toLowerCase()].includes(filters[1])) {
              filtered[k] = v
            }
          }
        })
      }
      else {
        filtered = cards
      }
      return filtered
    }
  },
  watch: {
    stateCards() {
      this.importCards()
    }
  },
  created() {
    console.log('cards created')
    this.$store.dispatch('startSocket')
    this.importCards()
    this.$store.dispatch('updateCards')
  },
  mounted() {
    this.updateSizes()
    window.addEventListener('resize', this.updateSizes)
    //console.log(this.$store.getters.navSecondary)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateSizes)
  }
}
</script>

<style>
  #card-list {
    display: flex;
    flex-wrap: wrap;
    padding: 0px 5px 0px 5px;
  }
  .card-wrapper {
    width: 100%;
    padding: 0px 5px 10px 5px;
  }

  .card-wrapper.cols-2 {
      width: 50%;
    }

  .card-wrapper.cols-3 {
      width: 33%;
  }
</style>
