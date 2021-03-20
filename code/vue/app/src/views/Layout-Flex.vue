<template>
  <v-main>
    <div class="container fill-height">
          <div class="header">crave control</div>
          <div class="left-nav">leftnav</div>
          <div class="main">main</div>
          <div class="nav-small">
          </div>
    </div>
  </v-main>

</template>

<script>
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'
import WsService from '@/services/WsService.js'

export default {
  components: {},
  data() {
    return {
      imported: [],
      cards: {},
      tab: null,
      items: [
        'web', 'shopping', 'videos', 'images', 'news', 'upstairs', 'downstairs', 'devices', 'scenes'
      ]
    }
  },
  methods: {
    UpdateDevices() {
      this.$store.dispatch('fetchDevices')
      setTimeout(() => { this.UpdateDevices() }, 1500)
    },
    ImportCards() {
      Object.entries(this.$store.state.cards).forEach(([k, v]) => {
        let i = v['card']
        if (!this.imported.includes(i)) {
          this.$options.components[i] = () => import('@/components/cards/' + upperFirst(camelCase(i)) + '.vue')
          this.imported.push(i)
        }
      })
    },
  },
  computed: {
    stateCards() {
      return this.$store.state.cards
    },
  },
  watch: {
    stateCards()  {
      this.ImportCards()
      this.cards = this.stateCards
    }
  },
  created() {
    this.$store.dispatch('updateCards')
  },
  mounted() {
    //WsService.reConnect()
  }
}
</script>

<style scoped>
html, body {
  /*font-family: 'Roboto', 'Helvetica', sans-serif;*/
  font-family: 'Montserrat', sans-serif;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
}

.container {
  height: 100vh;
  padding: 0px;
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: minmax(40px, max-content) auto minmax(40px, max-content);
  border: 1px black solid;
}

.header {
  display: flex;
  grid-column: 1/-1;
  border: 1px black solid;
}

.left-nav {
  display: none;
  grid-column: 1/1;
  border: 1px black solid;
}

.main {
  grid-column: 1/-1;
  border: 1px black solid;
}

.nav-small {
  grid-column: 1/-1;
  border: 1px black solid;
}

@media only screen and (min-width:960px) {
  .container {
    grid-template-columns: 150px auto;
    grid-template-rows: minmax(40px, max-content) auto;
  }

  .left-nav {
    display: unset;
  }

  .nav-small {
    display: none;
  }

  .main {
    grid-column: 2/-1;
    border: 1px black solid;
  }
}
</style>
