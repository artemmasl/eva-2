import { createApp } from 'vue';
import { MotionPlugin } from '@vueuse/motion';

import App from './App.vue';
import { router } from './router';
import './styles/global.scss';
import { pinia } from './stores';

createApp(App).use(MotionPlugin).use(pinia).use(router).mount('#app');
