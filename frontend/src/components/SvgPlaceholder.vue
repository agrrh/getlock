<template>
  <div class="lock-glitch">
    <img src="../assets/padlock.svg">
    <img src="../assets/padlock2.svg">
    <img src="../assets/padlock.svg">
  </div>
</template>

<script>
export default {
  
}
</script>

<style lang="scss" scoped>
  @mixin imgGlitch($name, $intensity, $width, $height, $top, $left) {
  
  $steps: $intensity;
  
  // Ensure the @keyframes are generated at the root level
  @at-root {
    // We need two different ones
    @for $i from 1 through 2 {
      @keyframes #{$name}-anim-#{$i} {
        @for $i from 5 through $steps {
          #{percentage($i*(1/$steps))} {
            clip: rect(
              random($height)+px,
              $width+px,
              random($height)+px,
              0
            );
          }
        }
      }
    }
  }
  
  > img {
    position: absolute;
    top: $top+px;
    left: $left+px;
  }
  > img:nth-child(2),
  > img:nth-child(3){
    clip: rect(0, 0, 0, 0); 
  }
  > img:nth-child(2) {
    left: ($left + 2) + px;
    animation: #{$name}-anim-1 2s infinite linear alternate-reverse;
  }
  > img:nth-child(3) {
    left: ($left - 2) + px;
    animation: #{$name}-anim-2 3s infinite linear alternate-reverse;
  }
}

.lock-glitch {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto;
  @include imgGlitch("example-three", 30, 100, 100, 0, 0);
}
</style>