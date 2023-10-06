<template>
    <div class="buytickets userboard">
        <section class="top-barus" style="background-color: black;">
            <div class="left-contentus">
                <h1 class="title1us">BookMyMovie</h1>
                <div class="navigationus">
                    <li><router-link to="/shows" class="aus">Shows</router-link></li>
                    <li><router-link to="/theatres" class="activeus aus">Theatres</router-link></li>
                </div>
            </div>
            <div class="right-contentus">
                <div>
                    <router-link to="/bookings" class="aus">
                        <i class="fa fa-shopping-cart" style="font-size:24px;color:white"></i></router-link>
                    <span @click="logout" style="cursor: pointer;">
                        <i class="fa fa-sign-out" style="font-size:24px;color:white; padding: 15px;"
                            @click="logoutuser"></i>
                    </span>
                </div>
            </div>
        </section>
        <br>
        <h2 class="righttitle">Buy tickets for {{ mname }}:</h2>
        <div class="cardWrap">
            <div class="card cardLeft">
                <br>
                <div class="h1a">{{ tname }} </div>
                <div class="title4">
                    <div class="h2">{{ mname }}</div>
                    <span class="span">movie</span>
                </div>
                <div class="name1">
                    <h2 class="h2">{{ username }}</h2>
                    <span class="span">name</span>
                </div>
                <div class="name1">
                    <h2 class="h2">{{ tlname }},{{ tpname }}</h2>
                    <span class="span">Location</span>
                </div>
                <div>
                    <div class="seat">
                        <h2 class="h2">{{ counter }}</h2>
                        <span class="span">No of tickets</span>
                    </div>
                    <div class="time">
                        <div class="h2">{{ mstime }}</div>
                        <span class="span">time</span>
                    </div>
                </div><br>
                <div>Tickets Quantity:
                    <button @click="decreasecounter" class="quantity-btn quantity-btn-left">-</button>
                    <input style="font-size: 20px;width: 36px;" type="number" v-model="counter" min="1"
                        @input="preventNegativeInput" />
                    <button @click="increasecounter" class="quantity-btn quantity-btn-right">+</button>
                </div>
            </div>
            <div class="card cardRight"><br><br>
                <div class="number"><br>
                    <div class="h4">&#8377;{{ mprice * counter }}</div>
                    <span class="span">price</span>
                </div><br><br>
                <div style="margin-left: -10px;">
                    <div class="barcode"></div><br><br>
                    <div>
                        <div class="booking1" style="margin-left: 20px;"> 
                            <button @click="booking" class="btnus aus butt1">Book</button>
                        </div>
                    </div>
                </div>
                <br><br>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios';
import router from '../router';
import { mapActions } from 'vuex';
export default {
    data() {
        return {
            counter: 1,
            tid: parseInt(this.$route.params.tid),
            mid: parseInt(this.$route.params.mid),
            countercheck: false,
            movies: [],
            theatres: [],
            username: localStorage.getItem('userusername')
        }
    },
    computed: {
        tname() {
            return this.gettheatrefiltered().map(theatre => theatre.name).join()
        },
        tpname() {
            return this.gettheatrefiltered().map(theatre => theatre.place).join()
        },
        tlname() {
            return this.gettheatrefiltered().map(theatre => theatre.location).join()
        },
        mname() {
            return this.getmoviefiltered().map(movie => movie.name).join()
        },
        mprice() {
            return this.getmoviefiltered().map(movie => movie.price).join()
        },
        mstime() {
            return this.getmoviefiltered().map(movie => movie.starttime).join()
        },
        mseatsavailable() {
            return this.getmoviefiltered().map(movie => movie.seatsavailable).join()
        },
    },
    methods: {
        ...mapActions(['fetchTheatres', 'fetchMovies', 'logout']),
        async filterTheatresAsync() {
            try {
                await this.$store.dispatch('fetchTheatres');
                this.theatres = JSON.parse(localStorage.getItem('theatres'));
                console.log("theatres data", this.theatres)
            } catch (error) {
                console.error('Error fetching theatres:', error);
                return [];
            }
        },
        async filterMoviesAsync() {
            try {
                await this.$store.dispatch('fetchMovies');
                this.movies = JSON.parse(localStorage.getItem('movies'));
                console.log("theatres data", this.movies)
            } catch (error) {
                console.error('Error fetching theatres:', error);
                return [];
            }
        },
        increasecounter() {
            if (this.counter > this.mseatsavailable - 1) {
                this.counter = this.mseatsavailable - 1
            }
            return this.counter++
        },
        decreasecounter() {
            if (this.counter < 2) {
                return this.counter = 1;
            }
            return this.counter--
        },
        getmoviefiltered() {
            return this.movies.filter(movie => movie.venue_no === this.tid && movie.id === this.mid)

        },
        gettheatrefiltered() {
            return this.theatres.filter(theatre => theatre.id === this.tid)

        },
        preventNegativeInput() {
            if (this.counter < 2) {
                this.counter = 1;
            }
            else if (this.counter >= parseInt(this.mseatsavailable)) {
                this.counter = this.mseatsavailable
                console.log(this.counter)
            }
        },
        booking() {
            const token = localStorage.getItem('token');
            const headers = {
                Authorization: `Bearer ${token}`,
            };

            const data = {
                mid: this.mid,
                counter: this.counter,
            };

            axios
                .post('http://localhost:5000/booking', data, { headers })
                .then((response) => {
                    // Handle the successful response if needed
                    console.log('Booking success:', response.data);
                    if (response.data.message === 'successfull') {
                        alert("Thank you...Booking Successfull...Redirecting to your bookings")
                        router.push('/bookings')
                    }
                    else {
                        alert("try again :(")

                    }
                })
                .catch((error) => {
                    // Handle the error if there is any
                    console.error('Error booking:', error);
                    alert("Session expired...redirecting to login")
                    router.push('/login')
                });

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
        this.filterMoviesAsync();
        this.filterTheatresAsync()

    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrl);

    },
}
</script>

<style scoped>
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css';

@import 'https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T';

@import '../assets/styles/buytickets.css';
</style>

