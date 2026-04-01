import json
import random
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameSession

logger = logging.getLogger(__name__)


@csrf_exempt
def new_game(request):
    """创建新游戏"""
    logger.info("Creating new game")
    board = [[0] * 4 for _ in range(4)]
    # 随机生成两个初始数字
    add_random_tile(board)
    add_random_tile(board)
    
    game = GameSession.objects.create(
        board=board,
        score=0,
        game_over=False,
        won=False,
        previous_board=[],
        previous_score=0,
        can_undo=False
    )
    
    logger.info(f"New game created with id={game.id}")
    return JsonResponse({
        'id': game.id,
        'board': board,
        'score': game.score,
        'best_score': game.best_score,
        'game_over': game.game_over,
        'won': game.won,
        'can_undo': game.can_undo
    })


@csrf_exempt
def move(request):
    """处理移动操作"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        direction = data.get('direction')  # 'up', 'down', 'left', 'right'
        game_id = data.get('game_id')
        
        if not game_id:
            return JsonResponse({'error': 'game_id required'}, status=400)
        
        try:
            game = GameSession.objects.get(id=game_id)
        except GameSession.DoesNotExist:
            logger.warning(f"Game not found: id={game_id}")
            return JsonResponse({'error': 'Game not found'}, status=404)
        
        if game.game_over:
            return JsonResponse({
                'board': game.board,
                'score': game.score,
                'game_over': True,
                'won': game.won,
                'can_undo': game.can_undo
            })
        
        board = [row[:] for row in game.board]  # 深拷贝
        old_board = [row[:] for row in board]
        old_score = game.score
        
        # 执行移动
        moved, score_gained = move_board(board, direction)
        
        if moved:
            # 只有还没有撤销过才能保存上一步状态
            if not game.can_undo:
                game.previous_board = [row[:] for row in old_board]
                game.previous_score = old_score
                game.can_undo = True
            
            # 添加新数字
            add_random_tile(board)
            game.board = board
            game.score += score_gained  # 累加得分
            
            # 更新最高分
            if game.score > game.best_score:
                game.best_score = game.score
            
            # 检查是否获胜
            if not game.won and has_won(board):
                game.won = True
            
            # 检查游戏是否结束
            if not can_move(board):
                game.game_over = True
            
            game.save()
            logger.info(f"Game {game_id}: moved {direction}, score={game.score}, game_over={game.game_over}, won={game.won}")
        
        return JsonResponse({
            'board': board,
            'score': game.score,
            'best_score': game.best_score,
            'game_over': game.game_over,
            'won': game.won,
            'moved': moved,
            'can_undo': game.can_undo
        })
    
    except Exception as e:
        logger.exception(f"Error processing move for game {game_id}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def move_board(board, direction):
    """移动游戏板，返回 (是否移动, 本次得分)"""
    moved = False
    score_gained = 0
    
    if direction == 'left':
        for i in range(4):
            row, changed, points = move_row_left(board[i])
            board[i] = row
            score_gained += points
            if changed:
                moved = True
    elif direction == 'right':
        for i in range(4):
            row, changed, points = move_row_right(board[i])
            board[i] = row
            score_gained += points
            if changed:
                moved = True
    elif direction == 'up':
        for j in range(4):
            col = [board[i][j] for i in range(4)]
            new_col, changed, points = move_row_left(col)
            score_gained += points
            if changed:
                moved = True
                for i in range(4):
                    board[i][j] = new_col[i]
    elif direction == 'down':
        for j in range(4):
            col = [board[i][j] for i in range(4)]
            new_col, changed, points = move_row_right(col)
            score_gained += points
            if changed:
                moved = True
                for i in range(4):
                    board[i][j] = new_col[i]
    
    return moved, score_gained


def move_row_left(row):
    """向左移动一行，返回 (新行, 是否变化, 得分)"""
    original_row = row[:]
    new_row = [x for x in row if x != 0]
    changed = False
    score = 0
    
    # 合并相同的数字
    i = 0
    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            score += new_row[i]  # 合并得分
            new_row.pop(i + 1)
            changed = True
        i += 1
    
    # 填充零
    while len(new_row) < 4:
        new_row.append(0)
    
    if not changed:
        changed = new_row != original_row
    
    return new_row, changed, score


def move_row_right(row):
    """向右移动一行"""
    reversed_row = row[::-1]
    new_row, changed, score = move_row_left(reversed_row)
    return new_row[::-1], changed, score


def add_random_tile(board):
    """在空白位置随机添加2或4"""
    empty_cells = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4


def can_move(board):
    """检查是否还能移动"""
    # 检查是否有空白位置
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return True
    
    # 检查是否有可以合并的相邻数字
    for i in range(4):
        for j in range(4):
            current = board[i][j]
            # 检查右边
            if j < 3 and board[i][j + 1] == current:
                return True
            # 检查下边
            if i < 3 and board[i + 1][j] == current:
                return True
    
    return False


def has_won(board):
    """检查是否达到2048"""
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:
                return True
    return False


@csrf_exempt
def undo(request):
    """处理撤销操作"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        game_id = data.get('game_id')
        
        if not game_id:
            return JsonResponse({'error': 'game_id required'}, status=400)
        
        try:
            game = GameSession.objects.get(id=game_id)
        except GameSession.DoesNotExist:
            logger.warning(f"Game not found: id={game_id}")
            return JsonResponse({'error': 'Game not found'}, status=404)
        
        if not game.can_undo:
            return JsonResponse({
                'error': 'Cannot undo',
                'board': game.board,
                'score': game.score,
                'best_score': game.best_score,
                'game_over': game.game_over,
                'won': game.won,
                'can_undo': False
            }, status=400)
        
        # 执行撤销
        game.board = [row[:] for row in game.previous_board]
        game.score = game.previous_score
        game.can_undo = False
        game.game_over = False  # 撤销后游戏重新开始
        
        game.save()
        logger.info(f"Game {game_id}: undo successful")
        
        return JsonResponse({
            'board': game.board,
            'score': game.score,
            'best_score': game.best_score,
            'game_over': game.game_over,
            'won': game.won,
            'can_undo': False
        })
    
    except Exception as e:
        logger.exception(f"Error processing undo for game {game_id}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
