<template>
    <div>
        <div class="header">
            <a href="#default" class="logo title3 a9">Hello {{ username }}</a>
            <div class="header-right">
                <router-link to="/admindash" class="active a9" >Home</router-link>
                <a class="a9 a7" @click="logoutadmin">logout</a>
            </div>
        </div>
        <div class="formcv-style-2">
            <div class="formcv-style-2-heading">Create Venue</div>
            <form @submit.prevent="createvenue" method="post">
                <label class="labelcv" for="field1"><span class="spancv">Venue Name <span
                            class="spancv required">*</span></span><input type="text" class="input-field" name="vname"
                        v-model="Venuefin.vname" required /></label>
                <label class="labelcv" for="field2"><span class="spancv">Place <span
                            class="spancv required">*</span></span><input type="text" class="input-field"
                        v-model="Venuefin.vplace" required /></label>
                <label class="labelcv" for="field2"><span class="spancv">Location <span
                            class="spancv required">*</span></span><input type="text" v-model="Venuefin.vlocation"
                        class="input-field" name="vlocation" required /></label>
                <label class="labelcv" for="field2"><span class="spancv">Capacity <span
                            class="spancv required">*</span></span><input type="number" class="input-field" name="vcapacity"
                        v-model="Venuefin.vcapacity" required /></label>
                <p v-if="!params">{{ message }}</p>
                <button v-if="!params" class="inputcv" type="submit" :disabled="isVenueDuplicate()">Submit</button>
                <button v-else class="inputcv" type="submit">Update</button>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import router from '../router'
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            username: localStorage.getItem('username'),
            params: this.$route.params.id,
            Venuefin: {
                vid: this.$route.params.id,
                vname: '',
                vplace: '',
                vlocation: '',
                vcapacity: '',
            }
        }
    },
    computed: {
        message() {
            if (this.isVenueDuplicate()) {
                return "Alert: Already exists"
            }
            return ""
        },
    },
    methods: {
        ...mapActions(['logoutadmin']),
        async createvenue() {
            const token = localStorage.getItem('admintoken')
            const data = {
                vname: this.Venuefin.vname,
                vplace: this.Venuefin.vplace,
                vlocation: this.Venuefin.vlocation,
                vcapacity: this.Venuefin.vcapacity,
            };
            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            }
            // Dispatch Vuex action to handle login
            if (!this.params) {
                try {
                    const response = await axios.post('http://127.0.0.1:5000/admin/createvenue', data, config);
                    alert(response.data.message)
                    router.push('/admindash')

                }
                catch (error) {
                    if (error.response.status === 401 || error.response.status === 422) {
                        alert("Session expired,redirecting to login")
                        localStorage.removeItem('admintoken')
                        router.push('/admin/login')
                    }
                    else {
                        alert(error.response.message)
                    }
                }
            }
            else {
                try {
                    const response = await axios.put('http://127.0.0.1:5000/admin/updatevenue', this.Venuefin, config);
                    alert(response.data.message)
                }
                catch (error) {
                    if (error.response.status === 401 || error.response.status === 422) {
                        alert("Session expired,redirecting to login")
                        localStorage.removeItem('admintoken')
                        router.push('/admin/login')
                    }
                    else {
                        alert(error.response.message)
                    }
                }
                const lastVisitedUrl = localStorage.getItem('lastVisitedUrladm');
                if (lastVisitedUrl) {
                    this.$router.replace(lastVisitedUrl);
                } else {
                    this.$router.replace('/admindash');
                }
            }

        },
        isVenueDuplicate() {
            const venue = JSON.parse(localStorage.getItem('venue')) || []
            if (venue.length > 0) {
                return venue.some(
                    v =>
                        v.venuename.toLowerCase() === this.Venuefin.vname.toLowerCase() &&
                        v.place.toLowerCase() === this.Venuefin.vplace.toLowerCase() &&
                        v.location.toLowerCase() === this.Venuefin.vlocation.toLowerCase()
                )
            }
            return false
        },
        FilterVenue() {
            if (this.$route.params.id) {
                const venue = JSON.parse(localStorage.getItem('venue'))
                console.log(venue)
                const venuesfiltered = venue.filter(venue => parseInt(venue.id) === parseInt(this.params))
                console.log(venuesfiltered)
                console.log(this.Venuefin)
                this.Venuefin.vname = venuesfiltered[0].venuename,
                    this.Venuefin.vplace = venuesfiltered[0].place,
                    this.Venuefin.vlocation = venuesfiltered[0].location,
                    this.Venuefin.vcapacity = venuesfiltered[0].capacity
            }
        }
    },
    saveLastVisitedUrladm() {
        const currentUrl = this.$route.fullPath;
        localStorage.setItem('lastVisitedUrladm', currentUrl);
    },
    logoutuser(){
        this.$store.dispatch('logoutadmin')
    },
    created() {
        window.addEventListener('beforeunload', this.saveLastVisitedUrladm);
    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrladm);

    },
    mounted() {
        this.FilterVenue()
    }
}

</script>
<style scoped>
@import '../assets/styles/admincreatevenue.css';
</style>
