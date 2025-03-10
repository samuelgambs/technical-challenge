import axios from "axios"

// Create an axios instance with default config
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
})

// User API calls
export const userApi = {
  getUsers: async () => {
    const response = await api.get("/users/")
    return response.data
  },

  createUser: async (userData: { username: string; email: string; password: string }) => {
    const response = await api.post("/users/", userData)
    return response.data
  },

  deleteUser: async (userId: number) => {
    const response = await api.delete(`/users/${userId}/`)
    return response.data
  },
}

// Post API calls
export const postApi = {
  getPosts: async () => {
    const response = await api.get("/posts/")
    return response.data
  },

  createPost: async (postData: { title: string; content: string; author_id: number }) => {
    const response = await api.post("/posts/", postData)
    return response.data
  },

  updatePost: async (postId: number, postData: { title: string; content: string }) => {
    const response = await api.patch(`/posts/${postId}/`, postData)
    return response.data
  },

  deletePost: async (postId: number) => {
    const response = await api.delete(`/posts/${postId}/`)
    return response.data
  },
}

