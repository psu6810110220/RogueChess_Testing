# tests/test_items.py
import pytest
from unittest.mock import patch
from logic.board import ChessBoard
from logic.pieces import Rook, Pawn, Knight
from logic.item_logic import ITEM_DATABASE
from logic.item_effects import apply_equip_effect, get_pre_crash_modifiers
from logic.crash_logic import simulate_ai_crash_result

class TestItemsAndInventory:
    """หมวดทดสอบระบบไอเทมและคลังเก็บของ (Items & Inventory System)"""

    def test_stat_boost(self):
        """เทสที่ 1: จำลองการสวมใส่ไอเทมเพิ่ม/ลดพลัง และตรวจสอบค่าสถานะของตัวหมาก"""
        pawn = Pawn('white')
        # จำลองเบี้ยที่มีค่าเริ่มต้นบางอย่าง (ปกติ base_points=5, coins=3 สำหรับ Pawn ใน medieval)
        initial_base = pawn.base_points
        initial_coins = pawn.coins
        
        # ใส่ไอเทม 6: Gambler's Coin (+1 Coin, -2 Base Point)
        pawn.item = ITEM_DATABASE[6]
        apply_equip_effect(pawn)
        
        # ตรวจสอบค่าสถานะที่เปลี่ยนไป
        assert pawn.coins == initial_coins + 1
        assert pawn.base_points == initial_base - 2

        # ลองใส่ไอเทม 10: Crown of the Usurper (เฉพาะ Pawn ให้ Base=5, Coin=3 เสมอ)
        pawn.item = ITEM_DATABASE[10]
        apply_equip_effect(pawn)
        assert pawn.base_points == 5
        assert pawn.coins == 3

    def test_shield_logic(self):
        """เทสที่ 2: ตรวจสอบว่าถ้าหมากมีไอเทมโล่ป้องกัน โล่จะทำงานเพื่อป้องกันการโจมตีได้จริง"""
        attacker = Rook('white')
        defender = Rook('black')
        
        # ให้ฝั่งรับใส่ป้ายโล่ Mirage Shield (ID 4)
        defender.item = ITEM_DATABASE[4]
        
        # วิธีที่ 1: เช็คการคำนวณ Modifier ก่อนเริ่มทอยเหรียญ (Pre-Crash Modifiers)
        a_mod, d_mod, is_blocked = get_pre_crash_modifiers(attacker, defender)
        assert is_blocked == True
        
        # วิธีที่ 2: เช็คตอนจำลองผลการต่อสู้ของ AI จะต้องคืนค่ามาว่าโดนบล็อก
        result = simulate_ai_crash_result(attacker, defender, "medieval", "medieval")
        assert result == "blocked"

    @patch('logic.board.random.randint')
    @patch('components.hidden_passive.random.randint')
    def test_inventory_limit(self, mock_hidden_randint, mock_board_randint):
        """เทสที่ 3: ตรวจสอบว่าถ้ากระเป๋าเต็มแล้ว (เกิน 5 ชิ้น) จะไม่สามารถเก็บไอเทมเพิ่มได้"""
        # ให้การจำลอง Passive ราบรื่น ไม่ error ตอนสร้างหมาก
        mock_hidden_randint.return_value = 50 
        mock_board_randint.return_value = 1
        
        board = ChessBoard()
        
        # สร้างกระเป๋าให้เต็ม 5 ชิ้นไปก่อน
        for i in range(5):
            board.inventory_white.append(ITEM_DATABASE[1])
            
        assert len(board.inventory_white) == 5
        
        # ผู้ชนะปะทะฝ่ายขาวที่ควรจะได้ไอเทมดรอป
        winner = Knight('white')
        board.handle_item_drop(winner, is_defender=False)
        
        # จำนวนไอเทมจะต้องเท่าเดิม เพราะเต็มแล้ว (5 ชิ้น)
        assert len(board.inventory_white) == 5
