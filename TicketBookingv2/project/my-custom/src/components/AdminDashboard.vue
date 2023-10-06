<template>
    <div class="admindash">
        <div class="header">
            <a href="#default" class="logo title3 a9">Hello {{ username }}</a>
            <div class="header-right">
                <router-link to="/admindash" class="active a9">Home</router-link>
                <a class="a9" @click="logoutadmin">logout</a>
            </div>
        </div>
        <br>
        <div v-if="venue.length === 0">
            <br>
            <h2 style="margin-left: 10px;"> No show's or Venue Created. </h2>
            <br>
            <div style="display: flex; justify-content: center;"><router-link to="/admin/createvenue" class="btnus aus">
                    <span class="glyphicon glyphicon-plus-sign"></span> Add Venue
                </router-link></div>
        </div>
        <div v-else>
            <br>
            <div class="container-fluid">
                <div class="row gx-5 rounded">
                    <div class="col col-lg-2 " style="padding: 20px;" v-for="i in venue" :key="i.id">
                        <div class="p-3 border bg-light">
                            <h4> Venue : {{ i.venuename }} </h4>
                            <div v-if="i.shows.length === 0">
                                <h3 style="font-weight: bold;"> No shows available </h3><br>
                                <div style="display: flex; justify-content: center;"><router-link
                                        :to="`/admin/createshow/${i.id}`" class="btnus a9"><span
                                            class="glyphicon glyphicon-plus-sign"></span> Add Show</router-link>
                                </div>
                            </div>
                            <div v-else><br>
                                <h4 style="font-weight: bold;">Shows:</h4>
                                <div class="container-fluid bg-light dropdown" style="background-color: black;">
                                    <div v-for="k in i.shows" :key="k.id" class="row my-2 border">
                                        <h4 style="margin-left: 10px;">Name: {{ k.showname }}</h4>
                                        <h4 style="margin-left: 10px;">Date: {{ k.date }}</h4>
                                        <div class="container9">
                                            <button class="button9" style="margin-left: 10px;">Actions
                                                <div class="options">
                                                    <router-link :to="`/admin/updateshow/${i.id}/${k.id}`" class="option a1"
                                                        href="">Edit</router-link>
                                                    <button class="option a1" style="width: 100px"
                                                        @click="deleteshow(k.id)">Delete</button>
                                                </div>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br><br>
                            <div style="text-align: center;">
                                <button class="btnus aus" style="width:55px;background-color:#007bff;"><router-link
                                        :to="`/admin/updatevenue/${i.id}`" class="a1"
                                        style="color:black;text-decoration: none;width: 100%;">Edit</router-link></button>
                                <button @click="deletevenue(i.id)" class="btnus aus"
                                    style="background-color:#007bff ; color:black;width:60px" role="button">Delete
                                </button>
                            </div><br>
                            <div v-if="i.shows.length > 0" style="display: flex; justify-content: center;">
                                <router-link :to="`/admin/createshow/${i.id}`" class="btnus aus" style="color: black;"><span
                                        class="glyphicon glyphicon-plus-sign"></span> Add Show</router-link>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="display: flex; justify-content: center;"><router-link to="/admin/createvenue" class="btnus aus"
                        style="background-color: darkslategray;color: white;">
                        <span class="glyphicon glyphicon-plus-sign"></span> Add Venue
                    </router-link></div>
            </div>
            <br>
            <br>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import router from '../router'
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            username: localStorage.getItem('username'),
            venue: [],
        }
    },
    methods: {
        ...mapActions(['logoutadmin']),
        async getVenues() {
            try {
                const token = localStorage.getItem('admintoken');
                const response = await axios.get('http://localhost:5000/admin/venues', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                this.venue = response.data
                localStorage.setItem('venue', JSON.stringify(this.venue))
            } catch (error) {
                if (error.response.status === 401 || error.response.status === 422) {
                    alert("Unauthorized error,pushing you to login")
                    router.push('/admin/login')
                } else {
                    console.error('Error fetching data:', error);
                }
            }
        },
        async getShows() {
            try {
                const token = localStorage.getItem('admintoken');
                const response = await axios.get('http://localhost:5000/movies', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                localStorage.setItem('show', JSON.stringify(response.data))
            } catch (error) {
                if (error.response.status === 401 || error.response.status === 422) {
                    alert("Unauthorized error,pushing you to login")
                } else {
                    console.error('Error fetching data:', error);
                }
            }
        },
        async deleteshow(number) {
            const token = localStorage.getItem('admintoken');
            const data = {
                'sid': number,
            };
            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            }
            try {
                console.log(data, config, token)
                const response = await axios.delete('http://localhost:5000/admin/deleteshow',
                    {
                        data: data,
                        headers: config.headers
                    });
                alert(response.data.message)
                this.getShows()
                this.getVenues()
            }
            catch (error) {
                if (error.response.status === 401 || error.response.status === 422) {
                    alert("Unauthorized error,pushing you to login page")
                    router.push('/login')
                } else {
                    alert(error.response.message);
                }
            }
        },
        async deletevenue(number) {
            const token = localStorage.getItem('admintoken');
            const data = {
                'vid': number
            };
            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            }
            try {
                const response = await axios.delete('http://localhost:5000/admin/deletevenue',
                    {
                        data: data,
                        headers: config.headers
                    });
                alert(response.data.message)
                this.getVenues()
            }
            catch (error) {
                if (error.response.status === 401 || error.response.status === 422) {
                    alert("Unauthorized error,pushing you to login")
                    router.push('/admin/login')
                } else {
                    alert(error.response.message);
                }
            }
        },
        saveLastVisitedUrladm() {
            const currentUrl = this.$route.fullPath;
            localStorage.setItem('lastVisitedUrladm', currentUrl);
        },
    },
    logoutuser() {
        this.$store.dispatch('logoutadmin')
    },
    created() {
        window.addEventListener('beforeunload', this.saveLastVisitedUrladm);
        this.getVenues(),
            this.getShows()


    },
    beforeCreated() {
        this.getVenues()

    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrladm);

    }
}
</script>
<style scoped>
@import 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css';
@import 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css';
@import '../assets/styles/admindash.css';
</style>