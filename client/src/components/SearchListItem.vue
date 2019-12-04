<template>
  <div class="box">
    <div class="columns">
      <div class="column is-one-fifth-tablet">
        <p class="image is-square">
          <img src="https://bulma.io/images/placeholders/128x128.png">
        </p>
      </div>
      <div class="column">
        <div class="content">
            <div class="columns is-gapless is-multiline">
              <div class="column is-half">
                <router-link :to="{ name: 'view_place', params: { id: place.placeId } }">
                  <strong class="placeName">{{place.placeName}}</strong>
                </router-link>
              </div>
              <div class="column is-half">
                <PlaceRater class="is-pulled-right"
                  :placeId="place.placeId"
                  :avgRating="place.avgRating"
                >
                </PlaceRater>
              </div>
              <div class="column">
                <small>{{place.address}}</small>
              </div>
            </div>
            {{place.description}}
        </div>
        <nav class="level is-mobile">
          <div class="level-left">
            <p class="level-item">
              <small>Submitted by: {{place.userName}}</small>
            </p>
          </div>
          <div class="level-right" v-if="allowEdit">
            <router-link class="level-item"
              :to="{ name: 'edit_place', params: { id: place.placeId } }"
            >
              <span class="icon is-small"><i class="fas fa-edit"></i></span>
            </router-link>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator';
import PlaceRater from '@/components/PlaceRater.vue';
import Place from '@/types/Place';
import AppModule from '@/store/modules/app';

@Component({
  props: {
    place: Object as () => Place,
  },
  components: {
    PlaceRater,
  },
})
export default class SearchListItem extends Vue {
  place!: Place;

  get allowEdit() {
    return AppModule.email === this.place.email;
  }
}
</script>

<style lang="scss" scoped>
small {
  color: #777777;
}

.placeName {
  color: #8d6b94;
}

.placeName:hover {
  color: #db504a;
}
</style>
