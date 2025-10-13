#!/usr/bin/env python3
"""
분리수거 품목 분류 모델 훈련 스크립트

사용법:
    python train_model.py --data_dir ./data/train --epochs 20 --model_path ./models/recycling_classifier.h5
"""

import argparse
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.model_trainer import train_model


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='분리수거 품목 분류 모델 훈련',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
데이터 디렉토리 구조 예시:
data/
├── train/
│   ├── plastic_bottle/
│   ├── glass_bottle/
│   ├── can/
│   ├── paper/
│   ├── cardboard/
│   ├── plastic_bag/
│   ├── food_waste/
│   └── general_waste/
        """
    )
    
    parser.add_argument(
        '--data_dir', 
        type=str, 
        required=True, 
        help='훈련 데이터 디렉토리 경로 (각 클래스별로 하위 디렉토리 구성)'
    )
    parser.add_argument(
        '--epochs', 
        type=int, 
        default=10, 
        help='훈련 에포크 수 (기본값: 10)'
    )
    parser.add_argument(
        '--model_path', 
        type=str, 
        default='models/recycling_classifier.h5', 
        help='모델 저장 경로 (기본값: models/recycling_classifier.h5)'
    )
    
    args = parser.parse_args()
    
    # 데이터 디렉토리 존재 확인
    if not os.path.exists(args.data_dir):
        print(f"오류: 데이터 디렉토리가 존재하지 않습니다: {args.data_dir}")
        return 1
    
    print("=" * 50)
    print("분리수거 품목 분류 모델 훈련 시작")
    print("=" * 50)
    print(f"데이터 디렉토리: {args.data_dir}")
    print(f"에포크 수: {args.epochs}")
    print(f"모델 저장 경로: {args.model_path}")
    print("=" * 50)
    
    try:
        # 모델 훈련 실행
        history = train_model(
            data_dir=args.data_dir,
            epochs=args.epochs,
            model_save_path=args.model_path
        )
        
        print("\n" + "=" * 50)
        print("훈련 완료!")
        print("=" * 50)
        print(f"최종 훈련 정확도: {history.history['accuracy'][-1]:.4f}")
        print(f"최종 검증 정확도: {history.history['val_accuracy'][-1]:.4f}")
        print(f"모델이 저장되었습니다: {args.model_path}")
        
        return 0
        
    except Exception as e:
        print(f"\n오류: 훈련 중 문제가 발생했습니다: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
