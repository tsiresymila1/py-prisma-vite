import { RouteRecordRaw } from "vue-router";

export const routes: RouteRecordRaw[] = [
  {
    name: "home",
    path: "/",
    component: async () => await import("./components/layout/Dashboard.vue"),
    children: [
      {
        name: "dashboard",
        path: "",
        component: async () => await import("./pages/Dashboard.vue"),
      },
      {
        name: "admin",
        path: "admin",
        component: async () => await import("./pages/Admin.vue"),
        children: [
          {
            name : "add_list",
            path: "",
            component: async () => await import('./components/Admin/AdminList.vue')
          },
          {
            name : "add_admin",
            path: "add",
            component: async () => await import('./components/Admin/AdminForm.vue')
          }
        ]
      },
    ],
  },
  {
    name: "login",
    path: "/login",
    component: async () => await import("./pages/Login.vue"),
  },
  {
    name: "register",
    path: "/register",
    component: async () => await import("./pages/Register.vue"),
  },
  {
    name: "notfound",
    path: "/:pathMatch(.*)*",
    component: async () => await import("./pages/NotFound.vue"),
  },
];
