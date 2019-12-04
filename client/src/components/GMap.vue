<template>
  <div class="gmap">

    <GmapMap
      :center= "{ lat: 0, lng: 0 }"
      :zoom="15"
      ref="mapRef"
      v-show="!(center.lat === 0 && center.lng === 0)"
    >
      <GmapMarker
        v-for="(item, index) in markers"
        :key="index"
        :position="item.position"
        :title="item.placeName"
        @click="markerClick(item)"
      />
    </GmapMap>
  </div>
</template>

<script lang="ts">
import {
  Vue, Component, Prop, Watch,
} from 'vue-property-decorator';
import Place from '@/types/Place';

@Component({ name: 'GMap' })
export default class GMap extends Vue {
  @Prop({ type: Array, required: true }) readonly places!:Place[]

  $refs!: {
    mapRef: any,
  }

  public mapTypeId: string='';

  public ll: any;

  public marker: any;

  public markers: any[]=[];

  private center: any = {
    lat: 0,
    lng: 0,
  };

  @Watch('places')
  onPlacesChanged(val: Place[], oldval: Place[]) {
    this.updateMarkers(val);
  }

  mounted() {
    this.updateMarkers(this.places);
  }

  public updateMarkers(placeArr: Place[]) {
    this.markers = [];
    if (placeArr.length > 0) {
      this.$refs.mapRef.$mapPromise.then((map: any) => {
        const bounds = new google.maps.LatLngBounds();
        for (let i = 0; i < placeArr.length; i += 1) {
          this.ll = { lat: placeArr[i].latitude, lng: placeArr[i].longitude };
          if (!(this.ll.lat === 0 && this.ll.lng === 0)) {
            this.marker = new google.maps.Marker({
              position: this.ll,
              placeId: placeArr[i].placeId,
              placeName: placeArr[i].placeName,
            });
            this.markers.push(this.marker);
            bounds.extend(this.ll);
          }
        }

        this.center.lat = placeArr[0].latitude;
        this.center.lng = placeArr[0].longitude;
        map.setCenter({ lat: placeArr[0].latitude, lng: placeArr[0].longitude });
        if (placeArr.length > 1) {
          map.setCenter(bounds.getCenter());
          map.fitBounds(bounds);
          setTimeout(() => {
            map.fitBounds(bounds);
          }, 10);
        }
      });
    }
  }

  markerClick(item: any) {
    this.$router.push({ name: 'view_place', params: { id: item.placeId } });
  }
}

</script>

<style lang="scss" scoped>
.vue-map-container {
  height: 450px;
  max-width: 992px;
  width: 100%;
}
</style>
