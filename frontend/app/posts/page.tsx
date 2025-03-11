"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import PostCreationForm from "@/components/posts/post-creation-form";
import PostList from "@/components/posts/post-list";

export default function PostsPage() {
  // State to trigger a refresh of the post list
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // State to manage the post being edited
  const [editingPost, setEditingPost] = useState<{
    id: number;
    title: string;
    content: string;
  } | null>(null);

  /**
   * Handles the event when a new post is created.
   * Increments the refresh trigger to update the post list.
   */
  const handlePostCreated = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  /**
   * Handles the event when a post is selected for editing.
   * Sets the editing post state with the selected post data.
   * @param {object} post - The post object to be edited.
   */
  const handleEditPost = (post: {
    id: number;
    title: string;
    content: string;
  }) => {
    setEditingPost(post);
  };

  /**
   * Handles the event when a post is updated.
   * Increments the refresh trigger and clears the editing post state.
   */
  const handlePostUpdated = () => {
    setRefreshTrigger((prev) => prev + 1);
    setEditingPost(null);
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Page title */}
      <h1 className="text-3xl font-bold mb-6">Post Management</h1>

      {/* Tabs for switching between post list and creation/edit form */}
      <Tabs defaultValue="list" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          {/* Tab trigger for post list */}
          <TabsTrigger value="list">Post List</TabsTrigger>

          {/* Tab trigger for post creation/edit form */}
          <TabsTrigger value="create">
            {editingPost ? "Edit Post" : "Create Post"}
          </TabsTrigger>
        </TabsList>

        {/* Content for the post list tab */}
        <TabsContent value="list">
          <PostList
            refreshTrigger={refreshTrigger}
            onEditPost={handleEditPost}
          />
        </TabsContent>

        {/* Content for the post creation/edit tab */}
        <TabsContent value="create">
          <PostCreationForm
            onPostCreated={handlePostCreated}
            onPostUpdated={handlePostUpdated}
            editingPost={editingPost}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}