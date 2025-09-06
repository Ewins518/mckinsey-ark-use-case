import { apiClient } from '@/lib/api/client'
import type { components } from '@/lib/api/generated/types'

// Helper type for axios errors
interface AxiosError extends Error {
  response?: {
    status: number
  }
}

// Use the generated types from OpenAPI
export type MemoryResponse = components['schemas']['MemoryResponse']
export type MemoryDetailResponse = components['schemas']['MemoryDetailResponse']
export type MemoryListResponse = components['schemas']['MemoryListResponse']
export type MemoryCreateRequest = components['schemas']['MemoryCreateRequest']
export type MemoryUpdateRequest = components['schemas']['MemoryUpdateRequest']

// For UI compatibility, we'll map the API response to include an id field
export type Memory = MemoryDetailResponse & { id: string }

// CRUD Operations
export const memoriesService = {
  // Get all memories
  async getAll(namespace: string): Promise<Memory[]> {
    const response = await apiClient.get<MemoryListResponse>(`/api/v1/namespaces/${namespace}/memories`)
    
    // Map the response items to include id for UI compatibility
    const memories = await Promise.all(
      response.items.map(async (item) => {
        // Fetch detailed info for each memory to get full data
        const detailed = await memoriesService.getByName(namespace, item.name)
        return detailed!
      })
    )
    
    return memories
  },

  // Get a single memory by name
  async getByName(namespace: string, name: string): Promise<Memory | null> {
    try {
      const response = await apiClient.get<MemoryDetailResponse>(`/api/v1/namespaces/${namespace}/memories/${name}`)
      return {
        ...response,
        id: response.name // Use name as id for UI compatibility
      }
    } catch (error) {
      if ((error as AxiosError).response?.status === 404) {
        return null
      }
      throw error
    }
  },

  // Get a single memory by ID (for UI compatibility - ID is actually the name)
  async getById(namespace: string, id: number | string): Promise<Memory | null> {
    // Convert numeric ID to string name
    const name = String(id)
    return memoriesService.getByName(namespace, name)
  },

  // Create a new memory
  async create(namespace: string, memory: MemoryCreateRequest): Promise<Memory> {
    const response = await apiClient.post<MemoryDetailResponse>(`/api/v1/namespaces/${namespace}/memories`, memory)
    return {
      ...response,
      id: response.name
    }
  },

  // Update an existing memory
  async update(namespace: string, name: string, updates: MemoryUpdateRequest): Promise<Memory | null> {
    try {
      const response = await apiClient.put<MemoryDetailResponse>(`/api/v1/namespaces/${namespace}/memories/${name}`, updates)
      return {
        ...response,
        id: response.name
      }
    } catch (error) {
      if ((error as AxiosError).response?.status === 404) {
        return null
      }
      throw error
    }
  },

  // Update by ID (for UI compatibility)
  async updateById(namespace: string, id: number | string, updates: MemoryUpdateRequest): Promise<Memory | null> {
    const name = String(id)
    return memoriesService.update(namespace, name, updates)
  },

  // Delete a memory
  async delete(namespace: string, name: string): Promise<boolean> {
    try {
      await apiClient.delete(`/api/v1/namespaces/${namespace}/memories/${name}`)
      return true
    } catch (error) {
      if ((error as AxiosError).response?.status === 404) {
        return false
      }
      throw error
    }
  },

  // Delete by ID (for UI compatibility)
  async deleteById(namespace: string, id: number | string): Promise<boolean> {
    const name = String(id)
    return memoriesService.delete(namespace, name)
  }
}