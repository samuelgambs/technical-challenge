"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { userApi } from "@/lib/api";
import { toast } from "sonner";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { AlertCircle, CheckCircle } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

// Zod schema for form validation
const formSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

// Type for form values inferred from the schema
type FormValues = z.infer<typeof formSchema>;

// Props interface for the UserRegistrationForm component
interface UserRegistrationFormProps {
  onUserCreated: () => void;
}

export default function UserRegistrationForm({ onUserCreated }: UserRegistrationFormProps) {
  // State to track if the form is submitting
  const [isSubmitting, setIsSubmitting] = useState(false);

  // State to manage form submission status (success or error)
  const [formStatus, setFormStatus] = useState<{
    type: "success" | "error" | null;
    message: string | null;
  }>({ type: null, message: null });

  // Initialize the form with react-hook-form
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
    },
  });

  // Handle form submission
  const onSubmit = async (data: FormValues) => {
    setIsSubmitting(true);
    setFormStatus({ type: null, message: null });

    try {
      await userApi.createUser(data);

      setFormStatus({
        type: "success",
        message: "User registered successfully!",
      });

      form.reset();
      onUserCreated();

      toast.success("User has been registered successfully");
    } catch (error: any) {
      console.error("Registration error:", error);

      let errorMessage = "An unexpected error occurred";

      if (error.response) {
        // Handle different status codes
        if (error.response.status === 400) {
          errorMessage = "Invalid data provided. Please check your inputs.";
        } else if (error.response.status === 500) {
          errorMessage = "Server error. Please try again later.";
        }
      }

      setFormStatus({
        type: "error",
        message: errorMessage,
      });

      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Register New User</CardTitle>
        <CardDescription>Create a new user account</CardDescription>
      </CardHeader>
      <CardContent>
        {formStatus.type && (
          <Alert variant={formStatus.type === "error" ? "destructive" : "default"} className="mb-6">
            {formStatus.type === "error" ? <AlertCircle className="h-4 w-4" /> : <CheckCircle className="h-4 w-4" />}
            <AlertTitle>{formStatus.type === "error" ? "Error" : "Success"}</AlertTitle>
            <AlertDescription>{formStatus.message}</AlertDescription>
          </Alert>
        )}

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Username</FormLabel>
                  <FormControl>
                    <Input placeholder="johndoe" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input type="email" placeholder="john@example.com" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="••••••" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? "Registering..." : "Register User"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}