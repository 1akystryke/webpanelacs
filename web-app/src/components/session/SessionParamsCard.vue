<template>
  <div class="card">
    <div class="card-title"><span>⚙️</span> {{ t.session.sessionParams }}</div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px;">
      <div>
        <div class="label">{{ t.session.tyreWear }}</div>
        <input v-model.number="session.tyreWear" type="number" min="0" step="0.1" class="input" />
      </div>
      <div>
        <div class="label">{{ t.session.damage }}</div>
        <input v-model.number="session.damage" type="number" min="0" step="0.1" class="input" />
      </div>
      <div>
        <div class="label">{{ t.session.fuelConsumption }}</div>
        <input v-model.number="session.fuelConsumption" type="number" min="0" step="0.1" class="input" />
      </div>
      <div>
        <div class="label">SUN_ANGLE</div>
        <input v-model.number="session.sunAngle" type="number" class="input" />
      </div>
    </div>
    <div style="margin-bottom: 24px;">
      <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #64748b;">
        {{ t.session.duration }}
      </h4>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
        <div>
          <div class="label">{{ t.session.practice }}</div>
          <input v-model.number="session.practiceDuration" type="number" min="0" class="input" />
        </div>
        <div>
          <div class="label">{{ t.session.qualifying }}</div>
          <input v-model.number="session.qualifyingDuration" type="number" min="0" class="input" />
        </div>
        <div>
          <div class="label">{{ t.session.race }}</div>
          <input v-model.number="session.raceLaps" type="number" min="0" class="input" />
        </div>
      </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">
      <div>
        <div class="label">PICKUP_MODE</div>
        <select v-model.number="session.pickupMode" class="input">
          <option :value="0">{{ t.session.disabled }}</option>
          <option :value="1">{{ t.session.enabled }}</option>
        </select>
      </div>
      <div>
        <div class="label">LOOP_MODE</div>
        <select v-model.number="session.loopMode" class="input">
          <option :value="0">{{ t.session.disabled }}</option>
          <option :value="1">{{ t.session.enabled }}</option>
        </select>
      </div>
      <div>
        <div class="label">ALLOWED_TYRES_OUT</div>
        <input v-model.number="session.allowedTyresOut" type="number" class="input" />
      </div>
      <div>
        <div class="label">LEGAL_TYRES</div>
        <input v-model="session.legalTyres" type="text" class="input" />
      </div>
    </div>
    <div style="margin-top: 24px;">
      <h4 style="font-size: 14px; font-weight: 600; margin-bottom: 12px; color: #64748b;">
        {{ t.session.assists }}
      </h4>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
        <div class="checkbox-group">
          <input id="abs" v-model="session.absAllowed" type="checkbox" />
          <label for="abs">ABS_ALLOWED</label>
        </div>
        <div class="checkbox-group">
          <input id="tc" v-model="session.tcAllowed" type="checkbox" />
          <label for="tc">TC_ALLOWED</label>
        </div>
        <div class="checkbox-group">
          <input id="stability" v-model="session.stabilityAllowed" type="checkbox" />
          <label for="stability">STABILITY_ALLOWED</label>
        </div>
        <div class="checkbox-group">
          <input id="autoclutch" v-model="session.autoclutchAllowed" type="checkbox" />
          <label for="autoclutch">AUTOCLUTCH_ALLOWED</label>
        </div>
        <div class="checkbox-group">
          <input id="blankets" v-model="session.tyreBlanketsAllowed" type="checkbox" />
          <label for="blankets">TYRE_BLANKETS_ALLOWED</label>
        </div>
        <div class="checkbox-group">
          <input id="mirror" v-model="session.forceVirtualMirror" type="checkbox" />
          <label for="mirror">FORCE_VIRTUAL_MIRROR</label>
        </div>
        <div class="checkbox-group">
          <input id="lobby" v-model="session.registerToLobby" type="checkbox" />
          <label for="lobby">REGISTER_TO_LOBBY</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  session: {
    type: Object,
    required: true
  },
  t: {
    type: Object,
    required: true
  }
})
</script>
