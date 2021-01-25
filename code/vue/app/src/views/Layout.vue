<template>
  <v-main>
    <v-app-bar flat dense app>crave control</v-app-bar>

    <v-container fluid class="outer-container fill-height">

      <v-row no-gutters align-items="start" class="main-row">
        <v-col class="left-tabs">
          left tabs
        </v-col>
        <v-col class="main-col">

          <v-container fluid class="cards-container">
            <v-row no-gutters class="cards-row">
              <v-col
                v-for="n in 18"
                :key="n"
                cols="12"
                md="6"
                xl="4"  
                class="card-col"      
              >
                <div class="widget-card">
                  widget
                </div>
              </v-col>
            </v-row>
          </v-container>
  
        </v-col>
      </v-row>

      <v-row no-gutters class="top-tabs">
        <v-col>
          <v-tabs
            centered
            v-model="tab"
            show-arrows
          >
            <v-tabs-slider color="blue"></v-tabs-slider>

            <v-tab
              v-for="item in items"
              :key="item"
            >
              {{ item }}
            </v-tab>
          </v-tabs>
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
  padding: 0px;
}

.top-tabs {
  height: 50px;
  padding-right: 27px;
}

.main-row {
  height: calc(100vh - 100px);
}

.left-tabs {
  display: none;
  border: 1px black solid;
  height: 100%;
  max-width: 250px;
}

.main-col {
  border: 1px black solid;
  height: 100%;
}

.cards-container {
  padding: 0px;
  height: 100%;
}

.cards-row {
  height: 100%;
  overflow-y: auto;
}

.v-tab {
  font-size: 12px;
}

.card-col {
  padding: 10px;
}

.widget-card {
  color: white;
  background-color: darkblue;
  height: 60px;
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
