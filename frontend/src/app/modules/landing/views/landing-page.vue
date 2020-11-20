<template>
  <div class="box">
    <!-- Navigation -->
    <nav class="app-navbar" :style="navbarStyle">
      <div class="container">
          <router-link
          class=""
          to="/"
        >
          <img src="@/assets/img/findex_logo_white_dash.png" height="31"/>
        </router-link>
        <!-- <a class="navbar-brand" href="#">Start Bootstrap</a> -->
        <button class="btn alignleft" @click="onLoginClick" v-if="!authenticated">SIGN IN</button>
        <button class="btn alignleft" @click="onPortalClick" v-else>PORTAL</button>
      </div>
    </nav>
    <div class="content row">
        <!-- <p class="contentTile">The first AI powered solution for Education!</p> -->
    </div>

    <!-- Masthead -->
    <!-- <header class="masthead text-white text-center">
      <div class="overlay"></div>
      <div class="container">
        <div class="row">
          <div class="col-xl-9 mx-auto">
            <h1 class="mb-5">
              The first AI powered solution for Education!
            </h1>
          </div>
          <div class="col-md-10 col-lg-8 col-xl-7 mx-auto">
            <p class="mb-4 d-none d-md-block">
              <strong>The most comprehensive tool for the education industry.</strong>
            </p>
          </div>
        </div>
      </div>
    </header> -->

    <!-- Icons Grid -->
    <!-- <section class="features-icons bg-light text-center">
      <div class="container">
        <div class="row">
          <div class="col-lg-4">
            <div class="features-icons-item mx-auto mb-5 mb-lg-0 mb-lg-3">
              <div class="features-icons-icon d-flex">
                <i class="icon-screen-desktop m-auto text-primary"></i>
              </div>
              <h3>Optimise your operations</h3>
              <p class="lead mb-0">
                We use Artificial Intelligence to optimise your school's operations!
              </p>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="features-icons-item mx-auto mb-5 mb-lg-0 mb-lg-3">
              <div class="features-icons-icon d-flex">
                <i class="icon-layers m-auto text-primary"></i>
              </div>
              <h3>Predict sustainability</h3>
              <p class="lead mb-0">
                We use thousands of external data points to predict future risks like demographic shifting!
              </p>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="features-icons-item mx-auto mb-0 mb-lg-3">
              <div class="features-icons-icon d-flex">
                <i class="icon-check m-auto text-primary"></i>
              </div>
              <h3>Easy to Use</h3>
              <p class="lead mb-0">
                Ready to use and customizable for your purpose by integrating your internal data to our dataset!
              </p>
            </div>
          </div>
        </div>
      </div>
    </section> -->

    <!-- Image Showcases -->
    <!-- <section class="showcase">
      <div class="container-fluid p-0">
        <div class="row no-gutters">
          <div
            class="col-lg-6 order-lg-2 text-white showcase-img"
            style="background-image: url('img/bg-showcase-1.jpg');"
          ></div>
          <div class="col-lg-6 order-lg-1 my-auto showcase-text">
            <h2>Fully Responsive Design</h2>
            <p class="lead mb-0">
              When you use a theme created by Start Bootstrap, you know that the
              theme will look great on any device, whether it's a phone, tablet,
              or desktop the page will behave responsively!
            </p>
          </div>
        </div>
        <div class="row no-gutters">
          <div
            class="col-lg-6 text-white showcase-img"
            style="background-image: url('img/bg-showcase-2.jpg');"
          ></div>
          <div class="col-lg-6 my-auto showcase-text">
            <h2>Updated For Bootstrap 4</h2>
            <p class="lead mb-0">
              Newly improved, and full of great utility classes, Bootstrap 4 is
              leading the way in mobile responsive web development! All of the
              themes on Start Bootstrap are now using Bootstrap 4!
            </p>
          </div>
        </div>
        <div class="row no-gutters">
          <div
            class="col-lg-6 order-lg-2 text-white showcase-img"
            style="background-image: url('img/bg-showcase-3.jpg');"
          ></div>
          <div class="col-lg-6 order-lg-1 my-auto showcase-text">
            <h2>Easy to Use &amp; Customize</h2>
            <p class="lead mb-0">
              Landing Page is just HTML and CSS with a splash of SCSS for users
              who demand some deeper customization options. Out of the box, just
              add your content and images, and your new landing page will be
              ready to go!
            </p>
          </div>
        </div>
      </div>
    </section> -->

    <!-- Testimonials -->
    <!-- <section class="testimonials text-center bg-light">
      <div class="container">
        <h2 class="mb-5">Our Team...</h2>
        <div class="row">
          <div class="col-lg-4">
            <div class="testimonial-item mx-auto mb-5 mb-lg-0">
              <img class="img-fluid rounded-circle mb-3" src="../../../../../static/landing/base_images/BH.jpg" alt="">
              <h5>Behrang Z.</h5>
              <p class="font-weight-light mb-0">Lead Data Scientist</p>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="testimonial-item mx-auto mb-5 mb-lg-0">
              <img class="img-fluid rounded-circle mb-3" src="../../../../../static/landing/base_images/FR.jpg" alt="">
              <h5>Fred G.</h5>
              <p class="font-weight-light mb-0">Senior Data Scientist</p>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="testimonial-item mx-auto mb-5 mb-lg-0">
              <img class="img-fluid rounded-circle mb-3" src="../../../../../static/landing/base_images/NH.jpg" alt="">
              <h5>Nathan C.</h5>
              <p class="font-weight-light mb-0">Data Scientist</p>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="testimonial-item mx-auto mb-5 mb-lg-0">
              <img class="img-fluid rounded-circle mb-3" src="../../../../../static/landing/base_images/NH.jpg" alt="">
              <h5>Thao N.</h5>
              <p class="font-weight-light mb-0">"Data Scientist"</p>
            </div>
          </div>
        </div>
      </div>
    </section> -->

    <!-- Call to Action -->
    <!-- <section class="call-to-action text-white text-center">
      <div class="overlay"></div>
      <div class="container">
        <div class="row">
          <div class="col-xl-9 mx-auto">
            <h2 class="mb-4">Ready to get started? Sign up now!</h2>
          </div>
          <div class="col-md-10 col-lg-8 col-xl-7 mx-auto">
            <form>
              <div class="form-row">
                <div class="col-12 col-md-9 mb-2 mb-md-0">
                  <input
                    type="email"
                    class="form-control form-control-lg"
                    placeholder="Enter your email..."
                  />
                </div>
                <div class="col-12 col-md-3">
                  <button
                    type="submit"
                    class="btn btn-block btn-lg btn-primary"
                  >
                    Sign up!
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section> -->

    <!-- Footer -->
    <!-- <footer class="footer bg-dark footerStyle">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 h-100 text-center text-lg-left my-auto">
            <ul class="list-inline mb-2">
              <li class="list-inline-item">
                <a href="#">About</a>
              </li>
              <li class="list-inline-item">&sdot;</li>
              <li class="list-inline-item">
                <a href="#">Contact</a>
              </li>
              <li class="list-inline-item">&sdot;</li>
              <li class="list-inline-item">
                <a href="#">Terms of Use</a>
              </li>
              <li class="list-inline-item">&sdot;</li>
              <li class="list-inline-item">
                <a href="#">Privacy Policy</a>
              </li>
            </ul>
            <p class="text-muted small mb-4 mb-lg-0">
              &copy; Your Website 2019. All Rights Reserved.
            </p>
          </div>
          <div class="col-lg-6 h-100 text-center text-lg-right my-auto">
            <ul class="list-inline mb-0">
              <li class="list-inline-item mr-3">
                <a href="#">
                  <i class="fab fa-facebook fa-2x fa-fw"></i>
                </a>
              </li>
              <li class="list-inline-item mr-3">
                <a href="#">
                  <i class="fab fa-twitter-square fa-2x fa-fw"></i>
                </a>
              </li>
              <li class="list-inline-item">
                <a href="#">
                  <i class="fab fa-instagram fa-2x fa-fw"></i>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer> -->
  </div>
</template>

<script>
import { authService } from '@/app/shared/services/auth-service'
import { passwResetService } from '@/app/shared/services/passw-reset-service'
import { AuthResult } from '@/app/shared/models/auth-result-enum'
import { mapActions, mapState } from 'vuex'
import { colorShiftHsl, ColorThemeMixin } from '@/services/vuestic-ui'

export default {
  name: 'app',
  inject: ['contextConfig'],
  data(){
      return{
          color: '#1b1f22'
      }
  },
  computed: {
    ...mapState({ authenticated: state => state.user.authenticated }),
    navbarStyle () {
      const style = {
        backgroundColor: this.color,
      }

    //   if (this.contextConfig.gradient) {
    //     style.backgroundColor = colorShiftHsl(this.color, {
    //       s: -13,
    //       l: 15,
    //     }).css
    //   }

      if (this.contextConfig.shadow === 'sm') {
        style.boxShadow = !this.isTopBar ? '0 2px 3px 0 rgba(52, 56, 85, 0.25)' : null
      }
      return style
    },
    shapeStyle () {
      return {
        borderTopColor: this.contextConfig.gradient ? colorShiftHsl(this.color, {
          h: -1,
          s: -11,
          l: 10,
        }).css : 'transparent',
      }
    }
  },
  methods: {
    ...mapActions('user', ['authenticate']),
    async onLoginClick () {
      const result = await authService.signIn()
      switch (result) {
        case AuthResult.PASSW_RESET: {
          await passwResetService.resetPassw()
          break
        }
        case AuthResult.SUCCESS: {
          const token = await authService.getToken()
          if (token) {
            this.authenticate(token)
            this.$router.push('portal/dashboard')
          }
          break
        }
      }
    },
    onPortalClick () {
      this.$router.push('portal/dashboard')
    }
  },
}
</script>
<style src="../../../../../static/landing/vendor/bootstrap/css/bootstrap.min.css" scoped>
</style>
<style src="../../../../../static/landing/css/landing-page.min.css" scoped>
</style>
<style src="../../../../../static/landing/vendor/fontawesome-free/css/all.min.css" scoped>
</style>
<style src="../../../../../static/landing/vendor/simple-line-icons/css/simple-line-icons.css" scoped>
</style>

<style scoped>
.box {
  display: flex;
  flex-flow: column;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
}

.box .content.row {
  flex: 1 1 auto;
  width: 100vw;
  height: calc(100vh - 70px);
  justify-content: center;
  align-items: center;
  margin: 0;
}

.contentTile {
  color: white;
  font-size: x-large;
  font-weight: 900;
}

.tempSection {
  width: 100vw;
  background-color: black;
  height: 100vh;
}

.app-navbar {
  transition: background-color 0.3s ease; /* sidebar's bg color transitions as well -> consistency */
  display: flex;
  padding: 1rem 1rem;
  z-index: 1;
  align-items: center;
  justify-content: space-between;
}

.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.app-navbar__content {
  z-index: 1;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
  flex-wrap: wrap;
  height: 100%;
  flex: 1 1 auto;
}

.btn {
  background-color: rgb(212, 61, 39);
  box-shadow: rgba(212, 61, 39, 0.6) 0 0.125rem 0.19rem 0;
  color: white;
  padding: 0.375rem 1.25rem;
  font-size: 1rem;
  line-height: 1.5;
  border-radius: 1.5rem;
  letter-spacing: 0.032rem;
  font-weight: 700;
}

.btn:hover {
  color: white;
  background-color: rgba(212, 61, 39);
}

.btn:active {
  outline: none;
  border: none;
}

.btn:focus {
  outline: 0 !important;
  box-shadow: none;
}

.content {
  background-color: rgb(37, 42, 48);
}

.footerStyle {
  background-color: rgb(27, 31, 34);
  flex: 0 1 40px;
}

.headerStyle {
  background-color: rgb(27, 31, 34);
}
</style>
