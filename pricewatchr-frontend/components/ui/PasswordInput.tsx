import * as React from "react";
import { Eye, EyeOff } from "lucide-react";

import { Input } from "@/components/ui/input"; // Assuming your Input is imported like this
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils"; // Utility function for conditionally joining class names

// Extend the props of the original Input component
export interface PasswordInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const PasswordInput = React.forwardRef<HTMLInputElement, PasswordInputProps>(
  ({ className, ...props }, ref) => {
    const [showPassword, setShowPassword] = React.useState(false);

    return (
      <div className="relative">
        <Input
          // Conditionally set the input type
          type={showPassword ? "text" : "password"}
          className={cn("pr-10", className)} // Add padding for the button
          ref={ref}
          {...props}
        />
        <Button
          type="button" // Important: prevent this button from submitting the form
          variant="ghost"
          size="sm"
          className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
          onClick={() => setShowPassword((prev) => !prev)}
        >
          {showPassword ? (
            <Eye className="h-4 w-4" aria-label="Hide password" />
          ) : (
            <EyeOff className="h-4 w-4" aria-label="Show password" />
          )}
        </Button>
      </div>
    );
  }
);
PasswordInput.displayName = "PasswordInput";

export { PasswordInput };
