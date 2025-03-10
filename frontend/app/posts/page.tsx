"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import PostCreationForm from "@/components/posts/post-creation-form"
import PostList from "@/components/posts/post-list"

export default function PostsPage() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [editingPost, setEditingPost] = useState<{
    id: number
    title: string
    content: string
  } | null>(null)

  const handlePostCreated = () => {
    setRefreshTrigger((prev) => prev + 1)
  }

  const handleEditPost = (post: { id: number; title: string; content: string }) => {
    setEditingPost(post)
  }

  const handlePostUpdated = () => {
    setRefreshTrigger((prev) => prev + 1)
    setEditingPost(null)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Post Management</h1>

      <Tabs defaultValue="list" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="list">Post List</TabsTrigger>
          <TabsTrigger value="create">{editingPost ? "Edit Post" : "Create Post"}</TabsTrigger>
        </TabsList>

        <TabsContent value="list">
          <PostList refreshTrigger={refreshTrigger} onEditPost={handleEditPost} />
        </TabsContent>

        <TabsContent value="create">
          <PostCreationForm
            onPostCreated={handlePostCreated}
            onPostUpdated={handlePostUpdated}
            editingPost={editingPost}
          />
        </TabsContent>
      </Tabs>
    </div>
  )
}

