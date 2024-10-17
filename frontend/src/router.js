import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./views/HomePage.vue"; // Puoi mantenere questa sezione per il futuro
import UserRegister from "./components/UserRegister.vue"; // Solo la pagina di registrazione

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: HomePage, // Se vuoi mantenere la home page per il futuro
  },
  {
    path: "/register",
    name: "UserRegister",
    component: UserRegister,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;
