<template>
    <div class="theatres">
        <section class="top-barus" style="background-color: black;">
            <div class="left-contentus">
                <h2 class="title1">BookMyMovie</h2>
                <div class="navigationus">
                    <li><router-link to="/shows" class="aus">Shows</router-link></li>
                    <li><router-link to="/theatres" class="aus">Theatres</router-link></li>
                </div>
            </div>
            <div class="right-contentus">
                <div>
                    <router-link to="/bookings" class="a1">
                        <i class="fa fa-shopping-cart" style="font-size:24px;color:white"></i></router-link>
                    <span @click="logout" style="cursor: pointer;">
                        <i class="fa fa-sign-out" style="font-size:24px;color:white; padding: 15px;"
                            @click="logoutuser"></i></span>
                </div>
            </div>
        </section>
        <br><br>
        <h2 class="sg-titleus" style="margin-left: 40px;"> Rate {{ showname }}:</h2>
        <br>
        <section class="main-container1" style="height: 100vh;">
            <div class="mainb">
                <div>
                    <p><span class="star-rating">
                            <h2>Rate out of 10</h2><br><br>
                            <div style="display: flex;justify-content: center;">
                                <label for="rate-1" style="--i:1"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-1" value="1" v-model="selectedRating">
                                <label for="rate-2" style="--i:2"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-2" value="2" checked v-model="selectedRating">
                                <label for="rate-3" style="--i:3"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-3" value="3" v-model="selectedRating">
                                <label for="rate-4" style="--i:4"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-4" value="4" v-model="selectedRating">
                                <label for="rate-5" style="--i:5"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-5" value="5" v-model="selectedRating">
                                <label for="rate-6" style="--i:6"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-6" value="6" v-model="selectedRating">
                                <label for="rate-7" style="--i:7"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-7" value="7" v-model="selectedRating">
                                <label for="rate-8" style="--i:8"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-8" value="8" v-model="selectedRating">
                                <label for="rate-9" style="--i:9"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-9" value="9" v-model="selectedRating">
                                <label for="rate-10" style="--i:10"><i class="fa-solid fa-star"></i></label>
                                <input type="radio" name="rating" id="rate-10" value="10" v-model="selectedRating">
                            </div>
                        </span></p>

                </div><br>
                <p>Selected Rating: {{ selectedRating }}</p>
                <button class="button" @click="rateshow()">SUBMIT</button>
            </div>
        </section>
    </div>
</template>
<script>
import axios from 'axios'
import router from '../router';
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            selectedRating: 1,
            movies: []
        }
    },
    computed: {
        showname() {
            const shows = JSON.parse(localStorage.getItem('movies'))
            const thisshow = shows.filter(show => show.id === parseInt(this.$route.params.sid))
            return thisshow.map(show => show.name).join()
        }
    },
    methods: {
        ...mapActions(['logout']),
        rateshow() {
            const token = localStorage.getItem('token');
            const headers = {
                Authorization: `Bearer ${token}`,
            };

            const data = {
                rate: this.selectedRating,
                show: this.$route.params.sid
            };

            axios
                .post('http://localhost:5000/rate', data, { headers })
                .then((response) => {
                    // Handle the successful response if needed
                    console.log('Booking success:', response.data);
                    if (response.data.message === 'successfull') {
                        alert("Successfully rated,Redirecting to your bookings")
                        router.push('/bookings')
                    }
                    else {
                        alert("try again :(")

                    }
                })
                .catch((error) => {
                    // Handle the error if there is any
                    if (error.response.status == 401) {
                        this.$store.dispatch('handleUnauthorized')
                        alert("Unauthorized error...redirecting to login")
                    }
                    else {
                        alert("Cant rate sorry")
                    }
                });
                
        },
        async filterMoviesAsync() {
                try {
                    await this.$store.dispatch('fetchMovies');
                    this.movies = localStorage.getItem('movies')
                } catch (error) {
                    console.error('Error fetching theatres:', error);
                    return [];
                }
            },
        saveLastVisitedUrl() {
            const currentUrl = this.$route.fullPath;
            localStorage.setItem('lastVisitedUrl', currentUrl);
        },
        logoutuser() {
            this.$store.dispatch('logout')
        },
    },
    created() {
        window.addEventListener('beforeunload', this.saveLastVisitedUrl);
        this.filterMoviesAsync()

    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrl);

    },

}
</script>
<style scoped>
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';

@import 'https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T';

@import '../assets/styles/rateshow.css';
</style>