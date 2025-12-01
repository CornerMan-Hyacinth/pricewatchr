"use client";

import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { login } from "@/services/auth";
import { useAuth } from "@/store/authStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});

export default function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
  });

  const setToken = useAuth((s) => s.setToken);

  const onSubmit = async (data: any) => {
    try {
      const res = await login(data.email, data.password);
      setToken(res.access_token);
      alert("Logged in!");
      window.location.href = "/dashboard";
    } catch (e) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-sm space-y-4 p-6 border rounded-xl shadow"
      >
        <h2 className="text-xl font-bold text-center">Login</h2>

        <Input placeholder="Email" {...register("email")} />
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}

        <Input
          type="password"
          placeholder="Password"
          {...register("password")}
        />
        {errors.password && (
          <p className="text-red-500">{errors.password.message}</p>
        )}

        <Button type="submit" className="w-full">
          Login
        </Button>
      </form>
    </div>
  );
}
