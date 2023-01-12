import { defineStore } from "pinia";
import { IUser } from "../type";
import { v4 as uuidv4 } from "uuid";

type AuthState = {
  user?: IUser | null;
  token?: string | null;
};

export const useAuth = defineStore("auth", {
  state: (): AuthState => ({ user: null, token: null }),
  getters: {
    berear: (state) => `Bearer ${state.token ?? ""}`,
    isAuth: (state) => state.user !== null,
  },
  actions: {
    async login(email: string, password: string) {
      const user: IUser = {
        id: uuidv4().replaceAll("-", ""),
        name: "Tsiresy MIlà",
        role: "ADMIN",
        email: "tsiresymila@gmail.com",
        password: "testtest",
      };
      this.user = user;
      this.token = "test Token";
      return Promise.resolve<IUser>(user);
    },
    logout() {
      this.user = null;
      this.token = null;
    },
  },
  persist: {
    storage: sessionStorage,
  },
});
