import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/place/edit/:id?',
    name: 'edit_place',
    props: true,
    component: () => import(/* webpackChunkName: "edit_place" */ '../views/EditPlace.vue'),
  },
  {
    path: '/place/:id?',
    name: 'view_place',
    props: true,
    component: () => import(/* webpackChunkName: "view_place" */ '../views/ViewPlace.vue'),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
