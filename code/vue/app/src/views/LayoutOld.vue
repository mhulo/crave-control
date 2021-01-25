<template>
  <v-main>
    <v-app-bar flat dense app>crave control old</v-app-bar>

    <v-container fluid class="outer-container fill-height">

      <v-row no-gutters class="top-tabs">
        <v-col>
          <v-tabs
            centered
            v-model="tab"
            show-arrows
          >
            <v-tabs-slider color="yellow"></v-tabs-slider>

            <v-tab
              v-for="item in items"
              :key="item"
            >
              {{ item }}
            </v-tab>
          </v-tabs>
        </v-col>
      </v-row>

      <v-row no-gutters align-items="start" class="main-row">
        <v-col class="left-tabs">
          left tabs
        </v-col>
        <v-col>

          <v-container fluid class="cards-container">
            <v-row no-gutters>
              <v-col
                v-for="n in 6"
                :key="n"
                cols="12"
                md="6"
                xl="4"          
              >
                <v-card
                  class="pa-2"
                  outlined
                  tile
                >
                  column
                </v-card>
              </v-col>
            </v-row>
          </v-container>
  
        </v-col>
      </v-row>
    </v-container>

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
.outer-container {
  border: 1px blue solid;
  padding: 0px;
}

.main-row {
  height: calc(100vh - 100px);
  border: 1px red solid;
  padding: 0px;
}

.top-tabs {
  border: 1px pink solid;
  height: 50px;
  padding-right: 27px;
}

.left-tabs {
  display: none;
  border: 1px green solid;
  max-width: 250px;
}

.cards-container {
  border: 2px black solid;
}

@media only screen and (min-width:960px) {
  .main-row {
    height: calc(100vh - 50px);
  }

  .top-tabs {
    display: none;
  }

  .left-tabs {
    display: unset;
  }
}
</style>
