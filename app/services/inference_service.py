"""
이미지 분류 추론 서비스
"""
import os
import io
import numpy as np
from PIL import Image
from typing import Dict, Optional
from app.models.recycling_classifier import RecyclingClassifier


class InferenceService:
    """이미지 분류 추론 서비스"""
    
    def __init__(self, model_path: str = "models/recycling_classifier.h5"):
        self.model_path = model_path
        self.classifier = None
        self._load_model()
    
    def _load_model(self):
        """모델 로드"""
        if os.path.exists(self.model_path):
            try:
                self.classifier = RecyclingClassifier(self.model_path)
                print(f"모델이 성공적으로 로드되었습니다: {self.model_path}")
            except Exception as e:
                print(f"모델 로드 중 오류가 발생했습니다: {e}")
                self.classifier = None
        else:
            print(f"모델 파일을 찾을 수 없습니다: {self.model_path}")
            print("테스트용 사전훈련된 모델을 생성하려면 다음 명령을 실행하세요:")
            print("python create_pretrained_model.py")
            self.classifier = None
    
    def is_model_loaded(self) -> bool:
        """모델이 로드되었는지 확인"""
        return self.classifier is not None and self.classifier.model is not None
    
    def classify_image(self, image_path: str) -> Dict:
        """
        이미지 분류
        
        Args:
            image_path: 이미지 파일 경로
            
        Returns:
            분류 결과 딕셔너리
        """
        if not self.is_model_loaded():
            return {
                'error': '모델이 로드되지 않았습니다.',
                'predicted_class': None,
                'confidence': 0.0,
                'is_recyclable': False
            }
        
        if not os.path.exists(image_path):
            return {
                'error': f'이미지 파일을 찾을 수 없습니다: {image_path}',
                'predicted_class': None,
                'confidence': 0.0,
                'is_recyclable': False
            }
        
        try:
            result = self.classifier.predict(image_path)
            return result
        except Exception as e:
            return {
                'error': f'분류 중 오류가 발생했습니다: {str(e)}',
                'predicted_class': None,
                'confidence': 0.0,
                'is_recyclable': False
            }
    
    def classify_image_from_bytes(self, image_bytes: bytes) -> Dict:
        """
        바이트 데이터로부터 이미지 분류
        
        Args:
            image_bytes: 이미지 바이트 데이터
            
        Returns:
            분류 결과 딕셔너리
        """
        if not self.is_model_loaded():
            return {
                'error': '모델이 로드되지 않았습니다.',
                'predicted_class': None,
                'confidence': 0.0,
                'is_recyclable': False
            }
        
        try:
            # 바이트 데이터를 PIL Image로 변환
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert('RGB')
            image = image.resize((224, 224))
            
            # numpy 배열로 변환
            image_array = np.array(image) / 255.0
            
            # 분류 수행
            result = self.classifier.predict_from_array(image_array)
            return result
        except Exception as e:
            return {
                'error': f'분류 중 오류가 발생했습니다: {str(e)}',
                'predicted_class': None,
                'confidence': 0.0,
                'is_recyclable': False
            }
    
    def get_class_info(self) -> Dict:
        """클래스 정보 반환"""
        if not self.is_model_loaded():
            return {'error': '모델이 로드되지 않았습니다.'}
        
        return {
            'class_names': self.classifier.class_names,
            'num_classes': self.classifier.num_classes,
            'recyclable_classes': ['glass', 'paper', 'plastic', 'metal']
        }


# 전역 추론 서비스 인스턴스
inference_service = InferenceService()
