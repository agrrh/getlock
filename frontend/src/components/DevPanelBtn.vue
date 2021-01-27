<template>
  <v-list-item>
    <v-tooltip right>
      <template v-slot:activator="{ on, attrs }">
        <v-btn 
          icon
          v-bind="attrs"
          v-on="on"
          @click="btnMethod"
        >
          <v-icon>{{ iconMdi }}</v-icon>
        </v-btn>
      </template>
      <span>
        <slot></slot>
      </span>
    </v-tooltip>
  </v-list-item>
</template>

<script>
export default {
  props: {
    btnMethod: Function,
    iconMdi: String
  }
}
</script>