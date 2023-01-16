import { RouteRecordRaw } from "vue-router";

export const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: import("./components/layout/Dashboard.vue"),
    children: [
      {
        name: "dashboard",
        path: "",
        component: import("./pages/Dashboard.vue"), 
      },
      {
        name: "admin",
        path: "admin",
        component: import("./pages/Admin.vue"),
        children: [
          {
            name : "add_list",
            path: "",
            component: import('./components/Admin/AdminList.vue')
          },
          {
            name : "add_admin",
            path: "add",
            component: import('./components/Admin/AdminForm.vue')
          }
        ]
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
