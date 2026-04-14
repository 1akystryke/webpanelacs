<template>
  <v-app>

    <!-- SIDEBAR -->
    <v-navigation-drawer v-model="drawer" permanent>
      <v-container>

        <v-row>
          <v-col>
            <div class="text-h6">
              Assetto Corsa Server Manager
            </div>
          </v-col>
        </v-row>

        <v-divider class="my-2" />

        <v-list density="compact">

          <v-list-item
            v-for="item in menuItems"
            :key="item.title"
            :to="item.to"
            router
            @click="handleClick(item)"
          >
            <v-list-item-title>
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
          <v-col>
          <v-btn :onclick="startServer">Start</v-btn>
          <v-btn :onclick="stopServer">Stop</v-btn>
          {{ menuCount }}
          <v-chip v-if="serverInfo.status==='online'" :color="'green'" variant="flat">
            online
          </v-chip>
          <v-chip v-else :color="'red'" variant="flat">
            offline
          </v-chip>
          <v-btn :onclick="ebaniyStatus">ebat?</v-btn>
          </v-col>
        </v-list>

      </v-container>
    </v-navigation-drawer>

    

    <!-- MAIN CONTENT -->
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>

  </v-app>
</template>

<script setup>
import { ref } from 'vue'

/* =======================
   DATA (state)
======================= */
const drawer = ref(true)
let serverInfo = {}
let csrfToken = ""
const menuItems = ref([
  { title: 'Home', to: '/' },
  { title: 'Session', to: '/session' },
  { title: 'Players', to: '/players' },
  { title: 'Content', to: '/content' },
  { title: 'Presets', to: '/presets' },
  { title: 'Logs', to: '/logs' },
])

/* =======================
   COMPUTED
======================= */




/* =======================
   METHODS
======================= */
async function getStatus() {
  const url = "api/info"
  const response = await fetch(url);
  serverInfo = await response.json()
}
async function stopServer() {
  await api('/api/server/stop', {
    method: 'POST'
  });
  await getStatus()
}
async function startServer() {
  await api('/api/server/start', {
    method: 'POST'
  });
  await getStatus()

}

function ebaniyStatus(){
  alert(serverInfo.status)
}


function handleClick(item) {
  console.log('Clicked:', item.title)
}

async function api(url, opts = {}) {
          const opt = {
            ...opts
          };
          opt.headers = {
            ...(opt.headers || {})
          };
          if (opt.method && opt.method !== 'GET' && csrfToken) opt.headers['X-CSRF-Token'] = csrfToken;
          try {
            const res = await fetch(url, opt);
            if (res.status === 401) {
              window.location.href = `/login?next=${encodeURIComponent(window.location.pathname || '/')}`;
              return {}
            }
            if (!res.ok) return {};
            return await res.json()
          } catch (e) {
            console.warn(e);
            return {}
          }
        }
async function fetchCsrf() {
  try {
    const r = await fetch('/api/csrf');
    if (r.ok) {
      const d = await r.json();
      csrfToken = d.token || ''
    }
  } catch (e) {
    console.log(e)
  }
}

fetchCsrf()
getStatus()
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>