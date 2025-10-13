#!/usr/bin/env python3
"""
사전훈련된 EfficientNetV2 모델을 사용하여 테스트용 모델 생성
학습하지 않은 상태에서도 기본적인 이미지 분류가 가능합니다.
"""

import os
import sys
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_pretrained_model():
    """사전훈련된 EfficientNetV2 모델 생성"""
    
    # 분리수거 품목 클래스 정의
    class_names = [
        'glass',              # 유리
        'paper',             # 종이
        'plastic',            # 플라스틱
        'metal',             # 금속
        'trash'              # 일반 쓰레기
    ]
    
    input_size = (224, 224, 3)
    num_classes = len(class_names)
    
    # EfficientNetV2-S 모델 로드 (사전 훈련된 가중치 사용)
    base_model = keras.applications.EfficientNetV2S(
        weights='imagenet',  # ImageNet 사전훈련 가중치
        include_top=False,
        input_shape=input_size
    )
    
    # 사전 훈련된 모델의 가중치 고정
    base_model.trainable = False
    
    # 분류 헤드 추가
    inputs = keras.Input(shape=input_size)
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    
    # 컴파일 (가중치는 랜덤 초기화됨)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model, class_names

def save_model_and_info(model, class_names, model_path="models/recycling_classifier.h5"):
    """모델과 클래스 정보 저장"""
    
    # models 디렉토리 생성
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # 모델 저장
    model.save(model_path)
    print(f"모델이 저장되었습니다: {model_path}")
    
    # 클래스 정보 저장
    class_info = {
        'class_names': class_names,
        'num_classes': len(class_names),
        'model_type': 'pretrained_efficientnetv2',
        'description': 'ImageNet 사전훈련된 EfficientNetV2-S 모델 (분리수거 품목에 특화되지 않음)'
    }
    
    class_file = model_path.replace('.h5', '_classes.json')
    with open(class_file, 'w', encoding='utf-8') as f:
        json.dump(class_info, f, ensure_ascii=False, indent=2)
    
    print(f"클래스 정보가 저장되었습니다: {class_file}")
    
    return model_path, class_file

def main():
    """메인 함수"""
    print("=" * 60)
    print("사전훈련된 EfficientNetV2 모델 생성")
    print("=" * 60)
    print("주의: 이 모델은 ImageNet으로 사전훈련된 모델입니다.")
    print("분리수거 품목에 특화되지 않아 정확도가 낮을 수 있습니다.")
    print("=" * 60)
    
    try:
        # 모델 생성
        print("모델 생성 중...")
        model, class_names = create_pretrained_model()
        
        # 모델 정보 출력
        print(f"모델 구조:")
        model.summary()
        
        # 모델 저장
        print("\n모델 저장 중...")
        model_path, class_file = save_model_and_info(model, class_names)
        
        print("\n" + "=" * 60)
        print("생성 완료!")
        print("=" * 60)
        print(f"모델 파일: {model_path}")
        print(f"클래스 정보: {class_file}")
        print("\n이제 API 서버를 실행하여 테스트할 수 있습니다:")
        print("uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("\n또는 테스트 스크립트를 실행하세요:")
        print("python test_inference.py --image_path <이미지경로>")
        
        return 0
        
    except Exception as e:
        print(f"\n오류: 모델 생성 중 문제가 발생했습니다: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
