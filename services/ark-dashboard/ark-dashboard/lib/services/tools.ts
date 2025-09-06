import { apiClient } from '@/lib/api/client'

// Tool interface for UI compatibility
export interface Tool {
  id: string
  name: string
  type?: string
  description?: string
  annotations?: unknown
  labels?: unknown
}

// Tool detail response with schema
export interface ToolDetail {
  name: string
  namespace: string
  description?: string
  labels?: Record<string, string>
  annotations?: Record<string, string>
  spec?: {
    inputSchema?: Record<string, unknown>
    [key: string]: unknown
  }
  status?: Record<string, unknown>
}

// Tool list response
interface ToolListResponse {
  items: Tool[]
  count: number
}

// Service for tool operations
export const toolsService = {
  // Get all tools in a namespace
  async getAll(namespace: string): Promise<Tool[]> {
    const response = await apiClient.get<ToolListResponse>(`/api/v1/namespaces/${namespace}/tools`)
    return response.items.map(item => ({ ...item, id: item.name }))
  },

  // Get detailed tool information including schema
  async getDetail(namespace: string, toolName: string): Promise<ToolDetail> {
    const response = await apiClient.get<ToolDetail>(`/api/v1/namespaces/${namespace}/tools/${toolName}`)
    return response
  },

  // Delete a tool
  async delete(namespace: string, identifier: string): Promise<void> {
    await apiClient.delete(`/api/v1/namespaces/${namespace}/tools/${identifier}`)
  }
}