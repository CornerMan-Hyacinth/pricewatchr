import { api } from "@/lib/api";

export const login = async (email: string, password: string) => {
  const res = await api.post("/auth/login", { email, password });
  return res.data;
};

export const registerUser = async (data: {
  email: string;
  password: string;
  name: string;
}) => {
  const res = await api.post("/auth/register", data);
  return res.data;
};

export const getProfile = async (token: string) => {
  const res = await api.get("/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
};
