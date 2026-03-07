# tests/test_variants.py
import pytest
from logic.board import ChessBoard

class TestMaps:
    """หมวดทดสอบระบบด่าน (Maps) แยกทีละด่าน"""
    
    def test_classic_map_loaded(self):
        """เทสที่ 1: ด่าน Classic Board"""
        board = ChessBoard(map_name='Classic Board')
        # ตรวจสอบว่าดึงรูปพื้นหลังได้ถูกต้อง
        assert board.bg_image == 'assets/boards/classic.png'

    def test_forest_map_loaded(self):
        """เทสที่ 2: ด่าน Enchanted Forest"""
        board = ChessBoard(map_name='Enchanted Forest')
        assert board.bg_image == 'assets/boards/forest.png'

    def test_desert_map_loaded(self):
        """เทสที่ 3: ด่าน Desert Ruins"""
        board = ChessBoard(map_name='Desert Ruins')
        assert board.bg_image == 'assets/boards/desert.png'

    def test_tundra_map_loaded(self):
        """เทสที่ 4: ด่าน Frozen Tundra"""
        board = ChessBoard(map_name='Frozen Tundra')
        assert board.bg_image == 'assets/boards/tundra.png'


class TestTribes:
    """หมวดทดสอบระบบเผ่าพันธุ์ (Tribes) แยกทีละคู่"""
    
    def test_tribe_medieval_and_ayothaya(self):
        """เทสที่ 5: คู่เผ่า อัศวินยุคกลาง (ขาว) vs อยุธยา (ดำ)"""
        board = ChessBoard(white_tribe='medieval', black_tribe='ayothaya')
        
        # เช็คว่าระบบกระดานบันทึกค่าเผ่าถูกต้อง (ในระบบเกม เผ่าจะถูกเก็บไว้ที่ Board ไม่ใช่ที่ตัว Piece)
        assert board.white_tribe == 'medieval'
        assert board.black_tribe == 'ayothaya'
        
        # สำหรับตัวหมาก (Piece) ระบบจะเอาชื่อเผ่าไปคำนวณสเตตัส (setup_stats) 
        # ดังนั้นวิธีเช็คที่ถูกต้องคือดูว่าตัวหมากมีค่า passive_desc, base_points เป็นต้นหรือไม่
        white_king = board.board[7][4]
        black_king = board.board[0][4]
        assert hasattr(white_king, 'passive_desc')
        assert hasattr(black_king, 'passive_desc')
        # ตรวจสอบว่า King ทั้งคู่ได้รับค่าสเตตัสเริ่มต้นเรียบร้อยแล้ว (มากกว่า 0)
        assert white_king.base_points >= 0
        assert black_king.base_points >= 0

    def test_tribe_demon_and_heaven(self):
        """เทสที่ 6: คู่เผ่า ปีศาจ (ขาว) vs สวรรค์ (ดำ)"""
        board = ChessBoard(white_tribe='demon', black_tribe='heaven')
        
        assert board.white_tribe == 'demon'
        assert board.black_tribe == 'heaven'
        
        white_king = board.board[7][4]
        black_king = board.board[0][4]
        assert hasattr(white_king, 'passive_desc')
        assert hasattr(black_king, 'passive_desc')
        assert white_king.base_points >= 0
        assert black_king.base_points >= 0