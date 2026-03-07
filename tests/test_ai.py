# tests/test_ai.py
import pytest
from unittest.mock import patch, MagicMock
from logic.board import ChessBoard
from logic.pieces import Rook, Pawn, King
from logic.ai_logic import ChessAI
import sys

# ป้องกันไม่ให้ AI พยายามดึงความยากจาก Kivy App ตอนรันเทส (ถ้าไม่มี Kivy หรือไม่อยาก mock ยาว)
class MockApp:
    def getattr(self, name, default):
        return 'normal'

class TestAILogic:
    """หมวดทดสอบระบบบอท (AI Logic System)"""

    @patch('logic.ai_logic.App')
    def test_ai_random_move(self, mock_app):
        """เทสที่ 1: ตรวจสอบว่าพิกัดที่บอทเลือกเดินเป็น Legal Move จริงหรือไม่"""
        # ตั้งค่าให้บอทในเทสนี้เป็นระดับ normal เสมอ
        mock_instance = MagicMock()
        mock_instance.ai_difficulty = 'normal'
        mock_app.get_running_app.return_value = mock_instance
        
        board = ChessBoard()
        board.board = [[None for _ in range(8)] for _ in range(8)]
        
        # วางหมากดำ (บอท) แค่ 1 ตัว
        bot_pawn = Pawn('black')
        board.board[1][4] = bot_pawn
        board.current_turn = 'black'
        
        # เรียก AI ให้คิดตาเดิน
        best_move = ChessAI.get_best_move(board, ai_color='black')
        
        assert best_move is not None
        start_pos, end_pos = best_move
        
        # คาดหวังว่าบอทจะเลือกเดิน Pawn ดำตัวนี้เท่านั้น
        assert start_pos == (1, 4)
        
        # คาดหวังว่าจุดจบต้องเป็น Legal Move ของมัน (เช่น 2,4 หรือ 3,4)
        legal_moves = board.get_legal_moves(start_pos)
        assert end_pos in legal_moves

    @patch('logic.ai_logic.App')
    def test_ai_capture_priority(self, mock_app):
        """เทสที่ 2: ถ้ามีโอกาสกินหมากฝ่ายตรงข้าม (สีขาว) บอทต้องเลือกเดินไปกินหมากตัวนั้น (Priority)"""
        mock_instance = MagicMock()
        mock_instance.ai_difficulty = 'normal' # normal จะสนใจคะแนนการกิน
        mock_app.get_running_app.return_value = mock_instance
        
        board = ChessBoard()
        board.board = [[None for _ in range(8)] for _ in range(8)]
        
        bot_rook = Rook('black')
        board.board[3][4] = bot_rook
        board.current_turn = 'black'
        
        # วางหมากศัตรู (ม้าขาว) ไว้ให้กินที่ 3,2 (แนวตรง)
        white_knight = Pawn('white') # ให้แต้ม 10 หรือ Rook กินได้
        board.board[3][2] = white_knight
        
        # เรียก AI ให้คิดตาเดิน
        best_move = ChessAI.get_best_move(board, ai_color='black')
        
        # AI ควรเลือกเดินไปกินชัวร์ๆ (เว้นแต่จะมีการเดินไปกลางกระดานได้แต้มมากกว่า แต่นี่กินได้แต้มแน่ๆ)
        # คะแนนปกติเดินกลางได้ 5 แต้ม แต่กินหมากได้ 100 แต้มขึ้นไป
        start_pos, end_pos = best_move
        assert start_pos == (3, 4)
        assert end_pos == (3, 2)

    @patch('logic.ai_logic.App')
    def test_ai_boundary_check(self, mock_app):
        """เทสที่ 3: ตรวจสอบว่าบอทจะไม่พยายามเดินหมากออกนอกขอบกระดาน (0-7, 0-7)"""
        mock_instance = MagicMock()
        mock_instance.ai_difficulty = 'normal'
        mock_app.get_running_app.return_value = mock_instance
        
        board = ChessBoard()
        board.board = [[None for _ in range(8)] for _ in range(8)]
        
        # วาง King ดำที่มุมขอบกระดาน (0,0)
        bot_king = King('black')
        board.board[0][0] = bot_king
        board.current_turn = 'black'
        
        best_move = ChessAI.get_best_move(board, ai_color='black')
        
        assert best_move is not None
        start_pos, end_pos = best_move
        er, ec = end_pos
        
        # ต้องไม่เดินออกไปข้างนอกพิกัด 0-7
        assert 0 <= er <= 7
        assert 0 <= ec <= 7
