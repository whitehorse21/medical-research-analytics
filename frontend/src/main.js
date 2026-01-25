import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import "./composables/useTheme"; // Import to initialize theme

createApp(App).use(router).mount("#app");
