<template>
    <div>
        <div style="margin-bottom: 24px">
            <div class="section-title">{{ t.content.title }}</div>
            <p style="color: #64748b">{{ t.content.hint }}</p>
        </div>

        <div class="card" style="margin-bottom: 24px">
            <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap; width: 100%">
                <input type="file" webkitdirectory @change="handleFolder" />
                <button class="btn btn-primary" @click="uploadZip" :disabled="!zipReady">Загрузить мод</button>
            </div>

            <div class="progress-area" v-if="progress > 0 || uploadProgress > 0 || uploading" style="margin-top: 18px; margin-bottom: 18px">
                <div class="progress-block" v-if="progress > 0">
                    <div class="progress-label">Архивация: {{ progress }}%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: `${progress}%` }" />
                    </div>
                </div>

                <div class="progress-block" v-if="uploadProgress > 0 || uploading">
                    <div class="progress-label">Загрузка: {{ uploading ? uploadProgress : uploadProgress }}%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: `${uploadProgress}%` }" />
                    </div>
                </div>
            </div>

            <div class="grid">
                <div class="card">
                    <div class="card-title">🏎️ {{ t.content.cars }}</div>

                    <input v-model="contentSearch.cars" type="text" class="input" :placeholder="t.content.searchCars" style="margin-bottom: 16px" />

                    <div class="content-list">
                        <div v-for="car in filteredCars" :key="car.id" class="content-item">
                            <div>
                                <div style="font-weight: 600">{{ car.name }}</div>
                                <div style="font-size: 12px; color: #64748b">{{ car.id }}</div>
                            </div>

                            <span class="badge" :class="car.is_mod ? 'mod' : 'vanilla'">
                                {{ car.is_mod ? t.content.mod : t.content.vanilla }}
                            </span>
                        </div>

                        <div v-if="filteredCars.length === 0" class="empty-state">
                            {{ t.content.noCars }}
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-title">🏁 {{ t.content.tracks }}</div>

                    <input v-model="contentSearch.tracks" type="text" class="input" :placeholder="t.content.searchTracks" style="margin-bottom: 16px" />

                    <div class="content-list">
                        <div v-for="track in filteredTracks" :key="track.id" class="content-item">
                            <div>
                                <div style="font-weight: 600">{{ track.name }}</div>
                                <div style="font-size: 12px; color: #64748b">{{ track.id }}</div>
                            </div>

                            <span class="badge" :class="track.is_mod ? 'mod' : 'vanilla'">
                                {{ track.is_mod ? t.content.mod : t.content.vanilla }}
                            </span>
                        </div>

                        <div v-if="filteredTracks.length === 0" class="empty-state">
                            {{ t.content.noTracks }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
    t: {
        type: Object,
        required: true,
    },
    cars: {
        type: Array,
        required: true,
    },
    tracks: {
        type: Array,
        required: true,
    },
    contentSearch: {
        type: Object,
        required: true,
    },
    handleFolder: {
        type: Function,
        required: true,
    },
    uploadZip: {
        type: Function,
        required: true,
    },
    progress: {
        type: Number,
        required: true,
    },
    uploadProgress: {
        type: Number,
        required: true,
    },
    uploading: {
        type: Boolean,
        required: true,
    },
    zipReady: {
        type: Boolean,
        required: true,
    },
});

const filteredCars = computed(() => props.cars.filter((car) => car.id.toLowerCase().includes(props.contentSearch.cars.toLowerCase())));

const filteredTracks = computed(() => props.tracks.filter((track) => track.id.toLowerCase().includes(props.contentSearch.tracks.toLowerCase())));
</script>
