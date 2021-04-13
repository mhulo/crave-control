<template>
  <div class="popup-comp-wrapper">
    <component
      :is="cardComp"
      :key="'card_'+cardType+'_detail_'+cardId"
      :card="cardData"
      :options="cardOptions"
    />
  </div>
</template>

<script>
import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'

export default {
  components: {},
  data() {
    return {
      cardComp: () => import('@/components/cards/'  + this.cardType + '.vue'),
      cardOptions: {
        'show': 'full'
      }
    }
  },
  methods: {},
  computed: {
    cardId() {
      return this.$route.params.cardId
    },
    cardData() {
      return (this.cardId in this.$store.getters.cards) ? 
        this.$store.getters.cards[this.cardId] :
        {}
    },
    cardType() {
      return (this.cardId in this.$store.getters.cards) ? 
        this.$store.getters.cards[this.cardId].card :
        'Default'
    },
  },
  watch: {
    cardData()  {
      this.cardComp = () => import('@/components/cards/'  + this.cardType + '.vue')
    }
  },
  created() {},
  mounted() {},
  beforeDestroy() {},
}
</script>

<style>
.popup-comp-wrapper {
  width: 100%;
  min-height: 100%;
  border: 0px yellow solid;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 10px;
  background: rgba(255,255,255,0.1)
}

</style>
