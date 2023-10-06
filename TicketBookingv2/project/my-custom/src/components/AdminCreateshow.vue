<template>
    <div>
        <div class="header">
            <a href="/admindash" class="logo title3 a9">Hello {{ username }}</a>
            <div class="header-right">
                <a class="active a9" href="">Home</a>
                <a class="a9" @click="logoutadmin">logout</a>
            </div>
        </div>
        <div class="formcv-style-2">
            <div class="formcv-style-2-heading">Create Show</div>
            <form @submit.prevent="createshow" method="post">
                <label class="labelcv" for="field1"><span class="spancv">Show Name <span
                            class="spancv required">*</span></span><input type="text" class="input-field" name="vname"
                        v-model="Showfin.sname" required /></label>
                <label class="labelcv" for="field2"><span class="spancv">Tags <span
                            class="spancv required">*</span></span><input type="text" class="input-field"
                        v-model="Showfin.stags" required /></label>
                <label class="labelcv" for="field2"><span class="spancv">Rating <span
                            class="spancv required">*</span></span><input type="number" v-model="Showfin.srating"
                        class="input-field" name="rating" required min="1" max="10" step="0.01" /></label>
                <label class="labelcv" for="field2"><span class="spancv">Start Time(in 24hrs format) <span
                            class="spancv required">*</span></span><input type="text" v-model="Showfin.sstime"
                        class="input-field" name="starttime" required /></label>
                <label class="labelcv" for="field2"><span class="spancv">End Time(in 24hrs format) <span
                            class="spancv required">*</span></span><input type="text" v-model="Showfin.setime"
                        class="input-field" name="endtime" required /></label><br>
                <label class="labelcv" for="field2"><span class="spancv">Movie play date(in yyyy-mm-dd): <span
                            class="spancv required">*</span></span><input type="text" v-model="Showfin.sdate"
                        class="input-field" name="endtime" pattern="\d{4}-\d{2}-\d{2}" required /></label><br>
                <label class="labelcv" for="field2"><span class="spancv">Price <span
                            class="spancv required">*</span></span><input type="number" class="input-field" name="vcapacity"
                        v-model="Showfin.sprice" required /></label><br>
                <input v-if="!params" type="file" ref="imageInput" @change="handleImageUpload" required><br>
                <p class="sg-title1" v-if="!params">{{ message }}</p>
                <button v-if="!params" class="inputcv" type="submit" :disabled="isShowDuplicate()">Submit</button>
                <button v-else class="inputcv" type="submit">Update</button>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import router from '../router'
import { mapActions } from 'vuex'
export default {
    data() {
        return {
            username: localStorage.getItem('username'),
            params: this.$route.params.sid,
            imageFile: null,
            Showfin: {
                sid: this.$route.params.sid,
                sname: '',
                stags: '',
                srating: '',
                sstime: '',
                setime: '',
                sprice: '',
                sdate: '',
                vid: this.$route.params.vid,
            }
        }
    },
    computed: {
        message() {
            if (this.isShowDuplicate()) {
                return "Alert: Already exists"
            }
            return ""
        },
    },
    methods: {
        ...mapActions(['logoutadmin']),
        handleImageUpload(event) {
            this.imageFile = event.target.files[0];
        },
        async createshow() {
            const token = localStorage.getItem('admintoken')
            const data = {
                vid: this.Showfin.vid,
                sname: this.Showfin.sname,
                stags: this.Showfin.stags,
                srating: this.Showfin.srating,
                sstime: this.Showfin.sstime,
                setime: this.Showfin.setime,
                sprice: this.Showfin.sprice,
                sdate: this.Showfin.sdate
            };
            console.log(data)
            const config = {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            }
            // Dispatch Vuex action to handle login
            if (!this.params) {
                try {
                    const response = await axios.post('http://127.0.0.1:5000/admin/createshow', data, config);
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
                if (!this.imageFile) {
                    alert("upload image")
                }
                const formData = new FormData();
                formData.append('image', this.imageFile);
                formData.append('moviename',this.Showfin.sname)
                try {
                    console.log("inside try")
                    const response = await fetch('http://127.0.0.1:5000/uploadimage', {
                        method: 'POST',
                        body: formData,
                    });

                    if (response.ok) {
                        alert('Image uploaded successfully');
                        router.push('/admindash')
                    } else {
                        alert('Image upload failed');
                    }
                } catch (error) {
                    console.error('An error occurred:', error);
                }

            }
            else {
                try {
                    const response = await axios.put('http://127.0.0.1:5000/admin/updateshow', this.Showfin, config);
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
        isShowDuplicate() {
            const show = JSON.parse(localStorage.getItem('show')) || []
            if (show.length > 0) {
                return show.some(
                    s =>
                        s.name.toLowerCase() === this.Showfin.sname.toLowerCase() &&
                        s.starttime === this.Showfin.sstime &&
                        s.endtime === this.Showfin.setime &&
                        s.date === this.Showfin.sdate
                )
            }
            return false
        },
        FilterShow() {
            if (this.$route.params.sid) {
                const show = JSON.parse(localStorage.getItem('show'))
                const showsfiltered = show.filter(show => parseInt(show.id) === parseInt(this.params))
                this.Showfin.sname = showsfiltered[0].name,
                    this.Showfin.srating = showsfiltered[0].rate,
                    this.Showfin.stags = showsfiltered[0].tag,
                    this.Showfin.sstime = showsfiltered[0].starttime,
                    this.Showfin.setime = showsfiltered[0].endtime,
                    this.Showfin.sprice = showsfiltered[0].price
                this.Showfin.sdate = showsfiltered[0].date

            }
        },
    },
    saveLastVisitedUrladm() {
        const currentUrl = this.$route.fullPath;
        localStorage.setItem('lastVisitedUrladm', currentUrl);
    },
    logoutuser() {
        this.$store.dispatch('logoutadmin')
    },
    created() {
        window.addEventListener('beforeunload', this.saveLastVisitedUrladm);
    },
    beforeDestroy() {
        window.removeEventListener('beforeunload', this.saveLastVisitedUrladm);

    },
    mounted() {
        this.FilterShow()
    }
}

</script>
<style scoped>
@import '../assets/styles/admincreatevenue.css';
</style>

