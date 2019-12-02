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
                <strong style="color:#8d6b94;">{{place.placeName}}</strong>
              </div>
              <div class="column is-half">
                <b-rate class="is-pulled-right"
                  icon-pack="fas"
                  custom-text=""></b-rate>
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
              <small>Submitted by: {{place.email}}</small>
            </p>
          </div>
          <div class="level-right" v-if="allowEdit">
            <router-link class="level-item" :to="{ name: 'edit', params: { id: place.placeId } }">
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
import Place from '@/types/Place';
import AppModule from '@/store/modules/app';

@Component({
  props: {
    place: Object as () => Place,
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
</style>
