"""
모델 훈련을 위한 서비스
"""
import os
import argparse
from typing import Dict, Any, Optional
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

from app.core.interfaces import IModelTrainer
from app.models.recycling_classifier import RecyclingClassifier
from app.core.data_processor import DataProcessor, DataQualityChecker


class ModelTrainer(IModelTrainer):
    """모델 훈련기 구현"""
    
    def __init__(self):
        self.data_processor = DataProcessor()
        self.quality_checker = DataQualityChecker(self.data_processor)
    
    def train(self, data_dir: str, epochs: int = 10, save_path: str = None) -> Dict[str, Any]:
        """모델 훈련"""
        if save_path is None:
            save_path = "models/recycling_classifier.h5"
        
        print(f"데이터 디렉토리: {data_dir}")
        print(f"에포크 수: {epochs}")
        print(f"모델 저장 경로: {save_path}")
        
        # 데이터 디렉토리 확인
        if not os.path.exists(data_dir):
            raise ValueError(f"데이터 디렉토리가 존재하지 않습니다: {data_dir}")
        
        # 데이터 품질 검사
        quality_report = self.quality_checker.check_dataset_quality(data_dir)
        print(f"데이터 품질 보고서: {quality_report}")
        
        # 분류기 생성
        classifier = RecyclingClassifier()
        
        # 모델 훈련
        print("모델 훈련을 시작합니다...")
        history = classifier.fine_tune(
            data_dir=data_dir,
            epochs=epochs,
            save_path=save_path
        )
        
        print("모델 훈련이 완료되었습니다!")
        print(f"최종 훈련 정확도: {history.history['accuracy'][-1]:.4f}")
        print(f"최종 검증 정확도: {history.history['val_accuracy'][-1]:.4f}")
        
        return {
            'history': history,
            'quality_report': quality_report,
            'final_accuracy': history.history['accuracy'][-1],
            'final_val_accuracy': history.history['val_accuracy'][-1]
        }
    
    def validate_model(self, validation_data: Any) -> Dict[str, Any]:
        """모델 검증"""
        # 모델 검증 로직 구현
        pass


def train_model(data_dir: str, epochs: int = 10, model_save_path: str = "models/recycling_classifier.h5"):
    """
    모델 훈련 함수 (기존 호환성 유지)
    
    Args:
        data_dir: 훈련 데이터가 있는 디렉토리 경로
        epochs: 훈련 에포크 수
        model_save_path: 모델 저장 경로
    """
    trainer = ModelTrainer()
    result = trainer.train(data_dir, epochs, model_save_path)
    return result['history']


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='분리수거 품목 분류 모델 훈련')
    parser.add_argument('--data_dir', type=str, required=True, help='훈련 데이터 디렉토리 경로')
    parser.add_argument('--epochs', type=int, default=10, help='훈련 에포크 수')
    parser.add_argument('--model_path', type=str, default='models/recycling_classifier.h5', help='모델 저장 경로')
    
    args = parser.parse_args()
    
    try:
        train_model(
            data_dir=args.data_dir,
            epochs=args.epochs,
            model_save_path=args.model_path
        )
    except Exception as e:
        print(f"훈련 중 오류가 발생했습니다: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
