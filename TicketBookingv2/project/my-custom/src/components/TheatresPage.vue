<template>
    <div class="theatres">
        <section class="top-barus">
            <div class="left-contentus">
                <h2 class="title1us">BookMyMovie</h2>
                <div class="navigationus">
                    <li><router-link to="/shows" class="aus">Shows</router-link></li>
                    <li><router-link to="/theatres" class="activeus aus">Theatres</router-link></li>
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
        <div class="container" style="padding: unset;">
            <input class="nosubmit1 input1" type="search"
                placeholder="Search your favorite theatre based on name,location or place" v-model="searchTheatre">
        </div>
        <br>
        <section class="main-container1">
            <div class="movies-container1">
                <div class="upcoming-img-box1">
                    <img class="image1" src="../assets/images/ad.jpg" alt="Ad">
                    <p class="upcoming-title1">Ad space</p>
                </div>
                <div v-if="Theatres.length > 0" class="current-movies1">
                    <div v-for="theatre in Theatres" :key="theatre.id" class="current-movie1">
                        <div class="cm-img-box1">
                            <img class="image1" src='../assets/images/theatre.jpg' alt="Movie Poster">
                        </div>
                        <h3 class="movie-title1">{{ theatre.name }}</h3><br>
                        <p v-if="!parame" class="screen-nameus">Capacity: {{ theatre.capacity }}</p>
                        <p v-else class="screen-nameus">Available seats: {{ seats(theatre.id) }}</p>
                        <p class="screen-nameus">Location: {{ theatre.place }},{{ theatre.location }}</p><br>
                        <div class="booking1" style="padding-bottom: 10px;">
                            <p v-if="parame" class="screen-name1">Price: &#8377;{{ price(theatre.id) }}</p>
                            <router-link :to="`/shows/${theatre.id}`" v-if="!parame" class="btnus aus"
                                style="color: black;">See running
                                movies</router-link>
                            <router-link :to="`/booktickets/${theatre.id}/${mid(theatre.id)}`" v-else class="btnus aus"
                                style="color: black;" v-bind:class="{ 'disabled-link': isDisabled }">{{ message }}
                            </router-link>
                            <button @click="triggerceleryjob(theatre.id, theatre.name)" v-if="!parame" class="btnus aus"
                                style="color: black;">Download
                                Theatre's performance</button>
                        </div>
                    </div>
                </div>
                <h2 v-else class="sg-title1" style="height: 100vh">Sorry, No theatres available :/
                </h2>
            </div>
        </section>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import axios from 'axios'
import { saveAs } from 'file-saver';
import router from "../router"

export default {
    data() {
        return {
            theatres: [],
            searchTheatre: '',
            message: 'Book Tickets',
        };
    },
    computed: {
        Theatres() {
            if (!this.theatres || this.theatres.length === 0) {
                this.filterTheatresAsync();
                return [];
            }
            else {
                if (!this.searchTheatre) {
                    return this.theatres;
                } else {
                    const searchWords = this.searchTheatre.trim().toLowerCase().split(' ');
                    return this.theatres.filter(theatre => {
                        const nameMatches = searchWords.every(word => theatre.combined.toLowerCase().includes(word));
                        return nameMatches;
                    });
                }
            }
        },
    },
    methods: {
        ...mapActions(['fetchTheatres', 'logout', 'fetchMovies']),
        async filterTheatresAsync() {
            try {
                await this.$store.dispatch('fetchTheatres');
                await this.$store.dispatch('fetchMovies');
                this.theatres = JSON.parse(localStorage.getItem('theatres'));
                console.log(this.theatres)
            } catch (error) {
                console.error('Error fetching theatres:', error);
                return [];
            }
        },
        seats(number) {
            const movies = JSON.parse(localStorage.getItem('movies'))
            const show = movies.filter(movie => movie.venue_no === number && movie.name.toLowerCase() === this.parame.toLowerCase())
            const seat = parseInt(show.map(movie => movie.seatsavailable))
            if (seat == 0) {
                this.isDisabled = true;
                this.message = "Sold out"
            }
            else {
                this.isDisabled = false;
                this.message = "Book Now"
            }
            return seat

        },
        price(number) {
            const movies = JSON.parse(localStorage.getItem('movies'))
            const show = movies.filter(movie => movie.venue_no === number && movie.name.toLowerCase() === this.parame.toLowerCase())
            return parseInt(show.map(movie => movie.price))
        },
        mid(number) {
            const show = JSON.parse(localStorage.getItem('movies'))
            const filtered = show.filter(show => show.venue_no == number && show.name == this.parame)
            return parseInt(filtered.map(filter => filter.id))
        },
        triggerceleryjob(number, name) {
            fetch(`http://127.0.0.1:5000/trigger-celery-job/${number}`)
                .then(r => r.json())
                .then(d => {
                    console.log("Celery task details", d);
                    alert("downloading please wait")
                    let interval = setInterval(() => {
                        fetch(`http://127.0.0.1:5000/status/${d.Task_ID}`).then(r => r.json()
                        ).then(d => {
                            if (d.Task_State === "SUCCESS") {
                                alert("downloaded successfully")
                                clearInterval(interval);
                                const vname = name.replace(/\s/g, "")
                                window.location.href = `http://127.0.0.1:5000/openfile/${vname}`;
                            }
                            else {
                                console.log("task still executing")
                            }
                        })
                    }, 4000);
                })
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
        this.filterTheatresAsync()

    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrl);

    },
}

</script>

<style scoped>
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css';


@import '../assets/styles/theatre.css';
</style>