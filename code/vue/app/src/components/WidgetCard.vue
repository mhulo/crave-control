<template>
  <div class="event-card -shadow">
    <span>{{ widget.name }} @ {{ widget.id }}</span>
  </div>
</template>

<script>
export default {
  props: {
    widget: Object
  }
}
</script>

<style scoped>
.event-link {
  color: black;
  text-decoration: none;
  font-weight: 100;
}
</style>
