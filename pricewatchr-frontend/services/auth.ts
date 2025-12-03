import { api } from "@/lib/api";
import {
  AuthResponse,
  EmailVerificationSendResponse,
  SuccessResponseModel,
} from "@/types/api-responses";
import { User } from "@/types/models";

export const login = async (email: string, password: string) => {
  const res = await api.post<AuthResponse>("/auth/login", { email, password });
  return res.data;
};

export const registerUser = async (data: {
  email: string;
  password: string;
  name: string;
}) => {
  const res = await api.post<SuccessResponseModel<User>>(
    "/auth/register",
    data
  );
  return res.data;
};

export const sendEmailVerificationCode = async (data: { email: string }) => {
  const res = await api.post<EmailVerificationSendResponse>(
    "/auth/email/verification/send",
    data
  );
  return res.data;
};

export const verifyEmailVerificationCode = async (data: {
  email: string;
  code: string;
}) => {
  const res = await api.post<AuthResponse>(
    "/auth/email/verification/verify",
    data
  );
  return res.data;
};

export const requestPasswordReset = async (data: { email: string }) => {
  const res = await api.post<SuccessResponseModel<null>>(
    "/password/reset/request",
    data
  );
  return res.data;
};

export const resetPassword = async (data: {
  token: string;
  new_password: string;
}) => {
  const res = await api.post<AuthResponse>("/password/reset/confirm", data);
  return res.data;
};

export const getProfile = async (token: string) => {
  const res = await api.get<SuccessResponseModel<User>>("/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
};
