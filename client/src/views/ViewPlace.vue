<template>
  <section>
    <div class="container">
      <div class="box viewPlace">
        <div class="columns is-multiline">
          <div class="column is-full">
            <GMap :places="places"></GMap>
          </div>
          <div class="column is-one-quarter">
            <h2 class="has-text-weight-bold is-size-5">{{ place.placeName }}</h2>
            <p class="has-text-weight-bold is-size-6">Address:</p>
            <p>{{ place.address }}</p>
            <p class="has-text-weight-bold is-size-6">Lat/Long:</p>
            <small>{{ place.latitude }}, {{ place.longitude }}</small>
            <p class="has-text-weight-bold is-size-6">User Rating:</p>
            <PlaceRater :placeId="place.placeId" :avgRating="place.avgRating"> </PlaceRater>
          </div>
          <div class="column">
            <h2 class="has-text-weight-bold is-size-5">Description</h2>
            <p><small><b>Submitted by:</b> {{ place.userName }}</small></p>
            <p>{{ place.description }}</p>
          </div>
        </div>
      </div>
      <!-- <div class="box viewPlace">
        <h2 class="has-text-weight-bold is-size-5">Reviews</h2>
        <article class="media">
          <div class="media-content">
            <div class="content">
              <p>
                <strong>John Smith</strong> <small>@johnsmith</small>
                <br>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Proin ornare magna eros, eu pellentesque tortor vestibulum ut.
                Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.
              </p>
            </div>
          </div>
        </article>
      </div> -->
    </div>
  </section>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator';
import PlaceRater from '@/components/PlaceRater.vue';
import Place from '@/types/Place';
import httpClient from '@/services/api';
import GMap from '@/components/GMap.vue';


@Component({
  components: {
    GMap,
  },
  props: {
    id: String,
  },
  components: {
    PlaceRater,
  },
})
export default class ViewPlace extends Vue {
  @Prop(String) readonly id: String | undefined;

  isLoading: boolean = false;

  place: Place = {} as any;

  get places() {
    return this.place === undefined ? [] : [this.place];
  }

  created() {
    if (this.id) {
      this.isLoading = true;
      httpClient.get(`/place/${this.id}`)
        .then((response) => {
          this.place = {
            placeId: response.data.place_id,
            placeName: response.data.place_name,
            email: response.data.email,
            userName: response.data.user_name,
            address: response.data.address,
            latitude: response.data.latitude,
            longitude: response.data.longitude,
            avgRating: response.data.avg_rating,
            description: response.data.description,
          };
          this.isLoading = false;
        });
    }
  }
}
</script>

<style lang="scss" scoped>
.viewPlace {
  margin-top: 25px;
}
</style>
