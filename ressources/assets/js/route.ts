import { RouteRecordRaw } from "vue-router";

export const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: import("./components/layout/Dashboard.vue"),
    children: [
      {
        path: "",
        component: import("./pages/Dashboard.vue"),
      },
      {
        path: "admin",
        component: import("./pages/Admin.vue"),
      },
    ],
  },
  {
    path: "/login",
    component: import("./pages/Login.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    component: import("./pages/NotFound.vue"),
  },
];
