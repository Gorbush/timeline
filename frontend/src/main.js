/*
 * Copyright (C) 2021, 2022 Tobias Himstedt
 * 
 * 
 * This file is part of Timeline.
 * 
 * Timeline is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * Timeline is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */
import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import { store } from './store'
import router from './router'
import VueJustifiedLayout from 'vue-justified-layout'
import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css' // needs css-loader
import axios from "axios";

Vue.use(VueLayers)
Vue.use(VueJustifiedLayout);
Vue.config.productionTip = false;

console.log("Configuring axios")
let basePath = (window.TIMELINE_BASEPATH ? window.TIMELINE_BASEPATH : process.env.VUE_APP_TIMELINE_BASEPATH) || "";
let service_host = window.SERVICE_HOST ? window.SERVICE_HOST : window.location.hostname;
let service_port = window.SERVICE_PORT ? window.SERVICE_PORT : window.location.port;

let serviceUrl = `${window.location.protocol}//${service_host}:${service_port}${basePath}`

Vue.prototype.$basePath = serviceUrl;
axios.defaults.baseURL = serviceUrl;
console.log("Configuring axios URL="+axios.defaults.baseURL)

new Vue({
  vuetify,
  router: router,
  store,
  render: h => h(App)
}).$mount('#app')

