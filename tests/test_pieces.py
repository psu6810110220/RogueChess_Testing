# tests/test_pieces.py
import pytest
from logic.board import ChessBoard
from logic.pieces import Knight, Bishop, Pawn, Obstacle

class TestPieceMovements:
    """หมวดทดสอบการเดินของหมากแต่ละประเภท (Piece Movements)"""

    def test_knight_movement_and_jumping(self):
        """เทสที่ 1: Knight เดินเป็นรูปตัว L และกระโดดข้ามหมากตัวอื่นได้"""
        board = ChessBoard()
        # เคลียร์กระดานให้ว่าง
        board.board = [[None for _ in range(8)] for _ in range(8)]
        
        # วาง Knight ขาวที่ D4 (3, 3)
        knight = Knight('white')
        board.board[3][3] = knight
        
        # วาง Obstacle ขวางทางเดินตรง (3, 4), (4, 3) ลองจำลองการขวาง
        board.board[3][4] = Obstacle("Rock", 99)
        board.board[4][3] = Obstacle("Rock", 99)
        board.board[4][4] = Obstacle("Rock", 99)
        
        # การเดินตัว L ไปตำแหน่ง E6 (1, 4) หรือ F5 (2, 5) ฯลฯ
        # (จาก 3,3 ไป 1,4 = ขยับแถว -2, คอลัมน์ +1)
        valid_moves = [
            (1, 4), (1, 2), # ขึ้น 2 ซ้ายขวา 1
            (5, 4), (5, 2), # ลง 2 ซ้ายขวา 1
            (2, 5), (4, 5), # ขวา 2 บนล่าง 1
            (2, 1), (4, 1)  # ซ้าย 2 บนล่าง 1
        ]
        
        for move in valid_moves:
            assert knight.is_valid_move((3, 3), move, board.board) == True

        # ลองเดินไปช่องที่ไม่ใช่ตัว L
        invalid_moves = [(3, 4), (4, 4), (2, 2), (1, 1), (7, 7)]
        for move in invalid_moves:
            assert knight.is_valid_move((3, 3), move, board.board) == False

    def test_bishop_movement_and_blocking(self):
        """เทสที่ 2: Bishop เดินทะแยง และถูกขวางได้เมื่อมีหมากบังทาง"""
        board = ChessBoard()
        board.board = [[None for _ in range(8)] for _ in range(8)]
        
        bishop = Bishop('white')
        
        # วาง Bishop ที่ C3 (5, 2)
        board.board[5][2] = bishop
        
        # เดินทะแยงมุมบนขวาไป F6 (2, 5) ระยะทาง 3 ช่อง
        assert bishop.is_valid_move((5, 2), (2, 5), board.board) == True
        # เดินทะแยงมุมล่างซ้ายไป A1 (7, 0) ระยะทาง 2 ช่อง
        assert bishop.is_valid_move((5, 2), (7, 0), board.board) == True

        # เดินไปช่องที่ไม่ใช่แนวทะแยง
        assert bishop.is_valid_move((5, 2), (5, 5), board.board) == False # เดินตรงไปขวา
        
        # วางหมากกีดขวางที่ D4 (4, 3) (ขวางการเดินไปฝั่งขวาบน)
        board.board[4][3] = Obstacle("Wall", 99)
        
        # ตอนนี้จะเดินทะแยงมุมบนขวาไป E5 (3, 4) และ F6 (2, 5) ไม่ได้แล้ว เพราะโดนบัง
        assert bishop.is_valid_move((5, 2), (3, 4), board.board) == False
        assert bishop.is_valid_move((5, 2), (2, 5), board.board) == False
        
        # แต่ยังขยับมากิน/หรืออยู่ตำแหน่ง (4, 3) ไม่ได้ใน logic ของเรา เพราะเป็นช่องเป้าหมาย แต่ is_path_clear ไม่นับช่องเป้าหมาย
        # แต่เดี๋ยวก่อน is_valid_move ของ Bishop เช็คแค่ is_path_clear ไม่ได้เช็ค target block (target เช็คใน move_piece หรือ board logic ถัดไป)
        # ดังนั้นถ้าไปช่องหลัง block มันควรจะเป็น False แน่นอน

    def test_pawn_movement_and_capture(self):
        """เทสที่ 3: Pawn เดิน 2 ช่องตาแรก เดิน 1 ช่องตาถัดไป และกินทะแยง"""
        board = ChessBoard()
        board.board = [[None for _ in range(8)] for _ in range(8)]
        
        pawn_white = Pawn('white')
        pawn_black = Pawn('black')
        
        # วาง Pawn ขาวที่จุดเริ่มต้นปกติ (แถว 6, คอลัมน์ 4) (E2)
        board.board[6][4] = pawn_white
        
        # 1. เดินตรง 1 ช่อง
        assert pawn_white.is_valid_move((6, 4), (5, 4), board.board) == True
        
        # 2. เดินตรง 2 ช่องตาแรก (จุดตัดเริ่ม)
        assert pawn_white.is_valid_move((6, 4), (4, 4), board.board) == True
        
        # ขยับ Pawn ไปตำแหน่งใหม่ (สมมติเดินมาแล้ว 1 ตาอยู่ที่ 5, 4)
        board.board[6][4] = None
        board.board[5][4] = pawn_white
        # 3. ลองเดิน 2 ช่องจากจุดที่ไม่ได้เริ่ม จะต้องเดินไม่ได้
        assert pawn_white.is_valid_move((5, 4), (3, 4), board.board) == False
        # เดินหน้าได้ 1 ช่อง
        assert pawn_white.is_valid_move((5, 4), (4, 4), board.board) == True

        # วาง Pawn ดำมาให้ขวางข้างหน้า Pawn ขาวที่ (4, 4)
        board.board[4][4] = pawn_black
        # 4. มีตัวขวางหน้า จะต้องเดินตรงไม่ได้
        assert pawn_white.is_valid_move((5, 4), (4, 4), board.board) == False

        # วางหมากศัตรูเยื้องทะแยงที่ (4, 3) ซ้ายบน และ (4, 5) ขวาบน
        board.board[4][3] = Pawn('black')
        board.board[4][5] = Pawn('black')
        
        # 5. กินทะแยงจะต้องกินได้ (True)
        assert pawn_white.is_valid_move((5, 4), (4, 3), board.board) == True
        assert pawn_white.is_valid_move((5, 4), (4, 5), board.board) == True
        
        # กินทะแยงไปช่องว่าง (ไม่มีหมาก) จะต้องเดินไม่ได้ (ยกเว้นระบบ En Passant ซึ่งตอนป้อนไม่ได้ส่ง ep_target)
        assert pawn_white.is_valid_move((5, 4), (4, 2), board.board) == False
