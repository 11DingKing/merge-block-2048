import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import Game2048 from '../src/components/Game2048.vue'
import { gameApi } from '../src/api/gameApi'

// Mock gameApi
vi.mock('../src/api/gameApi', () => ({
  gameApi: {
    newGame: vi.fn(),
    move: vi.fn()
  }
}))

// Mock useToast
vi.mock('../src/composables/useToast', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
    warning: vi.fn()
  })
}))

describe('Game2048 Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    
    gameApi.newGame.mockResolvedValue({
      id: 1,
      board: [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 4, 0], [0, 0, 0, 0]],
      score: 6,
      best_score: 0,
      game_over: false,
      won: false
    })
  })

  it('应该正确渲染组件', async () => {
    const wrapper = mount(Game2048)
    await nextTick()
    
    expect(wrapper.find('.game-title').exists()).toBe(true)
    expect(wrapper.find('.score-box').exists()).toBe(true)
    expect(wrapper.find('.game-container').exists()).toBe(true)
  })

  it('应该在挂载时创建新游戏', async () => {
    mount(Game2048)
    await nextTick()
    
    expect(gameApi.newGame).toHaveBeenCalled()
  })

  it('应该显示分数', async () => {
    const wrapper = mount(Game2048)
    await nextTick()
    
    const scoreValue = wrapper.find('.score-value')
    expect(scoreValue.exists()).toBe(true)
  })

  it('应该处理键盘输入', async () => {
    const wrapper = mount(Game2048)
    await nextTick()
    
    gameApi.move.mockResolvedValue({
      board: [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
      score: 6,
      best_score: 6,
      game_over: false,
      won: false,
      moved: true
    })
    
    // 模拟键盘事件
    const event = new KeyboardEvent('keydown', { key: 'ArrowLeft' })
    document.dispatchEvent(event)
    
    await nextTick()
    
    // 等待API调用
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(gameApi.move).toHaveBeenCalledWith('left', 1)
  })

  it('应该处理游戏结束状态', async () => {
    gameApi.newGame.mockResolvedValue({
      id: 1,
      board: [[2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64], [16, 32, 64, 128]],
      score: 510,
      best_score: 510,
      game_over: true,
      won: false
    })
    
    const wrapper = mount(Game2048)
    await nextTick()
    
    expect(wrapper.vm.gameOver).toBe(true)
  })

  it('应该处理获胜状态', async () => {
    gameApi.newGame.mockResolvedValue({
      id: 1,
      board: [[2048, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
      score: 2048,
      best_score: 2048,
      game_over: false,
      won: true
    })
    
    const wrapper = mount(Game2048)
    await nextTick()
    
    expect(wrapper.vm.won).toBe(true)
  })

  it('应该显示新游戏按钮', async () => {
    const wrapper = mount(Game2048)
    await nextTick()
    
    const newGameButton = wrapper.find('.btn-new-game')
    expect(newGameButton.exists()).toBe(true)
  })

  it('应该在新游戏按钮点击时创建新游戏', async () => {
    const wrapper = mount(Game2048)
    await nextTick()
    
    vi.clearAllMocks()
    
    const newGameButton = wrapper.find('.btn-new-game')
    await newGameButton.trigger('click')
    
    await nextTick()
    
    expect(gameApi.newGame).toHaveBeenCalled()
  })
})
