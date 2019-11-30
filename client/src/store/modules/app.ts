import {
  VuexModule, Module, Mutation, Action, getModule,
} from 'vuex-module-decorators';
import { IAppState } from './IAppState';
import store from '@/store';
import Place from '@/types/Place';
import httpClient from '@/services/api';

@Module({ dynamic: true, store, name: 'app' })
class App extends VuexModule implements IAppState {
    public places : Place[] = [];

    @Mutation
    private SET_PLACES(places: Place[]) {
      this.places = places;
    }

    @Action
    public SearchPlaces(query: string) {
      httpClient.get(`/place/${query}`)
        .then((response) => {
          const place : Place = {
            placeId: response.data.place_id,
            email: response.data.email,
            placeName: response.data.place_name,
            address: response.data.address,
            latLong: response.data.lat_long,
            avgRating: response.data.avg_rating,
            description: response.data.description,
          };
          this.SET_PLACES([place]);
        })
        .catch(() => {
          this.SET_PLACES([]);
        });
    }

    @Action
    public ClearPlaces() {
      this.SET_PLACES([]);
    }
}

export default getModule(App);
