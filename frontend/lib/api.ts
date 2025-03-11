import axios, { AxiosInstance, AxiosResponse } from "axios";

// Create an Axios instance with default configurations for the API
const api: AxiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1", // Base URL of the API (versioned)
  headers: {
    "Content-Type": "application/json", // Set default content type
  },
});

// --- User API Calls ---

export const userApi = {
  /**
   * Fetches a list of users from the API.
   * @returns {Promise<any[]>} A promise that resolves to an array of user objects.
   */
  getUsers: async (): Promise<any[]> => {
    try {
      const response: AxiosResponse<any[]> = await api.get("/users/");
      return response.data;
    } catch (error) {
      console.error("Error fetching users:", error);
      throw error; // Re-throw the error for component-level handling
    }
  },

  /**
   * Creates a new user with the provided data.
   * @param {object} userData - User data (username, email, password).
   * @returns {Promise<any>} A promise that resolves to the created user object.
   */
  createUser: async (userData: {
    username: string;
    email: string;
    password: string;
  }): Promise<any> => {
    try {
      const response: AxiosResponse<any> = await api.post("/users/", userData);
      return response.data;
    } catch (error) {
      console.error("Error creating user:", error);
      throw error;
    }
  },

  /**
   * Deletes a user with the specified ID.
   * @param {number} userId - The ID of the user to delete.
   * @returns {Promise<any>} A promise that resolves to the response data.
   */
  deleteUser: async (userId: number): Promise<any> => {
    try {
      const response: AxiosResponse<any> = await api.delete(`/users/${userId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting user ${userId}:`, error);
      throw error;
    }
  },
};

// --- Post API Calls ---

export const postApi = {
  /**
   * Fetches a list of posts from the API.
   * @returns {Promise<any[]>} A promise that resolves to an array of post objects.
   */
  getPosts: async (): Promise<any[]> => {
    try {
      const response: AxiosResponse<any[]> = await api.get("/posts/");
      return response.data;
    } catch (error) {
      console.error("Error fetching posts:", error);
      throw error;
    }
  },

  /**
   * Creates a new post with the provided data.
   * @param {object} postData - Post data (title, content, author_id).
   * @returns {Promise<any>} A promise that resolves to the created post object.
   */
  createPost: async (postData: {
    title: string;
    content: string;
    author_id: number;
  }): Promise<any> => {
    try {
      const response: AxiosResponse<any> = await api.post("/posts/", postData);
      return response.data;
    } catch (error) {
      console.error("Error creating post:", error);
      throw error;
    }
  },

  /**
   * Updates an existing post with the specified ID and data.
   * @param {number} postId - The ID of the post to update.
   * @param {object} postData - Post data (title, content).
   * @returns {Promise<any>} A promise that resolves to the updated post object.
   */
  updatePost: async (
    postId: number,
    postData: { title: string; content: string }
  ): Promise<any> => {
    try {
      const response: AxiosResponse<any> = await api.patch(
        `/posts/${postId}/`,
        postData
      );
      return response.data;
    } catch (error) {
      console.error(`Error updating post ${postId}:`, error);
      throw error;
    }
  },

  /**
   * Deletes a post with the specified ID.
   * @param {number} postId - The ID of the post to delete.
   * @returns {Promise<any>} A promise that resolves to the response data.
   */
  deletePost: async (postId: number): Promise<any> => {
    try {
      const response: AxiosResponse<any> = await api.delete(
        `/posts/${postId}/`
      );
      return response.data;
    } catch (error) {
      console.error(`Error deleting post ${postId}:`, error);
      throw error;
    }
  },
};