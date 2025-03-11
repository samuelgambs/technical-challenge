"use client";

import { useState, useEffect } from "react";
import { userApi } from "@/lib/api";
import { toast } from "sonner";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
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
} from "@/components/ui/alert-dialog";

// Interface for user data
interface User {
  id: number;
  username: string;
  email: string;
}

// Props interface for the UserList component
interface UserListProps {
  refreshTrigger: number;
}

export default function UserList({ refreshTrigger }: UserListProps) {
  // State to store the list of users
  const [users, setUsers] = useState<User[]>([]);

  // State to track if users are being loaded
  const [isLoading, setIsLoading] = useState(true);

  // State to store any error messages
  const [error, setError] = useState<string | null>(null);

  // State to track the user ID to be deleted
  const [userToDelete, setUserToDelete] = useState<number | null>(null);

  // Fetch users when the component mounts or refreshTrigger changes
  useEffect(() => {
    fetchUsers();
  }, [refreshTrigger]);

  // Function to fetch users from the API
  const fetchUsers = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await userApi.getUsers();
      setUsers(data);
    } catch (err) {
      console.error("Error fetching users:", err);
      setError("Failed to load users. Please try again.");
      toast.error("Failed to load users");
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle user deletion
  const handleDeleteUser = async (userId: number) => {
    try {
      await userApi.deleteUser(userId);
      setUsers(users.filter((user) => user.id !== userId));
      toast.success("User deleted successfully");
    } catch (err) {
      console.error("Error deleting user:", err);
      toast.error("Failed to delete user");
    } finally {
      setUserToDelete(null);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>User List</CardTitle>
        <CardDescription>Manage registered users</CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : error ? (
          <div className="text-center py-8 text-red-500">{error}</div>
        ) : users.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">No users found</div>
        ) : (
          <div className="divide-y">
            {users.map((user) => (
              <div key={user.id} className="py-4 flex justify-between items-center">
                <div>
                  <h3 className="font-medium">{user.username}</h3>
                  <p className="text-sm text-muted-foreground">{user.email}</p>
                </div>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="outline" size="icon" onClick={() => setUserToDelete(user.id)}>
                      <Trash2 className="h-4 w-4 text-red-500" />
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                      <AlertDialogDescription>
                        This will permanently delete the user "{user.username}" and all associated data. This action
                        cannot be undone.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction
                        className="bg-red-500 hover:bg-red-600"
                        onClick={() => handleDeleteUser(user.id)}
                      >
                        Delete
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}