#!/usr/bin/env python3
"""
데이터베이스 초기화 스크립트
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import create_tables

def main():
    """메인 함수"""
    print("=" * 50)
    print("데이터베이스 초기화")
    print("=" * 50)
    
    try:
        create_tables()
        print("✅ 데이터베이스 테이블이 성공적으로 생성되었습니다.")
        print("생성된 테이블:")
        print("- chat_log")
        print("- location")
        return 0
    except Exception as e:
        print(f"❌ 오류: 데이터베이스 초기화 중 문제가 발생했습니다: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
