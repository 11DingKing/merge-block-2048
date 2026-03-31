import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useToast } from '../src/composables/useToast'

describe('useToast', () => {
  beforeEach(() => {
    // 重置toasts数组
    const { toasts } = useToast()
    toasts.value = []
  })

  it('应该能够显示toast', () => {
    const toast = useToast()
    const id = toast.show('测试消息', 'info', 1000)
    
    expect(id).toBeDefined()
    expect(toast.toasts.value.length).toBe(1)
    expect(toast.toasts.value[0].message).toBe('测试消息')
    expect(toast.toasts.value[0].type).toBe('info')
  })

  it('应该能够显示不同类型的toast', () => {
    const toast = useToast()
    
    toast.success('成功消息')
    toast.error('错误消息')
    toast.info('信息消息')
    toast.warning('警告消息')
    
    expect(toast.toasts.value.length).toBe(4)
    expect(toast.toasts.value[0].type).toBe('success')
    expect(toast.toasts.value[1].type).toBe('error')
    expect(toast.toasts.value[2].type).toBe('info')
    expect(toast.toasts.value[3].type).toBe('warning')
  })

  it('应该能够移除toast', () => {
    const toast = useToast()
    const id = toast.show('测试消息')
    
    expect(toast.toasts.value.length).toBe(1)
    
    toast.remove(id)
    
    expect(toast.toasts.value.length).toBe(0)
  })

  it('应该自动移除toast', async () => {
    vi.useFakeTimers()
    
    const toast = useToast()
    toast.show('测试消息', 'info', 1000)
    
    expect(toast.toasts.value.length).toBe(1)
    
    vi.advanceTimersByTime(1000)
    
    expect(toast.toasts.value.length).toBe(0)
    
    vi.useRealTimers()
  })
})
