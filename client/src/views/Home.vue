<template>
  <section class="section home">
    <div class="container search-banner">
      <div class="columns">
        <div class="column is-one-quarter">
          <FilterSearch></FilterSearch>
        </div>
        <div class="column is-half">
          <h1 class="title has-text-centered">Spooky Search</h1>
          <SearchBar></SearchBar>
          <SearchList></SearchList>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// @ is an alias to /src
import FilterSearch from '@/components/FilterSearch.vue';
import SearchBar from '@/components/SearchBar.vue';
import SearchList from '@/components/SearchList.vue';

export default {
  name: 'home',
  components: {
    SearchBar,
    SearchList,
    FilterSearch,
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 0;
  padding-right: 0;
  padding-left: 0;
}

.search-banner .title {
  color: #fff;
}
</style>
