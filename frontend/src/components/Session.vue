<template>
  <v-col>
    <v-slide-x-transition 
      appear 
      mode="out-in"
    >
      <v-card class="py-4 px-6">
        <div>
          <span class="font-weight-bold">
            Session name:
          </span> 
          {{ name }}
        </div>
        <div>
          <span class="font-weight-bold">
            Session ID:
          </span> 
          {{ uuid }}
        </div>
        <p 
          :style="status.active ? 'color: #607d8b' : 'color: #009688'" 
          class="font-weight-bold mb-3"
        >
          {{ status.message }}
        </p>
        <v-progress-linear
          color="#3f51b5"
          :buffer-value="progressValue"
          stream
        ></v-progress-linear>
      </v-card>
    </v-slide-x-transition>
  </v-col>
</template>

<script>

export default {
  props: {
    lock: Object
  },
  name: 'Session',
  data: function() {
    return {
      name: this.lock.id,
      uuid: this.lock.uuid,
      age: this.lock.age,
      ttl: this.lock.ttl,
      status: {
        message: 'In progress',
        active: true
      }
    }
  },
  computed: {
    timeLeft() {
      return this.ttl - this.age
    },
    progressValue() {
      return this.age / this.ttl * 100
    }
  },
  methods: {
    countDownTimer() {
      if (this.timeLeft > 0) {
        setTimeout(() => {
          this.age += 1
          this.countDownTimer()
        }, 1000)
      }
    }
  },
  watch: {
    progressValue: {
      handler(val) {
        if (val === 100) {
          this.status.message = 'Done!';
          this.status.active = false;
        }
      }
    }
  },
  created() {
    this.countDownTimer()
  }
}
</script>