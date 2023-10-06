<template>
    <div class="userboard">
        <section class="top-barus">
            <div class="left-contentus">
                <h1 class="title1us">BookMyMovie</h1>
                <div class="navigationus">
                    <li><router-link to="/shows" class="activeus aus">Shows</router-link></li>
                    <li><router-link to="/theatres" class="aus">Theatres</router-link></li>
                </div>
            </div>
            <div class="right-contentus">
                <div>
                    <router-link to="/bookings" class="aus">
                        <i class="fa fa-shopping-cart" style="font-size:24px;color:white; padding: 15px;"></i></router-link>
                    <span @click="logout" style="cursor: pointer;">

                        <i class="fa fa-sign-out" style="font-size:24px;color:white" @click="logoutuser"></i></span>
                </div>
            </div>
        </section>
        <section class="main-containerus">
            <div class="sidebarus">
                <div class="container1us">
                    <input class="nosubmit inputus" style="margin-left: -20px;" type="search"
                        placeholder="Search your favorite movies" v-model="searchitem">
                </div><br>
                <div class="sidebarus-groups">
                    <h3 class="sg-titleus">Filter based on Categories:</h3>
                    <input type="checkbox" value="adventure" v-model="selectedGenres" class="inputus">
                    <label for="Adventure" class="labelus">Adventure</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Action" class="inputus">
                    <label for="Action" class="labelus">Action</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Animation" class="inputus">
                    <label for="Animation" class="labelus">Animation</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Comedy" class="inputus">
                    <label for="Comedy" class="labelus">Comedy</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Science" class="inputus">
                    <label for="Science" class="labelus">Science Fiction</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Thriller" class="inputus">
                    <label for="Thriller" class="labelus">Thriller</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="History" class="inputus">
                    <label for="History" class="labelus">History</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Documentary" class="inputus">
                    <label for="Documentary" class="labelus">Documentary</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Fantasy" class="inputus">
                    <label for="Fantasy" class="labelus">Fantasy</label><br>
                    <input type="checkbox" v-model="selectedGenres" value="Horror" class="inputus">
                    <label for="Horror" class="labelus">Horror</label><br>
                </div>
                <div class="sidebar-groups">
                    <h3 class="sg-titleus">Filter based on Ratings:</h3>
                    <input type="checkbox" value="9" v-model="selectedRatings" class="inputus">
                    <label for="9" class="labelus">9-10</label><br>
                    <input type="checkbox" value="8" v-model="selectedRatings" class="inputus">
                    <label for="8" class="labelus">8-9</label><br>
                    <input type="checkbox" value="7" v-model="selectedRatings" class="inputus">
                    <label for="7" class="labelus">7-8</label><br>
                    <input type="checkbox" value="6" v-model="selectedRatings" class="inputus">
                    <label for="6" class="labelus">6-7</label><br>
                    <input type="checkbox" value="5" v-model="selectedRatings" class="inputus">
                    <label for="5" class="labelus">5-6</label><br>
                    <input type="checkbox" value="4" v-model="selectedRatings" class="inputus">
                    <label for="4" class="labelus">4-5</label><br>
                    <input type="checkbox" value="3" v-model="selectedRatings" class="inputus">
                    <label for="3" class="labelus">3-4</label><br>
                    <input type="checkbox" value="2" v-model="selectedRatings" class="inputus">
                    <label for="2" class="labelus">2-3</label><br>
                    <input type="checkbox" value="1" v-model="selectedRatings" class="inputus">
                    <label for="1" class="labelus">1-2</label><br>
                </div>
            </div>
            <div class="movies-container">
                <div class="upcoming-img-box">
                    <img class="imageus" src="../assets/images/Oppie.jpeg" alt="">
                    <p class="upcoming-title">Upcoming Movie</p>
                    <div class="buttonsus">
                        <a href="theatres/Oppenheimer/date" class="btnus aus">Book Now</a>
                        <a href="https://www.youtube.com/watch?v=uYPbbksJxIg&t=3s" class="btnus-alt btnus aus">Play Trailer</a>
                    </div>
                </div>
                <h2 v-if="theatrename != ''" class="sg-titleus">Shows in {{ theatrename }} </h2>
                <br>
                <div v-if="Shows && Shows != 0" class="current-movies">
                    <div v-for="movie in Shows" :key="movie.id" class="current-movie">
                        <div class="cm-img-box">
                            <img class="imageus" :src="require(`@/assets/images/${movie.name}.jpg`)" alt="Movie Poster">
                        </div>
                        <h3 class="movie-title">{{ movie.name }}</h3><br>
                        <p class="screen-nameus">Rating : {{ movie.rate }}/10</p>
                        <p v-if="theatreid" class="screen-nameus">Tickets available: {{ movie.seatsavailable }}</p>
                        <p v-if="theatreid" class="screen-nameus">Date : {{ movie.date }}</p>

                        <div class="booking">
                            <br>
                            <router-link :to="`/theatres/${movie.name}/date`" v-if="!theatreid"
                                class="btnus a1" style="color: black;">See in
                                theatres</router-link>
                            <router-link :to="`/booktickets/${movie.venue_no}/${movie.id}`" v-else class="btnus a1"
                                style="color: black;"
                                v-bind:class="{ 'disabled-link': isDisabled(movie.seatsavailable), 'bgchange': isDisabled(movie.seatsavailable) }">{{
                                    message }}
                            </router-link>
                        </div>
                    </div>
                </div>
                <h2 v-else class="sg-titleus">Sorry, No movies available :/
                </h2>          

            </div>
        </section>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
    data() {
        return {
            movies: [],
            theatreid: this.$route.params.id,
            selectedGenres: [],
            selectedRatings: [],
            searchitem: '',
            message: '',
        };
    },
    computed: {
        ...mapState(['loading']),
        Shows() {
            if (!this.movies || this.movies === 0) {
                console.log("Inside shows()")
                this.filterMoviesAsync();
                return [];
            }
            else {
                if (this.searchitem === '') {
                    return this.filteredMoviesfinal
                }
                else {
                    if (this.selectedGenres.length === 0 && this.selectedRatings.length === 0) {
                        return this.filteredMoviesfinal.filter((movie) => movie.name.toLowerCase().includes(this.searchitem));
                    }
                    else {
                        return this.filteredMoviesfinal.filter((movie) =>
                            movie.name.toLowerCase().includes(this.searchitem));
                    }

                }
            }
        },
        uniqueShows() {
            const uniqueShowsMap = new Map();
            this.movies.forEach(show => {
                if (!uniqueShowsMap.has(show.name) || uniqueShowsMap.get(show.name).rate < show.rate) {
                    uniqueShowsMap.set(show.name, show);
                }
            });
            return Array.from(uniqueShowsMap.values());
        },

        theatrename() {
            const theatreId = parseInt(this.$route.params.id);
            const theatres = JSON.parse(localStorage.getItem('theatres')) || [];
            const theatre = theatres.find(theatre => parseInt(theatre.id) === theatreId);
            return theatre ? theatre.name : '';
        },
        filteredShows() {
            const param = this.$route.params.id;
            if (!param) {
                return this.uniqueShows;
            }
            return this.movies.filter(movie => parseInt(movie.venue_no) === parseInt(param))
        },
        filteredMovies() {
            if (this.selectedGenres.length === 0) {
                return this.filteredShows; // If no genres selected, return all movies
            } else {
                return this.filteredShows.filter((movie) =>
                    this.selectedGenres.every((genre) => movie.tags.includes(genre))
                );
            }

        },
        filteredMoviesfinal() {
            if (this.selectedRatings.length === 0) {
                return this.filteredMovies
            }
            else {
                const min = Math.min(...this.selectedRatings)
                const max = Math.max(...this.selectedRatings)
                return this.filteredMovies.filter(movie => movie.rate >= min && movie.rate <= max + 1)
            }
        },
    },
 
    methods: {
        ...mapActions(['fetchMovies', 'fetchTheatres', 'logout']),
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
        isDisabled(number) {
            if (number == 0) {
                this.message = "Sold out"
                return true
            }
            this.message = "Book Now"
            return false
        },
        saveLastVisitedUrl() {
            const currentUrl = this.$route.fullPath;
            localStorage.setItem('lastVisitedUrl', currentUrl);
        },
        logoutuser() {
            this.$store.dispatch('logout')
        }

    },
    created() {
        window.addEventListener('beforeunload', this.saveLastVisitedUrl);
        this.filterMoviesAsync();



    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrl);

    }

};
</script>
<style scoped>
@import '../assets/styles/userdashboard.css';
</style>