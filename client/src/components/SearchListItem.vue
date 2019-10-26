<template>
  <div class="box">
    <div class="columns">
      <div class="column is-one-fifth-tablet">
        <p class="image is-square">
          <img src="https://bulma.io/images/placeholders/128x128.png">
        </p>
      </div>
      <div class="column">
        <div class="content">
            <div class="columns is-gapless is-multiline">
              <div class="column is-half">
                <strong>Really Scary Place</strong> <small>Admin</small>
              </div>
              <div class="column is-half">
                <b-rate class="is-pulled-right"
                  icon-pack="fas"
                  @change="success"
                  custom-text=""></b-rate>
              </div>
              <div class="column">
                <small>Walmart, Austin, TX</small>
              </div>
            </div>
                          This place is really spooky and scary and I don't like it cause
            it's spooky and scary and there are really ugly things that pop
            out of nowhere and scare me and spook me. i'm pretty sure this
            place is haunted and i don't want to go bck nd you shouldn't
            either.
        </div>
        <!-- <nav class="level is-mobile">
          <div class="level-left">
            <a class="level-item">
              <span class="icon is-small"><i class="fas fa-reply"></i></span>
            </a>
            <a class="level-item">
              <span class="icon is-small"><i class="fas fa-retweet"></i></span>
            </a>
            <a class="level-item">
              <span class="icon is-small"><i class="fas fa-heart"></i></span>
            </a>
          </div>
        </nav> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {

};
</script>

<style>

</style>
