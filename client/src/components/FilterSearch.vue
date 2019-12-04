<template>
  <div class="box">
    <b-field label="Sort By" v-if="sizeOfSearch">
      <b-dropdown v-model="sort" aria-role="list">
        <button class="button" type="button" slot="trigger">
          <template v-if="!sort">
              <span>Best Match &#9662;</span>
          </template>
          <template v-else>
              <span>Top Rated &#9662;</span>
          </template>
          <b-icon icon="menu-down"></b-icon>
        </button>

        <b-dropdown-item :value="false" aria-role="listitem">
          <div class="media">
              <b-icon class="media-left"></b-icon>
              <div class="media-content">
                  <h3>Best Match</h3>
              </div>
          </div>
        </b-dropdown-item>

        <b-dropdown-item :value="true" aria-role="listitem">
          <div class="media">
              <b-icon class="media-left"></b-icon>
              <div class="media-content">
                  <h3>Top Rated</h3>
              </div>
          </div>
        </b-dropdown-item>
      </b-dropdown>
    </b-field>

    <section>
      <b-button @click="sortTopRated" v-if="sort">Apply</b-button>
    </section>

    <b-field label="Find Nearby">
      <div class="showSlider" v-if="this.latitude != -1">
        <b-slider v-model="sliderDistance">
        </b-slider>
        {{sliderDistance}} mi.
      </div>
    </b-field>

    <b-field label="Created By">
        <b-input placeholder="Email" type="email" v-model="createdEmail"></b-input>
    </b-field>

    <!-- <section>
      <b-button @click="applyFilters">Apply</b-button>
    </section> -->
  </div>
</template>

<style lang="scss" scoped>
.filter {
  color: #8d6b94;
}

.box {
  margin-top: 3.8rem;
}
</style>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import AppModule from '@/store/modules/app';

@Component
export default class FilterSearch extends Vue {
  public sliderDistance: number = 0;

  public sort: boolean = false;

  public createdEmail: string = '';

  public latitude: number = -1;

  public longitude: number = -1;

  created() {
    navigator.geolocation.getCurrentPosition(this.setPosition);
  }

  @Watch('sliderDistance')
  onSliderDistanceChanged(val: number, oldVal: number) {
    AppModule.updateFilterOptions({
      findNear: val,
    });
  }

  @Watch('createdEmail')
  onCreatedEmailChanged(val: number, oldVal: number) {
    AppModule.updateFilterOptions({
      createdBy: val,
    });
  }

  @Watch('latitude')
  onLatitudeChanged(val: number, oldVal: number) {
    AppModule.updateFilterOptions({
      location: {
        latitude: val,
        longitude: this.longitude,
      },
    });
  }

  @Watch('longitude')
  onLongitudeChanged(val: number, oldVal: number) {
    AppModule.updateFilterOptions({
      location: {
        latitude: this.latitude,
        longitude: val,
      },
    });
  }

  get sizeOfSearch() {
    this.sliderDistance = 0;
    this.sort = false;
    this.createdEmail = '';
    return AppModule.places.length > 0;
  }

  setPosition(position: any) {
    this.latitude = position.coords.latitude;
    this.longitude = position.coords.longitude;
  }

  get lat() {
    return this.latitude;
  }

  // applyFilters() {
  //   AppModule.ClearPlaces();
  //   AppModule.FilterSearch({
  //     location: {
  //       latitude: this.latitude,
  //       longitude: this.longitude,
  //     },
  //     findNear: this.sliderDistance,
  //     createdBy: this.createdEmail,
  //   });
  // }

  // sortTopRated() {
  //   AppModule.FilterSort();
  // }
}
</script>
