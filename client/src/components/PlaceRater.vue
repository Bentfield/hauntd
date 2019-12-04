<template>
  <b-rate
    icon-pack="fas"
    icon="ghost"
    :spaced="true"
    v-model="rating"
    @change="userRate"
    custom-text=""
    :disabled="!loggedIn"
  >
  </b-rate>
</template>

<script lang="ts">
import {
  Vue, Component, Prop, Watch,
} from 'vue-property-decorator';
import Place from '@/types/Place';
import AppModule from '@/store/modules/app';
import httpClient from '@/services/api';

@Component
export default class PlaceRater extends Vue {
  @Prop(Number) readonly placeId!: number;

  @Prop(Number) readonly avgRating!: number;

  @Watch('placeId')
  onPlaceIdChanged(val: number, oldVal: number) {
    this.localRating = undefined;
  }

  public localRating: number | undefined = undefined;

  get rating(): number {
    return this.localRating === undefined ? this.avgRating : this.localRating;
  }

  set rating(value:number) {
    this.localRating = value;
  }

  get loggedIn(): boolean {
    return AppModule.loggedIn;
  }

  userRate(value:Number) {
    httpClient.post('rating', {
      place_id: this.placeId,
      rating: value,
    }).then((response) => {
      this.$buefy.toast.open({
        message: 'Successfully submitted rating.',
        type: 'is-success',
      });
    }).catch((error) => {
      this.$buefy.toast.open({
        message: 'You must be logged in to rate places.',
        type: 'is-danger',
      });
    });
  }
}
</script>

<style>

</style>
