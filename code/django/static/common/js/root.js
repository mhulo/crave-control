
  Vue.use(httpVueLoader);

  var eventBus = new Vue();

  var app = new Vue({
    el: '#app',
    data: {
      premium: true,
      cart: []
    },
    components: { 
      'product': 'url:/static/common/vue/product.vue'
    },
    methods: {
      updateCart(id) {
        this.cart.push(id)
      }
    }
  });