<template>
  <v-app>
    <div class="app-shell">
      <ToastContainer :toasts="toasts" :remove-toast="removeToast" />

      <SidebarNav :tab="tab" :items="navItems" @update:tab="setTab" />

      <div class="main" style="flex: 1; display: flex; flex-direction: column;">
        <HeaderBar
          :title="headerTitle"
          :t="t"
          :server-status="server.status"
          :locale="locale"
          :toggle-language="toggleLanguage"
          :logout="logout"
        />

        <div class="content">
          <transition name="fade" mode="out-in">
            <DashboardView
              v-if="tab === 'dashboard'"
              key="dash"
              :server="server"
              :t="t"
              :start="start"
              :stop="stop"
            />

            <SessionView
              v-else-if="tab === 'session'"
              key="session"
              :t="t"
              :session="session"
              :tracks="tracks"
              :cars="cars"
              :weather="weather"
              :weather-list="weatherList"
              :saving="saving"
              :add-car="addCar"
              :remove-car="removeCar"
              :add-weather-slot="addWeatherSlot"
              :remove-weather-slot="removeWeatherSlot"
              :save-session="saveSession"
              :save-preset="savePreset"
              :get-car-skins="getCarSkins"
            />

            <PresetsView
              v-else-if="tab === 'presets'"
              key="presets"
              :t="t"
              :presets="presets"
              :apply-preset="applyPreset"
              :delete-preset="deletePreset"
            />

            <PlayersView
              v-else-if="tab === 'players'"
              key="players"
              :t="t"
              :server="server"
              :refresh-i-frame="refreshIFrame"
            />

            <ContentView
              v-else-if="tab === 'content'"
              key="content"
              :t="t"
              :cars="cars"
              :tracks="tracks"
              :content-search="contentSearch"
              :handle-folder="handleFolder"
              :upload-zip="uploadZip"
              :progress="progress"
              :upload-progress="uploadProgress"
              :uploading="uploading"
              :zip-ready="zipReady"
            />

            <LogsView
               v-else-if="tab === 'logs'"
              key="logs"
              :t="t"
              :logs="logs"
              :filtered-logs="filteredLogs"
              :logs-loading="logsLoading"
              :logs-auto-refresh="logsAutoRefresh"
              :logs-refresh-countdown="logsRefreshCountdown"
              :log-filter="logFilter"
              :log-levels="logLevels"
              :toggle-auto-refresh="toggleAutoRefresh"
              :clear-logs="clearLogs"
              :fetch-logs="fetchLogs"
              :get-log-level="getLogLevel"
              :get-log-level-text="getLogLevelText"
              :format-log-message="formatLogMessage"
              :set-log-filter="setLogFilter"
            />
          </transition>
        </div>
      </div>
    </div>
  </v-app>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import JSZip from 'jszip'
import { messages } from './i18n/messages'
import { useToasts } from './composables/useToasts'

import ToastContainer from './components/ToastContainer.vue'
import SidebarNav from './components/SidebarNav.vue'
import HeaderBar from './components/HeaderBar.vue'
import DashboardView from './views/DashboardView.vue'
import SessionView from './views/SessionView.vue'
import PresetsView from './views/PresetsView.vue'
import PlayersView from './views/PlayersView.vue'
import ContentView from './views/ContentView.vue'
import LogsView from './views/LogsView.vue'

const locale = ref('ru')
const tab = ref('dashboard')

const server = reactive({
  status: 'offline',
  clients: 0,
  maxclients: 0,
  track: ''
})

const zipBlob = ref(null)
const progress = ref(0)
const uploadProgress = ref(0)
const uploading = ref(false)

const contentSearch = reactive({
  cars: '',
  tracks: ''
})

const weatherList = ref([])
const presets = ref([])
const session = reactive({
  name: '',
  password: '',
  adminPassword: '',
  udpPort: 9600,
  tcpPort: 9600,
  httpPort: 8081,
  cars: [],
  track: '',
  trackVariant: '',
  trackVariants: [],
  tyreWear: 1,
  damage: 1,
  fuelConsumption: 1,
  sunAngle: 48,
  practiceDuration: 0,
  qualifyingDuration: 0,
  raceLaps: 0,
  pickupMode: 1,
  loopMode: 1,
  allowedTyresOut: 2,
  legalTyres: 'V70;',
  absAllowed: true,
  tcAllowed: true,
  stabilityAllowed: false,
  autoclutchAllowed: true,
  tyreBlanketsAllowed: true,
  forceVirtualMirror: false,
  registerToLobby: true,
  maxClients: 0
})

const weather = ref([
  {
    graphics: '3_clear',
    baseTemperatureAmbient: 18,
    baseTemperatureRoad: 6,
    variationAmbient: 1,
    variationRoad: 1
  }
])

const cars = ref([])
const tracks = ref([])
const loading = ref(false)
const csrfToken = ref('')
const saving = ref(false)

const logs = ref([])
const logsLoading = ref(false)
const logsAutoRefresh = ref(true)
const logsRefreshTimer = ref(null)
const logsRefreshCountdown = ref(10)
const logsCountdownInterval = ref(null)
const logFilter = ref('all')
const logLevels = ['all', 'error', 'warning', 'info']

const t = computed(() => messages[locale.value] || messages.ru)

const { toasts, removeToast, success, error, info } = useToasts(t)

const navItems = computed(() => [
  { key: 'dashboard', label: t.value.nav.dashboard },
  { key: 'session', label: t.value.nav.session },
  { key: 'players', label: t.value.nav.players },
  { key: 'content', label: t.value.nav.content },
  { key: 'presets', label: t.value.nav.presets },
  { key: 'logs', label: t.value.nav.logs }
])

const headerTitle = computed(() => {
  if (tab.value === 'dashboard') return t.value.dashboard.title
  if (tab.value === 'session') return t.value.session.title
  if (tab.value === 'players') return t.value.players.title
  if (tab.value === 'content') return t.value.content.title
  if (tab.value === 'presets') return t.value.presets.title
  if (tab.value === 'logs') return t.value.logs.title
})

const zipReady = computed(() => !!zipBlob.value && !uploading.value)

const filteredLogs = computed(() => {
  if (logFilter.value === 'all') return logs.value
  return logs.value.filter((log) => getLogLevel(log) === logFilter.value)
})

const getCarSkins = (carModel) => {
  const car = cars.value.find((item) => item.id === carModel)
  return car ? car.skins : []
}

const setTab = (value) => {
  tab.value = value
}

const setLogFilter = (value) => {
  logFilter.value = value
}

const toggleLanguage = () => {
  locale.value = locale.value === 'ru' ? 'en' : 'ru'
}

const addWeatherSlot = () => {
  weather.value.push({
    graphics: '3_clear',
    baseTemperatureAmbient: 18,
    baseTemperatureRoad: 6,
    variationAmbient: 1,
    variationRoad: 1
  })
}

const removeWeatherSlot = (index) => {
  if (weather.value.length > 1) weather.value.splice(index, 1)
}

const boolFromApi = (value) => (typeof value === 'boolean' ? value : value === 1 || value === '1')
const boolToApi = (value) => (value ? 1 : 0)

const api = async (url, options = {}) => {
  const opt = { ...options }
  opt.headers = { ...(opt.headers || {}) }
  if (opt.method && opt.method !== 'GET' && csrfToken.value) opt.headers['X-CSRF-Token'] = csrfToken.value
  try {
    const response = await fetch(url, opt)
    if (response.status === 401) {
      window.location.href = `/login?next=${encodeURIComponent(window.location.pathname || '/')}`
      return {}
    }
    if (!response.ok) return {}
    return await response.json()
  } catch (err) {
    console.warn(err)
    return {}
  }
}

const fetchCsrf = async () => {
  try {
    const response = await fetch('/api/csrf')
    if (response.ok) {
      const data = await response.json()
      csrfToken.value = data.token || ''
    }
  } catch (err) {
    console.warn(err)
  }
}

const fetchLogs = async (limit = 100) => {
  if (logsLoading.value) return
  logsLoading.value = true
  try {
    const response = await fetch(`/api/logs?limit=${limit}`)
    if (response.ok) {
      const data = await response.json()
      logs.value = data.logs || []
    }
  } catch (err) {
    console.warn(err)
  } finally {
    logsLoading.value = false
    resetCountdown()
  }
}

const getLogLevel = (log) => {
  const low = log.toLowerCase()
  if (low.includes('error') || low.includes('fail') || low.includes('crash')) return 'error'
  if (low.includes('warn')) return 'warning'
  if (low.includes('info') || low.includes('connected')) return 'info'
  return 'debug'
}

const getLogLevelText = (log) => `[${getLogLevel(log).toUpperCase()}]`

const formatLogMessage = (log) =>
  log.replace(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} /, '').replace(/^\d{2}:\d{2}:\d{2} /, '')

const fetchPresets = async () => {
  try {
    const data = await api('/api/presets')
    presets.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.warn(err)
    presets.value = []
  }
}

const savePreset = async () => {
  const presetName = window.prompt(t.value.presets.savePrompt)
  if (!presetName || !presetName.trim()) return

  const payload = {
    name: presetName,
    track: session.track,
    trackVariant: session.trackVariant,
    cars: session.cars.map((car) => ({
      id: car.model,
      restrictor: car.restrictor,
      ballast: car.ballast,
      skin: car.skin
    })),
    weather: weather.value,
    tyreWear: session.tyreWear,
    damage: session.damage,
    fuelConsumption: session.fuelConsumption,
    sunAngle: session.sunAngle,
    practiceDuration: session.practiceDuration,
    qualifyingDuration: session.qualifyingDuration,
    raceLaps: session.raceLaps,
    pickupMode: session.pickupMode,
    loopMode: session.loopMode,
    allowedTyresOut: session.allowedTyresOut,
    legalTyres: session.legalTyres,
    absAllowed: boolToApi(session.absAllowed),
    tcAllowed: boolToApi(session.tcAllowed),
    stabilityAllowed: boolToApi(session.stabilityAllowed),
    autoclutchAllowed: boolToApi(session.autoclutchAllowed),
    tyreBlanketsAllowed: boolToApi(session.tyreBlanketsAllowed),
    forceVirtualMirror: boolToApi(session.forceVirtualMirror),
    registerToLobby: boolToApi(session.registerToLobby),
    maxClients: session.maxClients
  }

  try {
    const response = await api(`/api/presets/save?name=${encodeURIComponent(presetName.trim())}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    })
    if (response && response.success) {
      success(t.value.presets.saveSuccess)
      await fetchPresets()
    } else {
      error(response?.message || t.value.presets.saveError)
    }
  } catch (err) {
    error(t.value.presets.saveError)
  }
}

const applyPreset = async (preset) => {
  if (!preset?.name) return
  try {
    const response = await api(`/api/presets/load?name=${encodeURIComponent(preset.name)}`)
    if (response && response.success) {
      success(t.value.presets.applySuccess)
      await fetchAll()
    } else {
      error(response?.message || t.value.presets.applyError)
    }
  } catch (err) {
    error(t.value.presets.applyError)
  }
}

const deletePreset = async (preset) => {
  if (!preset?.name) return
  if (!window.confirm(t.value.presets.deleteConfirm)) return

  try {
    const response = await api(`/api/presets/delete?name=${encodeURIComponent(preset.name)}`, {
      method: 'DELETE'
    })
    if (response && response.success) {
      success(t.value.presets.deleteSuccess)
      await fetchPresets()
    } else {
      error(response?.message || t.value.presets.deleteError)
    }
  } catch (err) {
    error(t.value.presets.deleteError)
  }
}

const startAutoRefresh = () => {
  stopAutoRefresh()
  if (!logsAutoRefresh.value) return
  logsRefreshTimer.value = setInterval(() => {
    if (tab.value === 'logs' && logsAutoRefresh.value) fetchLogs()
  }, 10000)
  resetCountdown()
  logsCountdownInterval.value = setInterval(() => {
    if (tab.value === 'logs' && logsAutoRefresh.value) {
      logsRefreshCountdown.value -= 1
      if (logsRefreshCountdown.value <= 0) logsRefreshCountdown.value = 10
    }
  }, 1000)
}

const stopAutoRefresh = () => {
  if (logsRefreshTimer.value) clearInterval(logsRefreshTimer.value)
  if (logsCountdownInterval.value) clearInterval(logsCountdownInterval.value)
  logsRefreshTimer.value = null
  logsCountdownInterval.value = null
}

const resetCountdown = () => {
  logsRefreshCountdown.value = 10
}

const toggleAutoRefresh = () => {
  logsAutoRefresh.value = !logsAutoRefresh.value
  if (logsAutoRefresh.value) {
    startAutoRefresh()
    if (tab.value === 'logs') fetchLogs()
  } else {
    stopAutoRefresh()
  }
}

const clearLogs = () => {
  logs.value = []
  info('Логи очищены')
}

const normalizeSessionCars = (carData) => {
  if (!Array.isArray(carData)) return []
  return carData
    .map((item) => {
      if (typeof item === 'string')
        return {
          model: item,
          restrictor: 0,
          ballast: 0,
          skin: ''
        }
      if (item && typeof item === 'object')
        return {
          model: item.model || item.id || '',
          restrictor: item.restrictor ?? 0,
          ballast: item.ballast ?? 0,
          skin: item.skin || ''
        }
      return {
        model: '',
        restrictor: 0,
        ballast: 0,
        skin: ''
      }
    })
    .filter((car) => car.model)
}

const updateTrackVariants = () => {
  const track = tracks.value.find((item) => item.id === session.track)
  session.trackVariants = track?.layouts || []
  if (!session.trackVariants.includes(session.trackVariant)) {
    session.trackVariant = session.trackVariants[0] || ''
  }
}

const fetchAll = async () => {
  loading.value = true
  try {
    const [serverInfo, sessionData, carsData, tracksData, weatherData] = await Promise.all([
      api('/api/info'),
      api('/api/session'),
      api('/api/cars'),
      api('/api/tracks'),
      api('/api/weather')
    ])

    Object.assign(server, {
      status: serverInfo?.status || 'offline',
      clients: serverInfo?.clients || 0,
      maxclients: serverInfo?.maxclients || 0,
      track: serverInfo?.track || ''
    })

    if (sessionData) {
      session.name = sessionData.name || ''
      session.password = sessionData.password || ''
      session.adminPassword = sessionData.adminPassword || ''
      session.udpPort = sessionData.udpPort ?? 9600
      session.tcpPort = sessionData.tcpPort ?? 9600
      session.httpPort = sessionData.httpPort ?? 8081
      if (Array.isArray(sessionData.cars)) {
        session.cars = sessionData.cars.map((car) => ({
          model: car.id || car.model || '',
          restrictor: Number(car.restrictor) ?? 0,
          ballast: Number(car.ballast) ?? 0,
          skin: car.skin || ''
        }))
      } else if (sessionData.cars) {
        session.cars = normalizeSessionCars(sessionData.cars)
      } else {
        session.cars = []
      }
      session.track = sessionData.track || ''
      session.trackVariant = sessionData.trackVariant || ''
      session.trackVariants = sessionData.trackVariants || []
      session.tyreWear = sessionData.tyreWear ?? 1
      session.damage = sessionData.damage ?? 1
      session.fuelConsumption = sessionData.fuelConsumption ?? 1
      session.sunAngle = sessionData.sunAngle ?? 48
      session.practiceDuration = sessionData.practiceDuration ?? 0
      session.qualifyingDuration = sessionData.qualifyingDuration ?? 0
      session.raceLaps = sessionData.raceLaps ?? 0
      session.pickupMode = sessionData.pickupMode ?? 1
      session.loopMode = sessionData.loopMode ?? 1
      session.allowedTyresOut = sessionData.allowedTyresOut ?? 2
      session.legalTyres = sessionData.legalTyres ?? 'SV'
      session.absAllowed = boolFromApi(sessionData.absAllowed)
      session.tcAllowed = boolFromApi(sessionData.tcAllowed)
      session.stabilityAllowed = boolFromApi(sessionData.stabilityAllowed)
      session.autoclutchAllowed = boolFromApi(sessionData.autoclutchAllowed)
      session.tyreBlanketsAllowed = boolFromApi(sessionData.tyreBlanketsAllowed)
      session.forceVirtualMirror = boolFromApi(sessionData.forceVirtualMirror)
      session.registerToLobby = boolFromApi(sessionData.registerToLobby)
      session.maxClients = sessionData.maxClients ?? 0
      if (sessionData.weather && Array.isArray(sessionData.weather) && sessionData.weather.length) {
        weather.value = sessionData.weather
      }
    }

    cars.value = carsData || []
    tracks.value = tracksData || []
    weatherList.value = weatherData || []
    updateTrackVariants()
  } finally {
    loading.value = false
  }
}

const start = async () => {
  await api('/api/server/start', { method: 'POST' })
  await fetchAll()
  success('Сервер запущен')
}

const stop = async () => {
  await api('/api/server/stop', { method: 'POST' })
  await fetchAll()
  success('Сервер остановлен')
}

const addCar = () => {
  if (cars.value.length)
    session.cars.push({
      model: cars.value[0].id,
      restrictor: 0,
      ballast: 0,
      skin: ''
    })
}

const removeCar = (index) => {
  session.cars.splice(index, 1)
}

const saveSession = async () => {
  saving.value = true
  const payload = {
    name: session.name,
    password: session.password,
    adminPassword: session.adminPassword,
    udpPort: session.udpPort,
    tcpPort: session.tcpPort,
    httpPort: session.httpPort,
    cars: session.cars.map((car) => ({
      id: car.model,
      restrictor: car.restrictor,
      ballast: car.ballast,
      skin: car.skin
    })),
    track: session.track,
    trackVariant: session.trackVariant,
    tyreWear: session.tyreWear,
    damage: session.damage,
    fuelConsumption: session.fuelConsumption,
    sunAngle: session.sunAngle,
    practiceDuration: session.practiceDuration,
    qualifyingDuration: session.qualifyingDuration,
    raceLaps: session.raceLaps,
    pickupMode: session.pickupMode,
    loopMode: session.loopMode,
    allowedTyresOut: session.allowedTyresOut,
    legalTyres: session.legalTyres,
    absAllowed: boolToApi(session.absAllowed),
    tcAllowed: boolToApi(session.tcAllowed),
    stabilityAllowed: boolToApi(session.stabilityAllowed),
    autoclutchAllowed: boolToApi(session.autoclutchAllowed),
    tyreBlanketsAllowed: boolToApi(session.tyreBlanketsAllowed),
    forceVirtualMirror: boolToApi(session.forceVirtualMirror),
    registerToLobby: boolToApi(session.registerToLobby),
    weather: weather.value,
    maxClients: session.maxClients
  }
  try {
    const response = await api('/api/session', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    if (response && response.success) {
      success(t.value.session.saveSuccess)
    } else {
      error(response?.message || t.value.session.saveError)
    }
    await fetchAll()
  } catch (err) {
    error(t.value.session.saveError)
  } finally {
    saving.value = false
  }
}

const logout = async () => {
  await fetch('/logout', {
    method: 'POST',
    headers: csrfToken.value ? { 'X-CSRF-Token': csrfToken.value } : {}
  })
  window.location.href = '/login'
}

const refreshIFrame = () => {
  const iframe = document.getElementById('players-entry-iframe')
  if (iframe) iframe.src = iframe.src
}

const handleFolder = async (event) => {
  const files = event.target.files
  if (!files?.length) return
  const zip = new JSZip()
  progress.value = 0
  uploadProgress.value = 0
  uploading.value = false

  for (const file of files) {
    zip.file(file.webkitRelativePath, file)
  }

  zipBlob.value = await zip.generateAsync({ type: 'blob' }, (metadata) => {
    progress.value = Math.round(metadata.percent)
  })
}

const uploadZip = async () => {
  if (!zipBlob.value || uploading.value) return

  uploading.value = true
  uploadProgress.value = 0

  const formData = new FormData()
  formData.append('mod', zipBlob.value, 'mod.zip')

  let uploadSuccess = false
  try {
    await new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', '/upload')
      if (csrfToken.value) xhr.setRequestHeader('X-CSRF-Token', csrfToken.value)

      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          uploadProgress.value = Math.round((event.loaded / event.total) * 100)
        }
      }

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(xhr.response)
        } else {
          reject(new Error(`Upload failed (${xhr.status})`))
        }
      }

      xhr.onerror = () => reject(new Error('Network error'))
      xhr.onabort = () => reject(new Error('Upload aborted'))
      xhr.send(formData)
    })

    uploadSuccess = true
    success('Мод загружен 🚀')
  } catch (err) {
    error('Ошибка загрузки мода')
  } finally {
    uploading.value = false
    if (uploadSuccess) {
      zipBlob.value = null
      progress.value = 0
      setTimeout(() => {
        uploadProgress.value = 0
      }, 500)
    }
  }
}

watch(tab, (newTab) => {
  if (newTab === 'logs') {
    fetchLogs()
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
  if (newTab === 'presets') {
    fetchPresets()
  }
})

watch(
  () => session.track,
  () => updateTrackVariants()
)

onMounted(() => {
  fetchCsrf()
  fetchAll()
})

onBeforeUnmount(() => {
  stopAutoRefresh()
})
</script>
