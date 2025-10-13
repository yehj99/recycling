#!/usr/bin/env python3
"""
분리수거 품목 분류 모델 훈련을 위한 데이터 준비 스크립트
"""
import os
import shutil
from pathlib import Path

def create_data_structure():
    """훈련 데이터 디렉토리 구조 생성"""
    
    # 기본 디렉토리 구조
    base_dir = Path("data/train")
    classes = ['glass', 'paper', 'plastic', 'metal', 'trash']
    
    print("=" * 60)
    print("분리수거 품목 분류 모델 훈련 데이터 구조 생성")
    print("=" * 60)
    
    # 디렉토리 생성
    for class_name in classes:
        class_dir = base_dir / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 생성됨: {class_dir}")
    
    print("\n" + "=" * 60)
    print("데이터 준비 가이드")
    print("=" * 60)
    
    # 각 클래스별 설명
    class_descriptions = {
        'glass': {
            'name': '유리 (Glass)',
            'examples': ['유리병', '유리컵', '유리잔', '유리조각'],
            'min_images': 100,
            'recommended': 500
        },
        'paper': {
            'name': '종이 (Paper)', 
            'examples': ['신문지', '책', '노트', '박스', '포장지'],
            'min_images': 100,
            'recommended': 500
        },
        'plastic': {
            'name': '플라스틱 (Plastic)',
            'examples': ['플라스틱병', '플라스틱컵', '비닐봉지', '플라스틱용기'],
            'min_images': 100,
            'recommended': 500
        },
        'metal': {
            'name': '금속 (Metal)',
            'examples': ['캔', '철제용기', '알루미늄', '스테인리스'],
            'min_images': 100,
            'recommended': 500
        },
        'trash': {
            'name': '일반 쓰레기 (Trash)',
            'examples': ['음식물쓰레기', '일회용품', '분해되지 않는 쓰레기'],
            'min_images': 100,
            'recommended': 500
        }
    }
    
    for class_name, info in class_descriptions.items():
        print(f"\n📁 {info['name']}")
        print(f"   예시: {', '.join(info['examples'])}")
        print(f"   최소 이미지: {info['min_images']}장")
        print(f"   권장 이미지: {info['recommended']}장")
        print(f"   저장 위치: data/train/{class_name}/")
    
    print("\n" + "=" * 60)
    print("이미지 요구사항")
    print("=" * 60)
    print("• 형식: JPG, PNG, BMP, TIFF")
    print("• 크기: 자동으로 224x224로 리사이즈됨")
    print("• 품질: 명확하고 다양한 각도/조명")
    print("• 다양성: 각 클래스별로 다양한 종류의 물체")
    
    print("\n" + "=" * 60)
    print("다음 단계")
    print("=" * 60)
    print("1. 각 클래스 폴더에 이미지 파일들을 복사")
    print("2. 데이터 품질 확인: python check_data_quality.py")
    print("3. 모델 훈련 시작: python train_model.py --data_dir data/train --epochs 20")
    
    return base_dir

def check_data_quality():
    """데이터 품질 확인"""
    base_dir = Path("data/train")
    
    if not base_dir.exists():
        print("❌ data/train 디렉토리가 존재하지 않습니다.")
        return
    
    print("\n" + "=" * 60)
    print("데이터 품질 확인")
    print("=" * 60)
    
    classes = ['glass', 'paper', 'plastic', 'metal', 'trash']
    total_images = 0
    
    for class_name in classes:
        class_dir = base_dir / class_name
        if class_dir.exists():
            image_files = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")) + \
                         list(class_dir.glob("*.bmp")) + list(class_dir.glob("*.tiff"))
            count = len(image_files)
            total_images += count
            
            status = "✅" if count >= 100 else "⚠️" if count >= 50 else "❌"
            print(f"{status} {class_name}: {count}장")
        else:
            print(f"❌ {class_name}: 디렉토리 없음")
    
    print(f"\n총 이미지 수: {total_images}장")
    
    if total_images >= 500:
        print("✅ 훈련을 시작할 수 있습니다!")
    elif total_images >= 250:
        print("⚠️  더 많은 데이터를 권장합니다.")
    else:
        print("❌ 데이터가 부족합니다. 최소 250장 이상 필요합니다.")

def main():
    """메인 함수"""
    print("분리수거 품목 분류 모델 훈련 데이터 준비")
    print("=" * 60)
    
    # 데이터 구조 생성
    create_data_structure()
    
    # 데이터 품질 확인
    check_data_quality()

if __name__ == "__main__":
    main()
