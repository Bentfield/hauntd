<template>
  <section>
    <div class="container">
      <div class="column is-half is-offset-one-quarter">
        <div class="box editPlace">
          <h1 v-if="isNew" class="title">Add Place</h1>
          <h1 v-else class="title">Edit Place</h1>
          <b-field label="Name" label-position="inside">
              <b-input
                placeholder="Name of location"
                maxlength="255"
                v-model="place.placeName"
                :has-counter="false">
              </b-input>
          </b-field>
          <b-field label="Address" label-position="inside">
              <b-input
                placeholder="Rough address of location"
                maxlength="205"
                v-model="place.address"
                :has-counter="false">
              </b-input>
          </b-field>
          <!-- <b-field label="City" label-position="inside">
              <b-input
                placeholder="Minneapolis, Chicago, etc.."
                maxlength="30"
                :has-counter="false">
              </b-input>
          </b-field>
          <b-field label="State" label-position="inside">
              <b-input
                placeholder="Minnesota, Illinois, etc.."
                maxlength="20"
                :has-counter="false">
              </b-input>
          </b-field> -->
          <b-field label="Description" label-position="inside">
              <b-input
                type="textarea"
                placeholder="What makes this place haunted?"
                v-model="place.description"
                maxlength="5000">
              </b-input>
          </b-field>
          <nav class="level is-mobile">
            <div class="level-left" />
            <div class="level-right">
              <a class="level-item buttons">
                <b-button class="is-success" @click="save">
                  Save
                </b-button>
                <b-button class="is-danger" icon-left="trash" v-if="!isNew" @click="deletePlace">
                  Delete
                </b-button>
              </a>
            </div>
          </nav>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import Place from '@/types/Place';
import httpClient from '@/services/api';

@Component({
  props: {
    id: Number,
  },
})
export default class EditPlace extends Vue {
  id!: Number;

  place: Place = {
    placeId: -1,
    placeName: '',
    email: '',
    address: '',
    latLong: '',
    avgRating: 0,
    description: '',
  }

  public save(): void {
    if (!this.isNew) {
      httpClient.patch(`/place?place_id=${this.place.placeId}`, {
        place_name: this.place.placeName,
        description: this.place.description,
        location_string: this.place.address,
      }).then((response) => {
        console.log(response);
      });
    } else {
      httpClient.post('/place', {
        email: 'test@gmail.com',
        place_name: this.place.placeName,
        location_string: this.place.address,
        description: this.place.description,

      }).then((response) => {
        console.log(response);
      });
    }
  }

  public deletePlace(): void {
    httpClient.delete(`/place?place_id=${this.id}`)
      .then((response) => {
        console.log(response);
      });
  }

  get isNew(): boolean {
    return this.id === undefined;
  }

  created() {
    httpClient.get(`/place?place_id=${this.id}`)
      .then((response) => {
        [this.place.placeId,
          this.place.email,
          this.place.placeName,
          this.place.address,
          this.place.latLong,
          this.place.avgRating,
          this.place.description] = response.data;
      });
  }
}
</script>

<style lang="scss" scoped>
.editPlace {
  margin-top: 25px;
  background-color: #fff;
}
</style>
