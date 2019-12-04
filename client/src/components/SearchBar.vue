<template>
  <section>
    <b-field>
      <b-input
        type="search"
        icon="search"
        placeholder="Search our haunted database..."
        size="is-medium"
        expanded
        v-model="query"
        @keyup.native.enter="search"
      ></b-input>
      <p class="control">
        <button class="button is-primary is-medium" @click="search">Boo</button>
      </p>
       <b-tooltip label="Give me a random spooky place."
            position="is-top"
            animated>
            <b-button type="is-white"
                icon-pack="fas"
                icon-right="ghost"
                size="is-medium"
                style="margin-left:10px;"
                @click="getSpooked"/>
        </b-tooltip>
    </b-field>

    <nav class="level">
      <div class="level-left">
        <b-button type="is-warning" outlined @click="editPlace()">Add Place</b-button>
      </div>
      <div class="level-right">
        <p>
          <strong>{{sizeOfSearch}}</strong> haunted places found
        </p>
      </div>
    </nav>
  </section>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import AppModule from '@/store/modules/app';
import httpClient from '@/services/api';

@Component
export default class SearchBar extends Vue {
  query: string = '';

  get sizeOfSearch() {
    return AppModule.places.length;
  }

  editPlace() {
    this.$router.push({ name: 'edit_place' });
  }

  search() {
    AppModule.SearchPlaces(this.query);
  }

  public getSpooked() {
    httpClient.get('/spook').then((response) => {
      this.$router.push({ name: 'view_place', params: { id: response.data.place_id } });
    });
  }
}
</script>

<style scoped lang="scss">
strong {
  color: #fff;
}
</style>
