"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { requestPasswordReset } from "@/services/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import Image from "next/image";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { toast, Toaster } from "sonner";
import { z } from "zod";
import PriceWatchrLogo from "@/public/images/pricewatchr_logo_dark.png";
import { MoveLeft } from "lucide-react";

const schema = z.object({
  email: z.email(),
});

export default function ForgotPasswordPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: any) => {
    try {
      await requestPasswordReset(data);
      toast.success(
        "We've sent an email with a reset link. Please check your spam folder as well."
      );
    } catch (e: any) {
      toast.error("Something went wrong. Please try again.");
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

        <h2 className="text-xl font-medium text-center mb-4">
          Forgot password?
        </h2>

        <div className="flex items-center justify-center mb-8 gap-x-4">
          <MoveLeft />
          <p className="text-black text-sm">
            Go back to{" "}
            <Link href={"/auth/login"} className="font-bold underline">
              Sign in
            </Link>
          </p>
        </div>

        <Input placeholder="Email" {...register("email")} />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}

        <Button type="submit" className="w-full mt-8">
          Request link
        </Button>
      </form>
    </div>
  );
}
