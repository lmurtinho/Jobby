import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, setAuthToken, clearAuthToken, getAuthToken } from '../utils/apiClient';

// Types for authentication
interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  skills?: string[];
  experienceLevel?: string;
  location?: string;
}

interface AuthContextType {
  // State
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  clearError: () => void;
  refreshProfile: () => Promise<void>;
}

interface RegisterData {
  name: string;
  email: string;
  password: string;
}

interface AuthProviderProps {
  children: ReactNode;
}

// Create the context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Custom hook to use the auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setTokenState] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const isAuthenticated = !!token && !!user;

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedToken = getAuthToken();
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
          setTokenState(storedToken);
          setUser(JSON.parse(storedUser));
          
          // Verify token is still valid by fetching profile
          try {
            const response = await authAPI.getProfile();
            setUser(response.data);
          } catch (error) {
            // Token is invalid, clear auth state
            logout();
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        logout();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await authAPI.login({ email, password });
      const { token: newToken, user: userData } = response.data;

      // Store auth data
      setAuthToken(newToken);
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Update state
      setTokenState(newToken);
      setUser(userData);
      
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Login failed. Please check your credentials.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: RegisterData): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await authAPI.register(userData);
      const { token: newToken, user: newUser } = response.data;

      // Store auth data
      setAuthToken(newToken);
      localStorage.setItem('user', JSON.stringify(newUser));
      
      // Update state
      setTokenState(newToken);
      setUser(newUser);
      
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Registration failed. Please try again.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = (): void => {
    try {
      // Call logout API (best effort - don't wait for response)
      authAPI.logout().catch(console.error);
    } catch (error) {
      console.error('Error during logout API call:', error);
    } finally {
      // Clear local state regardless of API call result
      clearAuthToken();
      setTokenState(null);
      setUser(null);
      setError(null);
    }
  };

  const clearError = (): void => {
    setError(null);
  };

  const refreshProfile = async (): Promise<void> => {
    try {
      if (!token) {
        throw new Error('No authentication token available');
      }

      const response = await authAPI.getProfile();
      const userData = response.data;
      
      // Update stored user data
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      
    } catch (error: any) {
      console.error('Error refreshing profile:', error);
      
      // If unauthorized, logout user
      if (error.response?.status === 401) {
        logout();
      }
      
      throw error;
    }
  };

  const contextValue: AuthContextType = {
    // State
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    
    // Actions
    login,
    register,
    logout,
    clearError,
    refreshProfile,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Export the context for testing purposes
export { AuthContext };
export default AuthProvider;
