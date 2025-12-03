"use client";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { login } from "@/services/auth";
import { useAuth } from "@/store/authStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Toaster, toast } from "sonner";
import Link from "next/link";
import PriceWatchrLogo from "@/public/images/pricewatchr_logo_dark.png";
import Image from "next/image";
import { PasswordInput } from "@/components/ui/PasswordInput";

const schema = z.object({
  email: z.email(),
  password: z.string().min(8),
});

type LoginFormData = z.infer<typeof schema>;

export default function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const setToken = useAuth((s) => s.setToken);

  const onSubmit = async (data: LoginFormData) => {
    try {
      const res = await login(data.email, data.password);
      setToken(res.access_token);
      toast.success("You have logged in successfully!");
      window.location.href = "/dashboard";
    } catch (e: any) {
      console.error(e);
      if (e.response.status === 401) {
        toast.error(e.response.data.message);
      } else {
        toast.error("Login failed. Please try again later.");
      }
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center">
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
          Sign in to continue
        </h2>

        <p className="text-black text-sm mb-8 text-center">
          Don;t have an account?{" "}
          <Link href={"/register"} className="font-bold underline">
            Sign up
          </Link>
        </p>

        <Input placeholder="Email" {...register("email")} />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}

        <PasswordInput placeholder="Password" {...register("password")} />
        {errors.password && (
          <p className="text-red-500 text-sm">{errors.password.message}</p>
        )}

        <Link href={"/"} className="text-sm underline cursor-pointer">
          Forgot password?
        </Link>

        <Button type="submit" className="w-full mt-8" disabled={isSubmitting}>
          {isSubmitting ? "Signing in..." : "Sign in"}
        </Button>
      </form>
    </main>
  );
}
