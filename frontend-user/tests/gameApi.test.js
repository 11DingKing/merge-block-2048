import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { gameApi } from '../src/api/gameApi'

// Mock axios
vi.mock('axios')

describe('Game API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('newGame', () => {
    it('应该成功创建新游戏', async () => {
      const mockResponse = {
        data: {
          id: 1,
          board: [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 4, 0], [0, 0, 0, 0]],
          score: 6,
          best_score: 0,
          game_over: false,
          won: false
        }
      }

      axios.create.mockReturnValue({
        post: vi.fn().mockResolvedValue(mockResponse)
      })

      const result = await gameApi.newGame()

      expect(result).toEqual(mockResponse.data)
      expect(result.id).toBe(1)
      expect(result.board).toHaveLength(4)
      expect(result.score).toBe(6)
    })

    it('应该处理创建游戏失败的情况', async () => {
      const mockError = new Error('Network Error')
      axios.create.mockReturnValue({
        post: vi.fn().mockRejectedValue(mockError)
      })

      await expect(gameApi.newGame()).rejects.toThrow('Network Error')
    })
  })

  describe('move', () => {
    it('应该成功执行移动操作', async () => {
      const mockResponse = {
        data: {
          board: [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          score: 6,
          best_score: 6,
          game_over: false,
          won: false,
          moved: true
        }
      }

      const mockPost = vi.fn().mockResolvedValue(mockResponse)
      axios.create.mockReturnValue({
        post: mockPost
      })

      const result = await gameApi.move('left', 1)

      expect(result).toEqual(mockResponse.data)
      expect(result.moved).toBe(true)
      expect(mockPost).toHaveBeenCalledWith('/api/move/', {
        direction: 'left',
        game_id: 1
      })
    })

    it('应该处理无法移动的情况', async () => {
      const mockResponse = {
        data: {
          board: [[2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          score: 30,
          best_score: 30,
          game_over: false,
          won: false,
          moved: false
        }
      }

      const mockPost = vi.fn().mockResolvedValue(mockResponse)
      axios.create.mockReturnValue({
        post: mockPost
      })

      const result = await gameApi.move('left', 1)

      expect(result.moved).toBe(false)
    })

    it('应该处理移动失败的情况', async () => {
      const mockError = new Error('Game not found')
      axios.create.mockReturnValue({
        post: vi.fn().mockRejectedValue(mockError)
      })

      await expect(gameApi.move('left', 999)).rejects.toThrow('Game not found')
    })

    it('应该支持所有方向', async () => {
      const directions = ['up', 'down', 'left', 'right']
      const mockPost = vi.fn().mockResolvedValue({
        data: {
          board: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          score: 0,
          best_score: 0,
          game_over: false,
          won: false,
          moved: true
        }
      })

      axios.create.mockReturnValue({
        post: mockPost
      })

      for (const direction of directions) {
        await gameApi.move(direction, 1)
        expect(mockPost).toHaveBeenCalledWith('/api/move/', {
          direction,
          game_id: 1
        })
      }
    })
  })

  describe('undo', () => {
    it('应该成功撤销上一步操作', async () => {
      const mockResponse = {
        data: {
          board: [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          score: 0,
          best_score: 10,
          game_over: false,
          won: false,
          success: true
        }
      }

      const mockPost = vi.fn().mockResolvedValue(mockResponse)
      axios.create.mockReturnValue({
        post: mockPost
      })

      const result = await gameApi.undo(1)

      expect(result).toEqual(mockResponse.data)
      expect(result.success).toBe(true)
      expect(mockPost).toHaveBeenCalledWith('/api/undo/', {
        game_id: 1
      })
    })

    it('应该处理撤销不可用的情况', async () => {
      const mockResponse = {
        data: {
          board: [[2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
          score: 30,
          best_score: 30,
          game_over: false,
          won: false,
          success: false
        }
      }

      const mockPost = vi.fn().mockResolvedValue(mockResponse)
      axios.create.mockReturnValue({
        post: mockPost
      })

      const result = await gameApi.undo(1)

      expect(result.success).toBe(false)
    })

    it('应该处理撤销失败的情况', async () => {
      const mockError = new Error('Undo failed')
      axios.create.mockReturnValue({
        post: vi.fn().mockRejectedValue(mockError)
      })

      await expect(gameApi.undo(999)).rejects.toThrow('Undo failed')
    })
  })
})
