import { api } from "@/lib/api";

interface EmailVerificationSendResponse {
  message: string;
  detail: "verification_code_sent";
}

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

export const sendEmailVerificationCode = async (email: string) => {
  const res = await api.post<EmailVerificationSendResponse>(
    "/auth/email/verification/send"
  );
  return res.data;
};

export const verifyEmail = async (data: { email: string; code: string }) => {
  const res = await api.post("/");
};

export const requestPasswordReset = async (data: { email: string }) => {
  const res = await api.post("/password/reset/request", data);
  return res.data;
};

export const resetPassword = async (data: {
  token: string;
  new_password: string;
}) => {
  const res = await api.post("/password/reset/confirm", data);
  return res.data;
};

export const getProfile = async (token: string) => {
  const res = await api.get("/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
};
