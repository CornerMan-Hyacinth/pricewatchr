"use client";

import { Button } from "@/components/ui/button";
import { sendEmailVerificationCode } from "@/services/auth";
import { ErrorResponseModel } from "@/types/api-responses";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import Image from "next/image";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { toast, Toaster } from "sonner";
import { z } from "zod";
import PriceWatchrLogo from "@/public/images/pricewatchr_logo_dark.png";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
} from "@/components/ui/input-otp";
import SvgLoader from "@/components/ui/SvgLoader";

const VERIFICATION_CODE_LENGTH = 6;
const RESEND_COOLDOWN_SECONDS = 90;

const schema = z.object({
  pin: z
    .string()
    .min(VERIFICATION_CODE_LENGTH, {
      error: `Your code must be ${VERIFICATION_CODE_LENGTH} characters.`,
    })
    .max(VERIFICATION_CODE_LENGTH, {
      error: `Your code must be ${VERIFICATION_CODE_LENGTH} characters.`,
    }),
});

type VerifyEmailFormData = z.infer<typeof schema>;

export default function VerifyEmailPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const userEmail = searchParams.get("email");

  const [isSendingOTP, setSendingOTP] = useState(false);
  const [secondsLeft, setSecondsLeft] = useState(0);

  const form = useForm<VerifyEmailFormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      pin: "",
    },
  });

  const sendVerificationCode = async () => {
    if (isSendingOTP || secondsLeft > 0) return;

    if (!userEmail) {
      toast.error("No email address found", {
        description:
          "You can click the link within the email sent to you. Or try signing up again",
      });
      return;
    }

    setSendingOTP(true);

    try {
      const data = await sendEmailVerificationCode({ email: userEmail });
      if (data.detail === "verification_code_sent") {
        if (data.message === "Email already verified") {
          toast(data.message, {
            description: "You can proceed to sign in.",
          });

          setTimeout(() => {
            router.push("/login");
          }, 3000);
        } else {
          toast.success(data.message);
        }
      }

      setSecondsLeft(RESEND_COOLDOWN_SECONDS);
      setSendingOTP(false);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const { response } = error;
        const errorBody: ErrorResponseModel = response.data;
        const errorMessage = errorBody.message || "An unknown error occurred.";

        toast.error(errorMessage);
        if (response.status === 404) {
          router.back();
        }
      } else {
        console.error("Network or unknown error:", error);
        toast.error("Could not connect to the server");
      }
    }
  };

  useEffect(() => {
    // sendVerificationCode();
  }, []);

  useEffect(() => {
    if (secondsLeft <= 0) return;

    const timer = setInterval(() => {
      setSecondsLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [secondsLeft]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };

  const onSubmit = async (data: VerifyEmailFormData) => {
    try {
      // const res = await
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const { response } = error;
        const errorBody: ErrorResponseModel = response.data;
        const errorMessage = error.message || "An unknown error occurred";

        if (response.status === 404) {
          toast.error("User not found", {
            description:
              "Click the alternative link provided in the email. Else, try signing up.",
          });
        } else if (
          response.status === 400 &&
          errorMessage === "Email already verified"
        ) {
          toast.error("Email already verified.", {
            description: "We're redirecting you to login now...",
          });
        } else {
          toast.error(errorMessage);
        }
      } else {
        console.error("Network or Unexpected Error:", error);
        toast.error("Could not connect to server.");
      }

      return null;
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center">
      <Toaster position="bottom-right" richColors />

      <div className="w-full max-w-sm space-y-4 p-6 border rounded-xl shadow flex flex-col items-center">
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

        <p className="text-base text-center text-gray-500 mb-8">
          We sent a 6-digit code to{" "}
          <span className="font-medium">{userEmail}</span>
        </p>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
              control={form.control}
              name="pin"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <InputOTP
                      maxLength={VERIFICATION_CODE_LENGTH}
                      value={field.value}
                      onChange={(value) => field.onChange(value)}
                      onComplete={(value) => {
                        field.onChange(value);
                        form.handleSubmit(onSubmit)();
                      }}
                    >
                      <InputOTPGroup>
                        {Array.from(
                          { length: VERIFICATION_CODE_LENGTH },
                          (_, i) => (
                            <InputOTPSlot
                              key={i}
                              index={i}
                              className="h-12 w-12"
                            />
                          )
                        )}
                      </InputOTPGroup>
                    </InputOTP>
                  </FormControl>
                  <FormMessage className="text-center" />
                </FormItem>
              )}
            />

            <p className="text-sm flex items-center gap-x-1">
              Didn&apos;t get the code?{" "}
              {secondsLeft > 0 ? (
                <span className="font-medium">
                  Resend in {formatTime(secondsLeft)}
                </span>
              ) : (
                <button
                  type="button"
                  onClick={sendVerificationCode}
                  disabled={isSendingOTP}
                  className={`font-bold underline transition-all text-primary hover:text-primary/80 cursor-pointer`}
                >
                  {isSendingOTP ? (
                    <SvgLoader color="#000" size={20} />
                  ) : (
                    <span>Resend</span>
                  )}
                </button>
              )}
            </p>

            <Button
              type="submit"
              className="w-full mt-8"
              disabled={form.formState.isSubmitting || isSendingOTP}
            >
              {form.formState.isSubmitting ? "Verifying..." : "Verify Email"}
            </Button>
          </form>
        </Form>
      </div>
    </main>
  );
}
