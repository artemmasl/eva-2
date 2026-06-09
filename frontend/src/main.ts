import { createApp } from 'vue';
import { MotionPlugin } from '@vueuse/motion';

import App from './App.vue';
import { router } from './router';
import './styles/global.scss';
import { pinia } from './stores';

createApp(App).use(MotionPlugin).use(pinia).use(router).mount('#app');

const revealApp = () => document.documentElement.classList.add('app-ready');

const fontsReady = document.fonts ? document.fonts.ready : Promise.resolve();
const safetyTimeout = new Promise((resolve) => setTimeout(resolve, 1500));

void Promise.race([fontsReady, safetyTimeout]).finally(revealApp);
