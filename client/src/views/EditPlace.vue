<template>
  <section>
    <div class="container">
      <b-loading :active.sync="isLoading"></b-loading>
      <div class="column is-half is-offset-one-quarter">
        <div class="box editPlace">
          <h1 v-if="isNew" class="title">Add Place</h1>
          <h1 v-else class="title">Edit Place</h1>
          <b-field label="Name" label-position="inside">
              <b-input
                placeholder="Name of location"
                maxlength="255"
                v-model="place.placeName"
                required
                :has-counter="false">
              </b-input>
          </b-field>
          <b-field label="Address" label-position="inside">
              <b-input
                placeholder="Rough address of location"
                maxlength="205"
                v-model="place.address"
                required
                :has-counter="false">
              </b-input>
          </b-field>
          <b-field grouped>
            <b-field label="Latitude" label-position="inside" expanded>
                <b-input
                  placeholder="Latitude"
                  type="number"
                  step="0.00000001"
                  maxlength="16"
                  v-model="place.latitude"
                  required
                  :has-counter="false">
                </b-input>
            </b-field>
            <b-field label="Longitude" label-position="inside" expanded>
              <b-input
                placeholder="Longitude"
                type="number"
                step="0.00000001"
                maxlength="16"
                v-model="place.longitude"
                required
                :has-counter="false">
              </b-input>
            </b-field>
          </b-field>
          <b-field label="Description" label-position="inside">
              <b-input
                type="textarea"
                placeholder="What makes this place haunted?"
                v-model="place.description"
                required
                maxlength="5000">
              </b-input>
          </b-field>
          <nav class="level is-mobile">
            <div class="level-left" />
            <div class="level-right">
              <a class="level-item buttons">
                <b-button v-bind:class="[saving ? 'is-loading' : '', 'is-success']" @click="save">
                  Save
                </b-button>
                <b-button v-bind:class="[deleting ? 'is-loading' : '', 'is-danger']"
                  icon-left="trash"
                  v-if="!isNew"
                  @click="deletePlace"
                >
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
import { Vue, Component, Prop } from 'vue-property-decorator';
import Place from '@/types/Place';
import httpClient from '@/services/api';
import AppModule from '@/store/modules/app';

@Component({
  props: {
    id: Number,
  },
})
export default class EditPlace extends Vue {
  @Prop(Number) readonly id: number | undefined;

  saving: boolean = false;

  deleting: boolean = false;

  isLoading: boolean = false;

  place: Place = {} as any;

  public save(): void {
    if (!this.validatePlace()) {
      this.$buefy.toast.open({
        message: 'Place fill in all fields.',
        type: 'is-danger',
      });
      return;
    }
    this.saving = true;
    if (!this.isNew) {
      httpClient.patch(`/place/${this.place.placeId}`, {
        place_name: this.place.placeName,
        description: this.place.description,
        address: this.place.address,
        latitude: this.place.latitude,
        longitude: this.place.longitude,
      }).then((response) => {
        this.$buefy.toast.open({
          message: 'Successfully saved changes.',
          type: 'is-success',
        });
      })
        .catch((e) => {
          this.$buefy.toast.open({
            message: 'Error encountered on save.',
            type: 'is-danger',
          });
        })
        .finally(() => {
          this.saving = false;
          AppModule.ClearPlaces();
        });
    } else {
      httpClient.post('/place', {
        email: 'test@gmail.com',
        place_name: this.place.placeName,
        address: this.place.address,
        description: this.place.description,
        latitude: this.place.latitude,
        longitude: this.place.longitude,
      }).then((response) => {
        this.$buefy.toast.open({
          message: 'Successfully created new place.',
          type: 'is-success',
        });
      })
        .catch(() => {
          this.$buefy.toast.open({
            message: 'Error encountered on save.',
            type: 'is-danger',
          });
        })
        .finally(() => {
          this.saving = false;
        });
    }
  }

  private validatePlace(): boolean {
    if (!this.place.placeName) {
      return false;
    }
    if (!this.place.latitude && this.place.latitude !== 0) {
      return false;
    }
    if (!this.place.longitude && this.place.longitude !== 0) {
      return false;
    }
    if (!this.place.address) {
      return false;
    }
    if (!this.place.description) {
      return false;
    }
    return true;
  }

  public deletePlace(): void {
    this.deleting = true;
    httpClient.delete(`/place/${this.id}`)
      .then((response) => {
        this.deleting = false;
        AppModule.ClearPlaces();
        this.$router.push({ name: 'home' }, () => {
          this.$buefy.toast.open({
            message: 'Deleted place successfully.',
            type: 'is-success',
          });
        });
      });
  }

  get isNew(): boolean {
    return this.id === undefined;
  }

  created() {
    if (this.id) {
      this.isLoading = true;
      httpClient.get(`/place/${this.id}`)
        .then((response) => {
          this.place.placeId = response.data.place_id;
          this.place.placeName = response.data.place_name;
          this.place.email = response.data.email;
          this.place.userName = response.data.user_name;
          this.place.address = response.data.address;
          this.place.latitude = response.data.latitude;
          this.place.longitude = response.data.longitude;
          this.place.avgRating = response.data.avg_rating;
          this.place.description = response.data.description;
          this.isLoading = false;
        });
    }
  }
}
</script>

<style lang="scss" scoped>
.editPlace {
  margin-top: 25px;
  background-color: #fff;
}
</style>
