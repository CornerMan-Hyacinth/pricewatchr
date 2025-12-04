"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Image from "next/image";
import { useForm } from "react-hook-form";
import { toast, Toaster } from "sonner";
import { z } from "zod";
import PriceWatchrLogo from "@/public/images/pricewatchr_logo_dark.png";
import { MoveLeft } from "lucide-react";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useParams } from "next/navigation";
import { PasswordInput } from "@/components/ui/PasswordInput";
import { resetPassword } from "@/services/auth";
import { useAuth } from "@/store/authStore";

const schema = z
  .object({
    token: z.string(),
    new_password: z
      .string()
      .min(8, "Password must be at least 8 characters long"),
    confirm_password: z.string(),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    error: "Passwords do not match",
    path: ["confirm_password"],
  });

type ResetPasswordFormData = z.infer<typeof schema>;

export default function ResetPasswordPage() {
  const params = useParams();
  const urlToken = Array.isArray(params.token) ? params.token[0] : params.token;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      token: urlToken || "",
      new_password: "",
      confirm_password: "",
    },
  });

  const setToken = useAuth((s) => s.setToken);

  const onSubmit = async (data: ResetPasswordFormData) => {
    if (data.token.trim() === "") {
      toast.error(
        "Invalid or missing reset token. Please restart the password reset process."
      );
      return;
    }

    try {
      const res = await resetPassword(data);
      setToken(res.access_token);
      toast.success("Password reset successfully!");
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 2000);
    } catch (e: any) {
      if (e.response.status === 400) {
        toast.error(
          "Invalid or expired reset token. Please restart the password reset process."
        );
      } else {
        toast.error(
          "Something went wrong. Please try again or restart the reset process."
        );
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Toaster position="bottom-right" richColors />

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-sm space-y-4 p-6 border rounded-xl shadow"
      >
        <div className="w-full flex items-center justify-center">
          <Image
            alt="pricewatchr logo"
            src={PriceWatchrLogo}
            width={50}
            height={50}
            quality={90}
          />
        </div>

        <h2 className="text-xl font-medium text-center mb-4">Reset password</h2>

        <div className="flex items-center justify-center mb-8 gap-x-4">
          <MoveLeft />
          <p className="text-black text-sm">
            Go back to{" "}
            <Link href={"/auth/login"} className="font-bold underline">
              Sign in
            </Link>
          </p>
        </div>

        <PasswordInput
          placeholder="New password"
          {...register("new_password")}
        />
        {errors.new_password && (
          <p className="text-red-500 text-sm">{errors.new_password.message}</p>
        )}

        <PasswordInput
          placeholder="Confirm password"
          {...register("confirm_password")}
        />
        {errors.confirm_password && (
          <p className="text-red-500 text-sm">
            {errors.confirm_password.message}
          </p>
        )}

        <Button type="submit" className="w-full mt-8">
          Reset
        </Button>
      </form>
    </div>
  );
}
