<template>
  <b-rate
    icon-pack="fas"
    icon="ghost"
    :spaced="true"
    v-model="rating"
    @change="userRate"
    custom-text=""
  >
  </b-rate>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator';
import Place from '@/types/Place';
import httpClient from '@/services/api';

@Component
export default class PlaceRater extends Vue {
  @Prop(Number) readonly placeId!: number;

  @Prop(Number) readonly avgRating!: number;

  private localRating: number | undefined = undefined;

  get rating(): number {
    return this.localRating === undefined ? this.avgRating : this.localRating;
  }

  set rating(value:number) {
    this.localRating = value;
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
    });
  }
}
</script>

<style>

</style>
