<template>
  <div>
    <div>
      <img :src="$auth.user.picture">
      <h2>{{ $auth.user.name }}</h2>
      <p>{{ $auth.user.email }}</p>
    </div>
    <div>
      <button v-on:click="click">Click ME!</button>
    </div>
    <div>
      <pre>{{ JSON.stringify($auth.user, null, 2) }}</pre>
    </div>
  </div>
</template>

<script>
// import axios from 'axios'
import api from '@/service/api'
export default {
  name: 'Profile',
  methods: {
    async click () {
      api.get('/auth0').then((res) => { console.log(res) })
      // const token = await this.$auth.getTokenSilently()
      // axios.get('http://localhost:8002/auth0', {
      //   headers: {
      //     Authorization: `Bearer ${token}` // send the access token through the 'Authorization' header
      //   }
      // }).then((res) => {
      //   console.log(res)
      //   return res
      // })
    }
  }
}
</script>

<style scoped>

</style>
