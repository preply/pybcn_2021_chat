import { axiosInstance } from "./axios-instance";

export const getUser = () => axiosInstance.get("/users/me");
