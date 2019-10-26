<template>
  <div class="search-list">
    <br />
    <SearchListItem></SearchListItem>
    <SearchListItem></SearchListItem>
    <SearchListItem></SearchListItem>
  </div>
</template>

<script>
import SearchListItem from '@/components/SearchListItem.vue';

export default {
  components: {
    SearchListItem,
  },
  data() {
    return {
      items: [1, 2, 3, 4, 5],
    };
  },
};
</script>

<style lang="scss">
.search-list {
  text-align: left;
}
</style>
