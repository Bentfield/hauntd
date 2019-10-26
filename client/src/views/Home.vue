<template>
  <section class="section home">
    <div class="container search-banner">
      <div class="column is-half is-offset-one-quarter">
        <h1 class="title">Spooky Search</h1>
        <SearchBar></SearchBar>
        <SearchList></SearchList>
      </div>
    </div>
  </section>
</template>

<script>
// @ is an alias to /src
import SearchBar from '@/components/SearchBar.vue';
import SearchList from '@/components/SearchList.vue';

export default {
  name: 'home',
  components: {
    SearchBar,
    SearchList,
  },
};
</script>

<style lang="scss">
.search-banner .title {
  color: #fff;
}
</style>
