import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import router from '../router';
import { AxiosError } from 'axios';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    user: null,
    token: null,
    loading: true,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
    clearUser(state) {
      state.user = null;
      state.token = null;
    },
    clearLocalStorage() {

      localStorage.removeItem('token');
      localStorage.removeItem('movies'); // Clear any other data stored in local storage
      localStorage.removeItem('theatres'); // Clear any other data stored in local storage
      // Add other local storage keys if needed
    },
    setLoading(state, status) {
      state.loading = status;
    },
  },
  actions: {
    handleUnauthorized({ commit }) {
      commit('clearLocalStorage');
      if (router.currentRoute.path !== '/login') {
        router.push('/login');
      }

    },
    async login({ commit }, { user_id, password }) {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        user_id,
        password,
      });
      const { userusername, access_token } = response.data;
      commit('setUser', userusername);
      commit('setToken', access_token);
      localStorage.setItem('token', access_token);
      localStorage.setItem('userusername',userusername)

    },
    logout({ commit }) {
      commit('clearUser');
      localStorage.removeItem('token');
      alert("Successfully logged out")
      router.push('/login')
    },
    logoutadmin() {
      localStorage.removeItem('admintoken');
      alert("Logging out successfully")
      router.push('/admin/login')
    },

      async fetchMovies({ commit, dispatch }) {
        try {
          commit('setLoading', true); 
          const token = localStorage.getItem('token');
          const response = await axios.get('http://localhost:5000/movies', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          localStorage.setItem('movies',JSON.stringify(response.data))
        } catch (error) {
          const axiosError = error as AxiosError;
          if ( axiosError.response && (axiosError.response.status === 401 || axiosError.response.status === 422) ) {
            dispatch('handleUnauthorized');
          } else {
            console.error('Error fetching movies:', error);
          }
        } finally {
          if (localStorage.getItem('theatres')){
            commit('setLoading', false); // Set loading to false after API call
          }
        }
      },

    async fetchTheatres({ commit, dispatch }) {
      try {
        commit('setLoading', true); // Set loading to true before API call
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/theatres', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        localStorage.setItem('theatres',JSON.stringify(response.data))
      } catch (error) {
        const axiosError = error as AxiosError;
        if ( axiosError.response && (axiosError.response.status === 401 || axiosError.response.status === 422)) {
          await dispatch('handleUnauthorized');
        } else {
          console.error('Error fetching movies:', error);
        }
      } finally {
        if (localStorage.getItem('theatres')){
          commit('setLoading', false); // Set loading to false after API call
        }
      }
    },

  },
  getters: {
    isLoggedIn: (state) => !!state.user,
  },
});

export default store;

