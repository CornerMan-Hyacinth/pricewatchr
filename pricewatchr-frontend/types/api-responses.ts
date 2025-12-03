export interface SuccessResponseModel<T> {
  status: "success";
  message: string;
  data: T;
}

export interface ErrorResponseModel {
  status: "error";
  message: string;
  data: any;
}

export interface AuthResponse {
  message: string;
  access_token: string;
  token_type: string;
}

export interface EmailVerificationSendResponse {
  message: string;
  detail: "verification_code_sent";
}
