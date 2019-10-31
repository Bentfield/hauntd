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
                  @change="success"
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
          <div class="level-right">
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
import Vue from 'vue';
import Component from 'vue-class-component';
import Place from '@/types/Place';

@Component({
  props: {
    place: Object as () => Place,
  },
})
export default class EditPlace extends Vue {
  place!: Place;
}
</script>

<style lang="scss" scoped>
small {
  color: #777777;
}
</style>
