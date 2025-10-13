#!/usr/bin/env python3
"""
분리수거 품목 분류 추론 테스트 스크립트

사용법:
    python test_inference.py --image_path ./test_image.jpg --model_path ./models/recycling_classifier.h5
"""

import argparse
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.inference_service import InferenceService


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='분리수거 품목 분류 추론 테스트')
    parser.add_argument(
        '--image_path', 
        type=str, 
        required=True, 
        help='분류할 이미지 파일 경로'
    )
    parser.add_argument(
        '--model_path', 
        type=str, 
        default='models/recycling_classifier.h5', 
        help='모델 파일 경로 (기본값: models/recycling_classifier.h5)'
    )
    
    args = parser.parse_args()
    
    # 이미지 파일 존재 확인
    if not os.path.exists(args.image_path):
        print(f"오류: 이미지 파일이 존재하지 않습니다: {args.image_path}")
        return 1
    
    # 모델 파일 존재 확인
    if not os.path.exists(args.model_path):
        print(f"오류: 모델 파일이 존재하지 않습니다: {args.model_path}")
        print("먼저 모델을 훈련하세요: python train_model.py --data_dir ./data/train")
        return 1
    
    print("=" * 50)
    print("분리수거 품목 분류 추론 테스트")
    print("=" * 50)
    print(f"이미지 파일: {args.image_path}")
    print(f"모델 파일: {args.model_path}")
    print("=" * 50)
    
    try:
        # 추론 서비스 초기화
        inference_service = InferenceService(args.model_path)
        
        if not inference_service.is_model_loaded():
            print("오류: 모델을 로드할 수 없습니다.")
            return 1
        
        # 이미지 분류 수행
        result = inference_service.classify_image(args.image_path)
        
        if 'error' in result:
            print(f"오류: {result['error']}")
            return 1
        
        # 결과 출력
        print("\n분류 결과:")
        print("-" * 30)
        print(f"예측 클래스: {result['predicted_class']}")
        print(f"신뢰도: {result['confidence']:.4f}")
        print(f"분리수거 가능: {'예' if result['is_recyclable'] else '아니오'}")
        
        print("\n모든 클래스별 확률:")
        print("-" * 30)
        for class_name, probability in result['class_probabilities'].items():
            print(f"{class_name}: {probability:.4f}")
        
        return 0
        
    except Exception as e:
        print(f"오류: 추론 중 문제가 발생했습니다: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
