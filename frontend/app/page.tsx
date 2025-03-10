import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] gap-8">
      <h1 className="text-4xl font-bold text-center">Welcome to SocialConnect</h1>
      <p className="text-xl text-center text-muted-foreground max-w-2xl">
        A modern social media platform for connecting with friends and sharing your thoughts.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl mt-8">
        <Card>
          <CardHeader>
            <CardTitle>User Management</CardTitle>
            <CardDescription>Register, view and manage users</CardDescription>
          </CardHeader>
          <CardContent className="flex justify-center">
            <Link href="/users">
              <Button size="lg">Go to Users</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Post Management</CardTitle>
            <CardDescription>Create, view and manage posts</CardDescription>
          </CardHeader>
          <CardContent className="flex justify-center">
            <Link href="/posts">
              <Button size="lg">Go to Posts</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

