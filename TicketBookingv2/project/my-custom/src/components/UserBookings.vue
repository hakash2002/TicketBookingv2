<template>
    <div class="theatres">
        <section class="top-barus">
            <div class="left-contentus">
                <h2 class="title1us">BookMyMovie</h2>
                <div class="navigationus">
                    <li><router-link to="/shows" class="aus">Shows</router-link></li>
                    <li><router-link to="/theatres" class="aus">Theatres</router-link></li>
                </div>
            </div>
            <div class="right-contentus">
                <div>
                    <router-link to="/bookings" class="aus">
                        <i class="fa fa-shopping-cart" style="font-size:24px;color: white"></i></router-link>
                    <span @click="logout" style="cursor: pointer;">
                        <i class="fa fa-sign-out" style="font-size:24px;color:white; padding: 15px;" @click="logoutuser"></i>
                    </span>
                </div>
            </div>
        </section>
        <br>
        <section class="main-container1">
            <div class="movies-container1">
                <div class="upcoming-img-box1">
                    <img class="image1" style="width: inherit;" src="../assets/images/ad.jpg" alt="">
                    <p class="upcoming-title1">Ad Space</p>
                </div>
                <h2 class="sg-title1">Your Booking history:</h2><br><br>
                <div v-if="ub.length > 0" class="current-movies1">
                    <div v-for="i in ub" :key="i.id" class="current-movie1">
                        <h3 class="movie-title">Venue: {{ i.venue_name }}</h3>
                        <br>
                        <p class="screen-nameus">Show: {{ i.show_name }}</p><br>
                        <p class="screen-nameus">Location: {{ i.location }}</p>
                        <p class="screen-nameus">Number of tickets booked: {{ i.quantity }}</p>
                        <p class="screen-nameus">Time: {{ i.start_time }}</p>
                        <p class="screen-nameus">Date: {{ i.date }}</p>
                        <div class="booking1">
                            <p></p>
                            <router-link :to="`/rate/${i.show_no}`" class="btn a1" v-if="i.rated"
                                v-bind:class="{ 'disabled-link': i.rated }" style="background-color: red;"> Already Rated
                            </router-link>
                            <router-link :to="`/rate/${i.show_no}`" class="btnus a1" v-else
                                v-bind:class="{ 'disabled-link': i.rated }" style="color: black;"> Rate this show
                            </router-link>
                        </div>
                    </div>

                </div>
                <h2 v-else class="sg-title1" style="height: 100vh">Sorry, No Bookings :/
                </h2>
            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex'

export default {
    data() {
        return {
            ub: [],
        }
    },
    methods: {
        ...mapActions(['handleUnauthorized','logout']),
        async getBookings() {
            try {
                this.loading = true
                const token = localStorage.getItem('token')
                const response = await axios.get('http://localhost:5000/userbooking', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                this.ub = response.data
                console.log(this.ub)
            }
            catch (error) {
                if (error.response.status == 401) {
                    await this.$store.dispatch('handleUnauthorized')
                    alert("Unauthorized error...redirecting to login")
                }

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
        this.getBookings();
        window.addEventListener('beforeunload', this.saveLastVisitedUrl);

    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrl);

    },
}

</script>