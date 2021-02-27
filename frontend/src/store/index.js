import Vue from 'vue'
import Vuex from 'vuex'
import Axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    locks: '',
    sessionId: '',
    devPanelVisible: false,
    listIsLoading: false,
  },
  mutations: {
    updateLocks(state, payload) {
      state.locks = payload;
    },
    updateSessionId(state, payload) {
      state.sessionId = payload;
    },
    toggleDevPanel(state) {
      state.devPanelVisible = !state.devPanelVisible;
    },
    setLoading(state, payload) {
      state.listIsLoading = payload;
    }
  },
  getters: {
    getLocks(state, commit) {
      return {
        get() {
          return state.locks;
        },
        set(value) {
          commit('updateLocks', value);
        }
      }
    }
  },
  actions: {
    fetchData({commit}, setLoader) {
      setLoader ? commit('setLoading', true) : '';
      Axios.get('https://getlock.tech/v2/~test',
        {
          headers: {
            'X-Getlock-Auth': 'test'
          }
        }
      )
      .then(response => {
        console.log(response);
        this.commit('updateLocks', response.data.namespace.locks);
        setLoader ? commit('setLoading', false) : '';
      })
      .catch(err => {
        console.log(err)
        setLoader ? commit('setLoading', false) : '';
      })
    }
  },
})
