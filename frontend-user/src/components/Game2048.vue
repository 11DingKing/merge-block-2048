<template>
  <div class="game">
    <!-- Header -->
    <header class="header">
      <h1 class="logo">2048</h1>
      <div class="scores">
        <div class="score-box">
          <span class="label">SCORE</span>
          <span class="value">{{ score }}</span>
        </div>
        <div class="score-box best">
          <span class="label">BEST</span>
          <span class="value">{{ bestScore }}</span>
        </div>
      </div>
    </header>

    <!-- Board -->
    <div class="board" ref="boardEl" :class="{ shake: shaking }">
      <div class="cells">
        <div v-for="i in 16" :key="i" class="cell"></div>
      </div>
      
      <div class="tiles">
        <div v-for="tile in tiles" :key="tile.id" class="tile"
             :class="[`t${tile.value}`, { pop: tile.isNew, merge: tile.merged, dragging: draggingTile?.id === tile.id }]"
             :style="getTileStyle(tile)"
             @mousedown.prevent="startDrag($event, tile)"
             @touchstart.prevent="startDrag($event, tile)">
          {{ tile.value }}
        </div>
      </div>

      <!-- Drag indicator -->
      <div v-if="dragDirection" class="drag-indicator" :class="dragDirection">
        <span class="arrow">{{ directionArrow }}</span>
      </div>

      <!-- Score popup -->
      <transition name="score-pop">
        <div v-if="scoreAdd > 0" class="score-popup" :key="scoreKey">+{{ scoreAdd }}</div>
      </transition>

      <!-- Overlay -->
      <div v-if="showOverlay" class="overlay" :class="{ win: won }">
        <div class="overlay-box">
          <span class="emoji">{{ won ? '🎉' : '😢' }}</span>
          <span class="text">{{ won ? 'You Win!' : 'Game Over' }}</span>
          <button @click.stop="startGame">Play Again</button>
        </div>
      </div>
    </div>

    <div class="button-group">
      <button class="new-btn" @click="startGame">🔄 New Game</button>
      <button class="undo-btn" @click="undo" :disabled="!canUndo">↩️ Undo</button>
    </div>
    
    <p class="hint">💡 拖拽任意方块滑动，合并相同数字</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { gameApi } from '../api/gameApi'
import { useToast } from '../composables/useToast'

const toast = useToast()
const boardEl = ref(null)

const score = ref(0)
const bestScore = ref(0)
const gameOver = ref(false)
const won = ref(false)
const showOverlay = ref(false)
const gameId = ref(null)
const tiles = ref([])
const shaking = ref(false)
const scoreAdd = ref(0)
const scoreKey = ref(0)
const canUndo = ref(false)

// Drag state
const draggingTile = ref(null)
const dragOffset = ref({ x: 0, y: 0 })
const dragStart = ref({ x: 0, y: 0 })
const dragDirection = ref(null)

let uid = 0

const directionArrow = computed(() => {
  const arrows = { up: '↑', down: '↓', left: '←', right: '→' }
  return arrows[dragDirection.value] || ''
})

function getTileStyle(tile) {
  if (draggingTile.value?.id === tile.id) {
    return {
      '--x': tile.col,
      '--y': tile.row,
      transform: `translate(calc(var(--x) * (var(--cell) + var(--gap)) + ${dragOffset.value.x}px), calc(var(--y) * (var(--cell) + var(--gap)) + ${dragOffset.value.y}px))`,
      zIndex: 100,
      transition: 'none'
    }
  }
  return { '--x': tile.col, '--y': tile.row }
}

function startDrag(e, tile) {
  if (gameOver.value) return
  
  const point = e.touches ? e.touches[0] : e
  draggingTile.value = tile
  dragStart.value = { x: point.clientX, y: point.clientY }
  dragOffset.value = { x: 0, y: 0 }
  dragDirection.value = null
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', endDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('touchend', endDrag)
}

function onDrag(e) {
  if (!draggingTile.value) return
  e.preventDefault()
  
  const point = e.touches ? e.touches[0] : e
  const dx = point.clientX - dragStart.value.x
  const dy = point.clientY - dragStart.value.y
  
  // Constrain to one direction
  if (Math.abs(dx) > Math.abs(dy)) {
    dragOffset.value = { x: dx, y: 0 }
    dragDirection.value = dx > 20 ? 'right' : dx < -20 ? 'left' : null
  } else {
    dragOffset.value = { x: 0, y: dy }
    dragDirection.value = dy > 20 ? 'down' : dy < -20 ? 'up' : null
  }
}

function endDrag() {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', endDrag)
  
  if (dragDirection.value) {
    move(dragDirection.value)
  }
  
  draggingTile.value = null
  dragOffset.value = { x: 0, y: 0 }
  dragDirection.value = null
}

function createTiles(board) {
  const arr = []
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (board[r][c]) {
        arr.push({ id: uid++, row: r, col: c, value: board[r][c], isNew: true, merged: false })
      }
    }
  }
  return arr
}

function updateTiles(board) {
  const oldTiles = [...tiles.value]
  const newTiles = []
  
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      if (board[r][c]) {
        const oldAtPos = oldTiles.filter(t => t.row === r && t.col === c)
        const wasMerged = oldAtPos.length > 0 && oldAtPos.every(t => t.value < board[r][c])
        const sameValue = oldTiles.find(t => t.value === board[r][c] && (t.row !== r || t.col !== c))
        const existing = oldTiles.find(t => t.row === r && t.col === c && t.value === board[r][c])
        
        newTiles.push({
          id: existing ? existing.id : uid++,
          row: r, col: c, value: board[r][c],
          isNew: !existing && !sameValue,
          merged: wasMerged || (!existing && sameValue && oldAtPos.length > 0)
        })
      }
    }
  }
  tiles.value = newTiles
}

async function startGame() {
  try {
    const res = await gameApi.newGame()
    gameId.value = res.id
    score.value = res.score
    bestScore.value = res.best_score
    gameOver.value = false
    won.value = false
    showOverlay.value = false
    scoreAdd.value = 0
    canUndo.value = res.canUndo
    tiles.value = createTiles(res.board)
  } catch {
    toast.error('Failed to start game')
  }
}

async function move(dir) {
  if (gameOver.value) return
  try {
    const oldScore = score.value
    const res = await gameApi.move(dir, gameId.value)
    if (res.moved) {
      const diff = res.score - oldScore
      if (diff > 0) {
        scoreAdd.value = diff
        scoreKey.value++
        shaking.value = true
        setTimeout(() => {
          scoreAdd.value = 0
          shaking.value = false
        }, 300)
      }
      
      score.value = res.score
      bestScore.value = res.best_score
      canUndo.value = res.canUndo
      updateTiles(res.board)
      if (res.won) won.value = true
      if (res.game_over) gameOver.value = true
      if (res.won || res.game_over) setTimeout(() => showOverlay.value = true, 200)
    }
  } catch {
    toast.error('Move failed')
  }
}

/**
 * 撤销上一步操作
 * 每局游戏只允许撤销一次
 */
async function undo() {
  if (!canUndo.value) return
  try {
    const res = await gameApi.undo(gameId.value)
    score.value = res.score
    bestScore.value = res.best_score
    canUndo.value = res.canUndo
    gameOver.value = res.game_over
    won.value = res.won
    showOverlay.value = false
    tiles.value = createTiles(res.board)
    toast.success('已撤销上一步操作')
  } catch {
    toast.error('撤销失败')
  }
}

onMounted(startGame)
</script>

<style scoped>
* { box-sizing: border-box; }

.game {
  width: 100vw;
  height: 100dvh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 16px;
  user-select: none;
}

.header {
  width: 100%;
  max-width: 400px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 48px;
  font-weight: 900;
  margin: 0;
  background: linear-gradient(90deg, #f39c12, #e74c3c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.scores { display: flex; gap: 10px; }

.score-box {
  background: rgba(255,255,255,0.1);
  padding: 8px 16px;
  border-radius: 8px;
  text-align: center;
}
.score-box.best { background: rgba(243,156,18,0.3); }
.score-box .label { display: block; font-size: 11px; color: #aaa; font-weight: 600; }
.score-box .value { display: block; font-size: 22px; color: #fff; font-weight: 800; }

.board {
  --size: min(90vw, 90vh - 160px, 400px);
  --gap: calc(var(--size) * 0.025);
  --cell: calc((var(--size) - var(--gap) * 5) / 4);
  width: var(--size);
  height: var(--size);
  background: rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: var(--gap);
  position: relative;
}

.board.shake { animation: shake 0.2s ease-out; }

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}

.cells {
  display: grid;
  grid-template-columns: repeat(4, var(--cell));
  gap: var(--gap);
}

.cell {
  width: var(--cell);
  height: var(--cell);
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
}

.tiles {
  position: absolute;
  top: var(--gap);
  left: var(--gap);
}

.tile {
  position: absolute;
  width: var(--cell);
  height: var(--cell);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: calc(var(--cell) * 0.45);
  font-weight: 800;
  cursor: grab;
  transform: translate(calc(var(--x) * (var(--cell) + var(--gap))), calc(var(--y) * (var(--cell) + var(--gap))));
  transition: transform 0.15s ease-out;
}

.tile.dragging {
  cursor: grabbing;
  box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  transform-origin: center;
}

.tile.pop { animation: pop 0.2s ease-out; }
.tile.merge { animation: merge 0.25s ease-out; }

@keyframes pop {
  0% { opacity: 0; scale: 0; }
  60% { scale: 1.2; }
  100% { opacity: 1; scale: 1; }
}

@keyframes merge {
  0% { scale: 1; }
  30% { scale: 1.3; }
  60% { scale: 0.95; }
  100% { scale: 1; }
}

/* Tile colors */
.t2 { background: linear-gradient(135deg, #ffeaa7, #fdcb6e); color: #6d4c00; }
.t4 { background: linear-gradient(135deg, #81ecec, #00cec9); color: #006266; }
.t8 { background: linear-gradient(135deg, #fd79a8, #e84393); color: #fff; }
.t16 { background: linear-gradient(135deg, #74b9ff, #0984e3); color: #fff; }
.t32 { background: linear-gradient(135deg, #55efc4, #00b894); color: #fff; }
.t64 { background: linear-gradient(135deg, #ff7675, #d63031); color: #fff; }
.t128 { background: linear-gradient(135deg, #a29bfe, #6c5ce7); color: #fff; font-size: calc(var(--cell) * 0.38); }
.t256 { background: linear-gradient(135deg, #ffeaa7, #f39c12); color: #fff; font-size: calc(var(--cell) * 0.38); }
.t512 { background: linear-gradient(135deg, #fd79a8, #c44569); color: #fff; font-size: calc(var(--cell) * 0.38); }
.t1024 { background: linear-gradient(135deg, #00cec9, #079992); color: #fff; font-size: calc(var(--cell) * 0.32); }
.t2048 { background: linear-gradient(135deg, #f39c12, #e74c3c); color: #fff; font-size: calc(var(--cell) * 0.32); box-shadow: 0 0 30px #f39c12; }
.t4096, .t8192 { background: linear-gradient(135deg, #2d3436, #000); color: #fff; font-size: calc(var(--cell) * 0.28); }

.drag-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 60px;
  color: rgba(255,255,255,0.3);
  pointer-events: none;
  z-index: 50;
}

.drag-indicator .arrow {
  display: block;
  animation: pulse 0.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

.score-popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 48px;
  font-weight: 900;
  color: #4ade80;
  text-shadow: 0 2px 10px rgba(74, 222, 128, 0.5);
  pointer-events: none;
  z-index: 10;
}

.score-pop-enter-active { animation: scorePop 0.5s ease-out forwards; }
.score-pop-leave-active { display: none; }

@keyframes scorePop {
  0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
  30% { opacity: 1; transform: translate(-50%, -70%) scale(1.2); }
  100% { opacity: 0; transform: translate(-50%, -100%) scale(1); }
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.85);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s;
  z-index: 100;
}
.overlay.win { background: rgba(243,156,18,0.9); }

@keyframes fadeIn { from { opacity: 0; } }

.overlay-box { text-align: center; }
.overlay-box .emoji { display: block; font-size: 56px; }
.overlay-box .text { display: block; font-size: 28px; font-weight: 800; color: #fff; margin: 10px 0 20px; }
.overlay-box button {
  background: #fff;
  color: #1a1a2e;
  border: none;
  padding: 12px 28px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
}

.button-group {
  display: flex;
  gap: 12px;
}

.new-btn {
  background: linear-gradient(90deg, #f39c12, #e74c3c);
  color: #fff;
  border: none;
  padding: 14px 28px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(243,156,18,0.4);
}

.undo-btn {
  background: linear-gradient(90deg, #6c5ce7, #a29bfe);
  color: #fff;
  border: none;
  padding: 14px 28px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
  transition: all 0.3s ease;
}

.undo-btn:disabled {
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.3);
  cursor: not-allowed;
  box-shadow: none;
}

.hint {
  color: rgba(255,255,255,0.5);
  font-size: 14px;
  margin: 0;
}
</style>
