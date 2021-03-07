<template>
  <v-fade-transition appear>
    <div>
      <v-tabs 
        v-model="tab"
        :centered="$store.state.locks.length ? true : false"
        color="secondary"
        class="apiguide-tabs"
      >
        <v-tab>Curl</v-tab>
        <v-tab>JS</v-tab>
      </v-tabs>
      <v-tabs-items 
        v-model="tab"
        class="apiguide-tab-content"  
      >
        <!-- CURL -->
        <v-tab-item>
          <p class="apiguide-caption">
            Creating namespace:
          </p>
          <pre class="apiguide-codeblock">
            curl -X PUT -d "https://getlock.tech/v2/${YOUR_NAMESPACE}"
          </pre>
          <p class="apiguide-caption">
            Adding session:
          </p>
          <pre class="apiguide-codeblock">
            curl -X PUT -d ttl=3600 "https://getlock.tech/v2/${YOUR_NAMESPACE}/${SESSION_NAME}"
          </pre>
        </v-tab-item>
        <!-- JS -->
        <v-tab-item>
          <p class="apiguide-caption">
            Creating namespace:
          </p>
          <pre class="apiguide-codeblock">
            curl -X PUT -d "https://getlock.tech/v2/${YOUR_NAMESPACE}"
          </pre>
          <p class="apiguide-caption">
            Adding session using Axios
          </p>
          <pre class="apiguide-codeblock">
            Axios.put(`https://getlock.tech/v2/${YOUR_NAMESPACE}/${SESSION_NAME}`,
              {},
              {
                headers: {
                  'X-Getlock-Auth': YOUR_NAMESPACE
                }
              })
            })
            .then(response => {
              console.log(response);
            })
            .catch(err => {
              console.log(err)
            })
          </pre>
        </v-tab-item>
      </v-tabs-items>  
    </div>
  </v-fade-transition>
</template>

<script>
  export default {
    data () {
      return {
        tab: null,
      }
    },
  }
</script>

<style>

.apiguide-caption {
  margin: 16px 0 8px;
  font-weight: 600;
}

.apiguide-tabs {
  margin-top: 12px;
}

.v-slide-group__wrapper {
  padding: 0 16px;
}

.apiguide-codeblock {
  white-space: pre-line;
  font-size: 14px;
  padding: 12px;
  background-color: #949494;
  color: #fff;
  overflow: auto;
  word-break: break-all;
}

.apiguide-tab-content {
  padding: 16px;
}

</style>