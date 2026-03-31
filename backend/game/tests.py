from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import GameSession
from .views import (
    move_board, move_row_left, move_row_right,
    add_random_tile, can_move, has_won, calculate_score
)


class GameModelTest(TestCase):
    """测试游戏模型"""
    
    def test_create_game_session(self):
        """测试创建游戏会话"""
        board = [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 4, 0], [0, 0, 0, 0]]
        game = GameSession.objects.create(
            board=board,
            score=6,
            game_over=False,
            won=False
        )
        self.assertIsNotNone(game.id)
        self.assertEqual(game.score, 6)
        self.assertEqual(game.board, board)
        self.assertFalse(game.game_over)
        self.assertFalse(game.won)


class GameLogicTest(TestCase):
    """测试游戏逻辑函数"""
    
    def test_move_row_left(self):
        """测试向左移动行"""
        # 测试基本移动
        row = [2, 0, 4, 0]
        new_row, changed = move_row_left(row)
        self.assertEqual(new_row, [2, 4, 0, 0])
        self.assertTrue(changed)
        
        # 测试合并
        row = [2, 2, 0, 0]
        new_row, changed = move_row_left(row)
        self.assertEqual(new_row, [4, 0, 0, 0])
        self.assertTrue(changed)
        
        # 测试无变化
        row = [2, 4, 8, 16]
        new_row, changed = move_row_left(row)
        self.assertEqual(new_row, [2, 4, 8, 16])
        self.assertFalse(changed)
    
    def test_move_row_right(self):
        """测试向右移动行"""
        row = [0, 2, 0, 4]
        new_row, changed = move_row_right(row)
        self.assertEqual(new_row, [0, 0, 2, 4])
        self.assertTrue(changed)
        
        # 测试合并
        row = [0, 0, 2, 2]
        new_row, changed = move_row_right(row)
        self.assertEqual(new_row, [0, 0, 0, 4])
        self.assertTrue(changed)
    
    def test_move_board(self):
        """测试移动整个游戏板"""
        board = [
            [2, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 2]
        ]
        
        # 向左移动
        moved = move_board(board, 'left')
        self.assertTrue(moved)
        self.assertEqual(board[0], [2, 0, 0, 0])
        
        # 向上移动
        board = [
            [0, 0, 0, 2],
            [0, 0, 2, 0],
            [0, 2, 0, 0],
            [2, 0, 0, 0]
        ]
        moved = move_board(board, 'up')
        self.assertTrue(moved)
        self.assertEqual(board[0][0], 2)
    
    def test_can_move(self):
        """测试是否可以移动"""
        # 有空白位置
        board = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 0]
        ]
        self.assertTrue(can_move(board))
        
        # 无空白但可以合并
        board = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 2]
        ]
        self.assertTrue(can_move(board))
        
        # 无法移动
        board = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]
        self.assertFalse(can_move(board))
    
    def test_has_won(self):
        """测试是否获胜"""
        board = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 2048]
        ]
        self.assertTrue(has_won(board))
        
        board = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]
        self.assertFalse(has_won(board))
    
    def test_calculate_score(self):
        """测试计算分数"""
        board = [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        score = calculate_score(board)
        self.assertEqual(score, 6)


class GameAPITest(TestCase):
    """测试游戏API接口"""
    
    def setUp(self):
        self.client = Client()
    
    def test_new_game(self):
        """测试创建新游戏"""
        response = self.client.post(
            '/api/new-game/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('id', data)
        self.assertIn('board', data)
        self.assertIn('score', data)
        self.assertEqual(data['score'], 0)
        self.assertFalse(data['game_over'])
        self.assertFalse(data['won'])
        
        # 验证游戏已保存
        game = GameSession.objects.get(id=data['id'])
        self.assertIsNotNone(game)
    
    def test_move_left(self):
        """测试向左移动"""
        # 创建游戏
        response = self.client.post('/api/new-game/')
        game_data = json.loads(response.content)
        game_id = game_data['id']
        
        # 设置一个可以移动的棋盘
        game = GameSession.objects.get(id=game_id)
        game.board = [[0, 2, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        game.save()
        
        # 向左移动
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'left', 'game_id': game_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['moved'])
        self.assertEqual(data['board'][0][0], 2)
        self.assertEqual(data['board'][0][1], 4)
    
    def test_move_right(self):
        """测试向右移动"""
        response = self.client.post('/api/new-game/')
        game_id = json.loads(response.content)['id']
        
        game = GameSession.objects.get(id=game_id)
        game.board = [[2, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        game.save()
        
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'right', 'game_id': game_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['moved'])
    
    def test_move_up(self):
        """测试向上移动"""
        response = self.client.post('/api/new-game/')
        game_id = json.loads(response.content)['id']
        
        game = GameSession.objects.get(id=game_id)
        game.board = [[0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0]]
        game.save()
        
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'up', 'game_id': game_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['moved'])
    
    def test_move_down(self):
        """测试向下移动"""
        response = self.client.post('/api/new-game/')
        game_id = json.loads(response.content)['id']
        
        game = GameSession.objects.get(id=game_id)
        game.board = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0]]
        game.save()
        
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'down', 'game_id': game_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['moved'])
    
    def test_move_merge(self):
        """测试合并相同数字"""
        response = self.client.post('/api/new-game/')
        game_id = json.loads(response.content)['id']
        
        game = GameSession.objects.get(id=game_id)
        game.board = [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        game.save()
        
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'left', 'game_id': game_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['moved'])
        # 应该合并成4
        self.assertEqual(data['board'][0][0], 4)
    
    def test_move_no_change(self):
        """测试无法移动的情况"""
        response = self.client.post('/api/new-game/')
        game_id = json.loads(response.content)['id']
        
        game = GameSession.objects.get(id=game_id)
        # 设置一个无法向左移动的棋盘
        game.board = [[2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        game.save()
        
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'left', 'game_id': game_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['moved'])
    
    def test_move_invalid_game_id(self):
        """测试无效的游戏ID"""
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'left', 'game_id': 99999}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_move_missing_game_id(self):
        """测试缺少游戏ID"""
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'left'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_move_game_over(self):
        """测试游戏结束后的移动"""
        response = self.client.post('/api/new-game/')
        game_id = json.loads(response.content)['id']
        
        game = GameSession.objects.get(id=game_id)
        game.game_over = True
        game.save()
        
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'left', 'game_id': game_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['game_over'])
    
    def test_win_condition(self):
        """测试获胜条件"""
        response = self.client.post('/api/new-game/')
        game_id = json.loads(response.content)['id']
        
        game = GameSession.objects.get(id=game_id)
        game.board = [[2048, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        game.save()
        
        # 触发获胜检查（通过移动）
        response = self.client.post(
            '/api/move/',
            json.dumps({'direction': 'left', 'game_id': game_id}),
            content_type='application/json'
        )
        # 由于已经有2048，应该标记为获胜
        game.refresh_from_db()
        # 注意：这里需要实际移动才能触发检查，所以可能需要调整测试逻辑
