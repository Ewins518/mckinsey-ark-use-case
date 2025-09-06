import { apiClient } from '@/lib/api/client'
import type { components } from '@/lib/api/generated/types'

// Helper type for axios errors
interface AxiosError extends Error {
  response?: {
    status: number
  }
}

// Use the generated types from OpenAPI
export type ModelResponse = components['schemas']['ModelResponse']
export type ModelDetailResponse = components['schemas']['ModelDetailResponse']
export type ModelListResponse = components['schemas']['ModelListResponse']
export type ModelCreateRequest = components['schemas']['ModelCreateRequest']
export type ModelUpdateRequest = components['schemas']['ModelUpdateRequest']

// For UI compatibility, we'll map the API response to include an id field
export type Model = ModelDetailResponse & { id: string }

// CRUD Operations
export const modelsService = {
  // Get all models
  async getAll(namespace: string): Promise<Model[]> {
    const response = await apiClient.get<ModelListResponse>(`/api/v1/namespaces/${namespace}/models`)
    
    // Map the response items to include id for UI compatibility
    const models = await Promise.all(
      response.items.map(async (item) => {
        // Fetch detailed info for each model to get full data
        const detailed = await modelsService.getByName(namespace, item.name)
        return detailed!
      })
    )
    
    return models
  },

  // Get a single model by name
  async getByName(namespace: string, name: string): Promise<Model | null> {
    try {
      const response = await apiClient.get<ModelDetailResponse>(`/api/v1/namespaces/${namespace}/models/${name}`)
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

  // Get a single model by ID (for UI compatibility - ID is actually the name)
  async getById(namespace: string, id: number | string): Promise<Model | null> {
    // Convert numeric ID to string name
    const name = String(id)
    return modelsService.getByName(namespace, name)
  },

  // Create a new model
  async create(namespace: string, model: ModelCreateRequest): Promise<Model> {
    const response = await apiClient.post<ModelDetailResponse>(`/api/v1/namespaces/${namespace}/models`, model)
    return {
      ...response,
      id: response.name
    }
  },

  // Update an existing model
  async update(namespace: string, name: string, updates: ModelUpdateRequest): Promise<Model | null> {
    try {
      const response = await apiClient.put<ModelDetailResponse>(`/api/v1/namespaces/${namespace}/models/${name}`, updates)
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
  async updateById(namespace: string, id: number | string, updates: ModelUpdateRequest): Promise<Model | null> {
    const name = String(id)
    return modelsService.update(namespace, name, updates)
  },

  // Delete a model
  async delete(namespace: string, name: string): Promise<boolean> {
    try {
      await apiClient.delete(`/api/v1/namespaces/${namespace}/models/${name}`)
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
    return modelsService.delete(namespace, name)
  }
}