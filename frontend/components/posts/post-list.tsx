"use client"

import { useState, useEffect } from "react"
import { postApi } from "@/lib/api"
import { toast } from "sonner"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Pencil, Trash2 } from "lucide-react"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

interface Post {
  id: number
  title: string
  content: string
  user_id: number
}

interface PostListProps {
  refreshTrigger: number
  onEditPost: (post: { id: number; title: string; content: string }) => void
}

export default function PostList({ refreshTrigger, onEditPost }: PostListProps) {
  const [posts, setPosts] = useState<Post[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [postToDelete, setPostToDelete] = useState<number | null>(null)

  useEffect(() => {
    fetchPosts()
  }, [refreshTrigger])

  const fetchPosts = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const data = await postApi.getPosts()
      setPosts(data)
    } catch (err) {
      console.error("Error fetching posts:", err)
      setError("Failed to load posts. Please try again.")
      toast.error("Failed to load posts")
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeletePost = async (postId: number) => {
    try {
      await postApi.deletePost(postId)
      setPosts(posts.filter((post) => post.id !== postId))
      toast.success("Post deleted successfully")
    } catch (err) {
      console.error("Error deleting post:", err)
      toast.error("Failed to delete post")
    } finally {
      setPostToDelete(null)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Post List</CardTitle>
        <CardDescription>View and manage all posts</CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : error ? (
          <div className="text-center py-8 text-red-500">{error}</div>
        ) : posts.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">No posts found</div>
        ) : (
          <div className="space-y-6">
            {posts.map((post) => (
              <Card key={post.id} className="overflow-hidden">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <CardTitle>{post.title}</CardTitle>
                    <div className="flex gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() =>
                          onEditPost({
                            id: post.id,
                            title: post.title,
                            content: post.content,
                          })
                        }
                      >
                        <Pencil className="h-4 w-4 text-blue-500" />
                      </Button>
                      <AlertDialog>
                        <AlertDialogTrigger asChild>
                          <Button variant="ghost" size="icon" onClick={() => setPostToDelete(post.id)}>
                            <Trash2 className="h-4 w-4 text-red-500" />
                          </Button>
                        </AlertDialogTrigger>
                        <AlertDialogContent>
                          <AlertDialogHeader>
                            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                            <AlertDialogDescription>
                              This will permanently delete this post. This action cannot be undone.
                            </AlertDialogDescription>
                          </AlertDialogHeader>
                          <AlertDialogFooter>
                            <AlertDialogCancel>Cancel</AlertDialogCancel>
                            <AlertDialogAction
                              className="bg-red-500 hover:bg-red-600"
                              onClick={() => handleDeletePost(post.id)}
                            >
                              Delete
                            </AlertDialogAction>
                          </AlertDialogFooter>
                        </AlertDialogContent>
                      </AlertDialog>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground whitespace-pre-line">{post.content}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

