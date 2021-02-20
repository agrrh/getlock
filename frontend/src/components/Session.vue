<template>
  <v-col>
    <v-slide-x-transition 
      appear 
      mode="out-in"
    >
      <v-card 
        class="py-4 px-6"
      >
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
        <div>
          <span class="font-weight-bold">
            Remaining time:
          </span> 
          {{ timeLeft > 0 ? ttlToRealTime : '-' }}
        </div>
        <p 
          :style="status.active ? 'color: #607d8b' : 'color: #009688'" 
          class="font-weight-bold mb-3"
        >
          {{ status.message }}
        </p>
        <v-progress-linear
          color="info"
          :buffer-value="progressValue"
          stream
        ></v-progress-linear>
        <div 
          class="inactive-time"
          v-if="!status.active"
        >
          Ended {{ timeleftToMins }} minutes ago
        </div>
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
    },
    ttlToRealTime() {
      var sec_num = parseInt(this.timeLeft, 10);
      var hours   = Math.floor(sec_num / 3600);
      var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
      var seconds = sec_num - (hours * 3600) - (minutes * 60);

      if (hours   < 10) {hours   = "0"+hours;}
      if (minutes < 10) {minutes = "0"+minutes;}
      if (seconds < 10) {seconds = "0"+seconds;}
      return hours+':'+minutes+':'+seconds;
    },
    timeleftToMins() {
      const mins = Math.floor(this.timeLeft / 60)
      return Math.abs(mins);
    },
  },
  methods: {
    countDownTimer() {
      setTimeout(() => {
        this.age += 1
        this.countDownTimer()
      }, 1000)
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
    this.countDownTimer();
    if (this.lock.expired) {
      this.status.message = 'Done!';
      this.status.active = false;
    }
  }
}
</script>

<style scoped>
  .expired {
    opacity: 0.7;
  }

  .inactive-time {
    position: absolute;
    top: 16px;
    right: 24px;
    display: flex;
    align-items: center;
  }

  .inactive-time p {
    margin-bottom: 0;
    margin-left: 8px;
  }
</style>