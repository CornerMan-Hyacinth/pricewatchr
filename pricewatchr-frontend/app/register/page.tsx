"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast, Toaster } from "sonner";
import { z } from "zod";
import { registerUser } from "@/services/auth";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import PriceWatchrLogo from "@/public/images/pricewatchr_logo_dark.png";

const schema = z.object({
  name: z.string().min(1),
  email: z.email(),
  password: z.string().min(8),
});

export default function RegisterPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(schema) });

  const onSubmit = async (data: any) => {
    try {
      const res = await registerUser(data);
      toast.success("Success! Check your email to verify your account.");
    } catch (e: any) {
      console.error(e);
      if (e.response?.status === 400) {
        toast.error("An account with this email already exists.");
      } else {
        toast.error("Registration failed. Please try again later.");
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

        <h2 className="text-xl font-medium text-center mb-4">
          Welcome to PriceWatchr!
        </h2>

        <p className="text-black text-sm mb-8 text-center">
          Already have an account?{" "}
          <Link href={"/login"} className="font-bold underline">
            Sign in
          </Link>
        </p>

        <Input placeholder="Full name" {...register("name")} />
        {errors.name && (
          <p className="text-red-500 text-sm">{errors.name.message}</p>
        )}

        <Input placeholder="Email" {...register("email")} />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}

        <Input
          type="password"
          placeholder="Password"
          {...register("password")}
        />
        {errors.password && (
          <p className="text-red-500 text-sm">{errors.password.message}</p>
        )}

        <Button type="submit" className="w-full mt-8">
          Sign up
        </Button>

        <p className="text-black/50 text-xs text-center">
          By signing up, you agree to our{" "}
          <Link href={"/"} className="font-bold underline hover:text-black">
            Terms
          </Link>{" "}
          and{" "}
          <Link href={"/"} className="font-bold underline hover:text-black">
            Privacy Policy
          </Link>
          .
        </p>
      </form>
    </div>
  );
}
