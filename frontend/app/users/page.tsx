"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import UserRegistrationForm from "@/components/users/user-registration-form"
import UserList from "@/components/users/user-list"

export default function UsersPage() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleUserCreated = () => {
    setRefreshTrigger((prev) => prev + 1)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">User Management</h1>

      <Tabs defaultValue="list" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="list">User List</TabsTrigger>
          <TabsTrigger value="register">Register User</TabsTrigger>
        </TabsList>

        <TabsContent value="list">
          <UserList refreshTrigger={refreshTrigger} />
        </TabsContent>

        <TabsContent value="register">
          <UserRegistrationForm onUserCreated={handleUserCreated} />
        </TabsContent>
      </Tabs>
    </div>
  )
}

