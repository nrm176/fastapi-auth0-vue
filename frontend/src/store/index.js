import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

const messageModule = {
  strict: process.env.NODE_ENV !== 'production',
  namespaced: true,
  state: {
    error: '',
    warnings: [],
    info: ''
  },
  getters: {
    error: state => state.error,
    warnings: state => state.warnings,
    info: state => state.info
  },
  mutations: {
    set (state, payload) {
      if (payload.error) {
        state.error = payload.error
      }
      if (payload.warnings) {
        state.warnings = payload.warnings
      }
      if (payload.info) {
        state.info = payload.info
      }
    },
    clear (state) {
      state.error = ''
      state.warnings = []
      state.info = ''
    }
  },
  actions: {
    /**
     * error
     */
    setErrorMessage (context, payload) {
      context.commit('clear')
      context.commit('set', { error: payload.message })
    },
    /**
     * alert
     */
    setWarningMessages (context, payload) {
      context.commit('clear')
      context.commit('set', { warnings: payload.messages })
    },
    /**
     * info
     */
    setInfoMessage (context, payload) {
      context.commit('clear')
      context.commit('set', { info: payload.message })
    },
    /**
     * 全メッセージ削除
     */
    clearMessages (context) {
      context.commit('clear')
    }
  }
}

export default new Vuex.Store({
  modules: {
    message: messageModule
  },
  plugins: [createPersistedState({
    key: 'fastapi-auth0-vue',
    storage: window.sessionStorage
  })]
})
