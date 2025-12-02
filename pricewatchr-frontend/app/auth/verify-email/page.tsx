import { sendEmailVerificationCode } from "@/services/auth";
import { ErrorResponseModel } from "@/types/api-responses";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const VERIFICATION_CODE_LENGTH = 6;
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

interface EmailVerificationSendResponse {
  meessage: string;
  detail: "verification_code_sent";
}

export default function VerifyEmailPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get("email");
  const [isSendingOTP, setSendingOTP] = useState(true);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<VerifyEmailFormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      pin: "",
    },
  });

  const onSubmit = async (data: VerifyEmailFormData) => {
    try {
      // const res = await
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const { response } = error;
      }
    }
  };

  const sendVerificationCode = async () => {
    if (!email) {
      toast.error("No email address found", {
        description:
          "You can click the link within the email sent to you. Or try signing up again",
      });
      return;
    }

    setSendingOTP(true);

    try {
      const data = await sendEmailVerificationCode(email);
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
    sendVerificationCode();
  }, []);
}
