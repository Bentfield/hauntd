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

    public loggedIn: boolean = false;

    public email: string = '';

    @Mutation
    public SignIn(user: any) {
      httpClient.defaults.headers["Authorization"] = user.token.split(',')[0]; //eslint-disable-line
      localStorage.setItem('idToken', user.token);
      localStorage.setItem('email', user.email);
      this.email = user.email;
      this.loggedIn = true;
    }

    @Mutation
    public SignOut() {
      delete httpClient.defaults.headers["Authorization"]; //eslint-disable-line
      localStorage.clear();
      this.loggedIn = false;
      this.email = '';
    }

    @Mutation
    private SET_PLACES(places: Place[]) {
      this.places = places;
    }

    @Action
    public SearchPlaces(query: string) {
      httpClient.get(`/place/${query}`)
        .then((response) => {
          console.log(response);
          const place : Place = {
            placeId: response.data.place_id,
            email: response.data.email,
            placeName: response.data.place_name,
            address: response.data.address,
            latitude: response.data.latitude,
            longitude: response.data.longitude,
            avgRating: response.data.avg_rating,
            description: response.data.description,
          };
          this.SET_PLACES([place]);
        })
        .catch((e) => {
          this.SignOut();
          this.SET_PLACES([]);
        });
    }

    @Action
    public ClearPlaces() {
      this.SET_PLACES([]);
    }

    @Action
    public FilterSearch(options: any) {
      httpClient.get('/filter', { params: options })
        .then((response) => {
          const places: Place[] = [];
          console.log(response.data);
          response.data.forEach((place: any) => {
            places.push({
              placeId: place.place_id,
              email: place.email,
              placeName: place.place_name,
              address: place.address,
              latitude: place.latitude,
              longitude: place.longitude,
              avgRating: place.avg_rating,
              description: place.description,
            });
          });
          this.SET_PLACES(places);
        });
    }

    @Action
    public FilterSort() {

    }
}

export default getModule(App);
