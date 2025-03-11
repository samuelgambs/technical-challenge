"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import UserRegistrationForm from "@/components/users/user-registration-form";
import UserList from "@/components/users/user-list";

export default function UsersPage() {
  // State to trigger a refresh of the user list
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  /**
   * Handles the event when a new user is created.
   * Increments the refresh trigger to update the user list.
   */
  const handleUserCreated = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Page title */}
      <h1 className="text-3xl font-bold mb-6">User Management</h1>

      {/* Tabs for switching between user list and registration form */}
      <Tabs defaultValue="list" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          {/* Tab trigger for user list */}
          <TabsTrigger value="list">User List</TabsTrigger>

          {/* Tab trigger for user registration form */}
          <TabsTrigger value="register">Register User</TabsTrigger>
        </TabsList>

        {/* Content for the user list tab */}
        <TabsContent value="list">
          <UserList refreshTrigger={refreshTrigger} />
        </TabsContent>

        {/* Content for the user registration tab */}
        <TabsContent value="register">
          <UserRegistrationForm onUserCreated={handleUserCreated} />
        </TabsContent>
      </Tabs>
    </div>
  );
}