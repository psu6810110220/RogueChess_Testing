# tests/test_board.py
import pytest
from unittest.mock import patch
from logic.board import ChessBoard
from logic.pieces import King, Queen, Rook, Knight, Pawn

class TestBoardBasics:
    
    def test_board_initialization(self):
        """เทสที่ 1: ตรวจสอบการตั้งค่าเริ่มต้นของกระดาน (Basic Test)"""
        board = ChessBoard()
        assert board.current_turn == 'white'
        assert isinstance(board.board[0][4], King)
        assert board.board[0][4].color == 'black'
        assert isinstance(board.board[7][4], King)
        assert board.board[7][4].color == 'white'
        assert len(board.inventory_white) == 0
        assert len(board.inventory_black) == 0

    def test_turn_switching(self):
        """เทสที่ 2: ตรวจสอบการสลับเทิร์น"""
        board = ChessBoard()
        assert board.current_turn == 'white'
        board.complete_turn()
        assert board.current_turn == 'black'

    def test_is_in_check(self):
        """เทสที่ 3: ระบบรุกฆาต (Check)"""
        board = ChessBoard()
        board.board = [[None for _ in range(8)] for _ in range(8)]
        board.board[0][0] = King('white')
        board.board[0][7] = Rook('black') 
        assert board.is_in_check('white') == True
        assert board.is_in_check('black') == False

    def test_check_insufficient_material(self):
        """เทสที่ 4: กฎหมากไม่พอรุกฆาต = เสมอ (Draw)"""
        board = ChessBoard()
        board.board = [[None for _ in range(8)] for _ in range(8)]
        
        board.board[0][0] = King('white')
        board.board[7][7] = King('black')
        assert board.check_insufficient_material() == True
        
        board.board[2][2] = Queen('black')
        assert board.check_insufficient_material() == False

    # 🌟 [คะแนนพิเศษ Stub] จำลองล็อกผลลัพธ์การสุ่ม (Random) 🌟
    @patch('logic.board.random.randint')
    def test_handle_item_drop_stub(self, mock_randint):
        """เทสที่ 5: Stub ล็อกการสุ่มไอเทม 100%"""
        # ✨ 1. บังคับ randint ให้สุ่มได้ไอเทม ID 1 เสมอ
        mock_randint.return_value = 1
        
        # 2. สร้างกระดาน
        board = ChessBoard()
        
        # 3. จำลองให้ Knight ฝ่ายขาว (ฝ่ายรุก) เป็นผู้ชนะการปะทะ
        # (ฟังก์ชันรับพารามิเตอร์: winner, is_defender=False)
        winner = Knight('white')
        board.handle_item_drop(winner, is_defender=False)
        
        # 4. เช็คผลลัพธ์ว่าไอเทมเข้ากระเป๋าและเป็น ID 1 ตามที่จำลองไว้
        assert len(board.inventory_white) == 1
        assert board.inventory_white[0].id == 1