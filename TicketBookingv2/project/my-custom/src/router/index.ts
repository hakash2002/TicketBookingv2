import Vue from 'vue';
import VueRouter from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import UserDashboard from '../components/UserDashboard.vue'
import TheatresPage from '../components/TheatresPage.vue'
import BuyTickets from '../components/BuyTickets.vue'
import UserBookings from '../components/UserBookings.vue'
import RateShow from '../components/RateShow.vue'
import SignUp from '../components/SignUp.vue'
import AdminLogin from '../components/AdminLogin.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import AdminCreatevenue from '../components/AdminCreatevenue.vue'
import AdminCreateshow from '../components/AdminCreateshow.vue'
import AdminRegister from '../components/AdminRegister.vue'
import TheatresCopy from '../components/TheatrespageDate.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    component: LoginPage,
  },
  {
    path: '/shows',
    component: UserDashboard,
  },
  {
    path: '/shows/:id',
    component: UserDashboard,
  },
  {
    path: '/theatres',
    component: TheatresPage,
  },
  {
    path: '/theatres/:name',
    component: TheatresPage,
  },
  {
    path: '/theatres/:name/date',
    component: TheatresCopy,
  },
  {
    path: '/booktickets/:tid/:mid',
    component: BuyTickets,
  },
  {
    path: '/bookings',
    component: UserBookings,
  },
  {
    path: '/rate/:sid',
    component: RateShow,
  },
  {
    path: '/register',
    component: SignUp,
  },
  {
    path: '/admin/register',
    component: AdminRegister,
  },
  {
    path: '/admin/login',
    component: AdminLogin,
  },
  {
    path: '/admindash',
    component: AdminDashboard,
  },
  {
    path: '/admin/createvenue',
    component: AdminCreatevenue,
  },
  {
    path: '/admin/updatevenue/:id',
    component: AdminCreatevenue,
  },
  {
    path: '/admin/createshow/:vid',
    component: AdminCreateshow
  },
  {
    path: '/admin/updateshow/:vid/:sid',
    component: AdminCreateshow
  },

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;



