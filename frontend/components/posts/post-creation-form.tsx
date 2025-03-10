"use client"

import { useState, useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { postApi, userApi } from "@/lib/api"
import { toast } from "sonner"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { AlertCircle, CheckCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

// Interface para usuário
interface User {
  id: number
  username: string
  email: string
}

const formSchema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters"),
  content: z.string().min(10, "Content must be at least 10 characters"),
  author_id: z.string().min(1, "Please select an author"),
})

type FormValues = z.infer<typeof formSchema>

interface PostCreationFormProps {
  onPostCreated: () => void
  onPostUpdated: () => void
  editingPost: {
    id: number
    title: string
    content: string
  } | null
}

export default function PostCreationForm({ onPostCreated, onPostUpdated, editingPost }: PostCreationFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [formStatus, setFormStatus] = useState<{
    type: "success" | "error" | null
    message: string | null
  }>({ type: null, message: null })

  const [users, setUsers] = useState<User[]>([])
  const [isLoadingUsers, setIsLoadingUsers] = useState(true)

  // Buscar a lista de usuários
  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoadingUsers(true)
      try {
        const data = await userApi.getUsers()
        setUsers(data)
      } catch (error) {
        console.error("Error fetching users:", error)
        toast.error("Failed to load users")
      } finally {
        setIsLoadingUsers(false)
      }
    }

    fetchUsers()
  }, [])

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: "",
      content: "",
      author_id: "",
    },
  })

  // Update form values when editing post changes
  useEffect(() => {
    if (editingPost) {
      form.reset({
        title: editingPost.title,
        content: editingPost.content,
        author_id: "", // Idealmente, você buscaria o autor do post aqui
      })
    } else {
      form.reset({
        title: "",
        content: "",
        author_id: "",
      })
    }
  }, [editingPost, form])

  const onSubmit = async (data: FormValues) => {
    setIsSubmitting(true)
    setFormStatus({ type: null, message: null })

    try {
      if (editingPost) {
        // Update existing post - não enviamos o author_id na atualização
        const { author_id, ...updateData } = data
        await postApi.updatePost(editingPost.id, updateData)

        setFormStatus({
          type: "success",
          message: "Post updated successfully!",
        })

        onPostUpdated()

        toast.success("Post has been updated successfully")
      } else {
        // Create new post
        await postApi.createPost({
          title: data.title,
          content: data.content,
          author_id: Number.parseInt(data.author_id), // Convertendo string para número
        })

        setFormStatus({
          type: "success",
          message: "Post created successfully!",
        })

        form.reset()
        onPostCreated()

        toast.success("Post has been created successfully")
      }
    } catch (error: any) {
      console.error("Post submission error:", error)

      let errorMessage = "An unexpected error occurred"

      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = "Invalid data provided. Please check your inputs."
          console.error("API Error Details:", error.response.data)
        } else if (error.response.status === 500) {
          errorMessage = "Server error. Please try again later."
        }
      }

      setFormStatus({
        type: "error",
        message: errorMessage,
      })

      toast.error(errorMessage)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{editingPost ? "Edit Post" : "Create New Post"}</CardTitle>
        <CardDescription>
          {editingPost ? "Update your existing post" : "Share your thoughts with the community"}
        </CardDescription>
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
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter post title" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="content"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Content</FormLabel>
                  <FormControl>
                    <Textarea placeholder="Write your post content here..." className="min-h-[150px]" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {!editingPost && (
              <FormField
                control={form.control}
                name="author_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Author</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value} disabled={isLoadingUsers}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select an author" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {isLoadingUsers ? (
                          <SelectItem value="loading" disabled>
                            Loading users...
                          </SelectItem>
                        ) : users.length === 0 ? (
                          <SelectItem value="none" disabled>
                            No users available
                          </SelectItem>
                        ) : (
                          users.map((user) => (
                            <SelectItem key={user.id} value={user.id.toString()}>
                              {user.username}
                            </SelectItem>
                          ))
                        )}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}

            <div className="flex gap-4 justify-end">
              {editingPost && (
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    form.reset()
                    onPostUpdated() // This will also clear the editing state
                  }}
                >
                  Cancel
                </Button>
              )}

              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting
                  ? editingPost
                    ? "Updating..."
                    : "Creating..."
                  : editingPost
                    ? "Update Post"
                    : "Create Post"}
              </Button>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}

