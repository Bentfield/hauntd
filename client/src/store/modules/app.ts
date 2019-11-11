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
    public SearchPlaces(name: string) {
      httpClient.get(`/place?place_name=${name}`)
        .then((response) => {
          const place : Place = {
            placeId: response.data[0],
            email: response.data[1],
            placeName: response.data[2],
            address: response.data[3],
            latLong: response.data[4],
            avgRating: response.data[5],
            description: response.data[6],
          };
          this.SET_PLACES([place]);
        })
        .catch(() => {
          this.SET_PLACES([]);
        });
    }
}

export default getModule(App);
