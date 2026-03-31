import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const gameApi = {
  /**
   * 创建新游戏
   * @returns {Promise<Object>} 新游戏的状态数据
   */
  async newGame() {
    const response = await api.post('/api/new-game/')
    return response.data
  },

  /**
   * 执行移动操作
   * @param {string} direction - 移动方向 ('up', 'down', 'left', 'right')
   * @param {number} gameId - 游戏会话ID
   * @returns {Promise<Object>} 移动后的游戏状态数据
   */
  async move(direction, gameId) {
    const response = await api.post('/api/move/', {
      direction: direction,
      game_id: gameId,
    })
    return response.data
  },

  /**
   * 撤销上一步操作
   * @param {number} gameId - 游戏会话ID
   * @returns {Promise<Object>} 撤销后的游戏状态数据
   */
  async undo(gameId) {
    const response = await api.post('/api/undo/', {
      game_id: gameId,
    })
    return response.data
  },
}
