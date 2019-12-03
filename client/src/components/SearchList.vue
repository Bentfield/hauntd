<template>
  <div class="search-list">
    <br />
    <SearchListItem
      v-for="place in places"
      v-bind:key="place.place_id"
      :place="place">
    </SearchListItem>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import AppModule from '@/store/modules/app';
import SearchListItem from '@/components/SearchListItem.vue';

@Component({
  components: {
    SearchListItem,
  },
})
export default class SearchList extends Vue {
  get places() {
    return AppModule.places;
  }
}
</script>

<style lang="scss">
.search-list {
  text-align: left;
}
</style>
