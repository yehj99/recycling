"""
데이터 처리기 - 이미지 전처리 및 데이터 증강
"""
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional, Any
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from app.core.interfaces import IDataProcessor


class DataProcessor(IDataProcessor):
    """데이터 처리기 구현"""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
        self._augmentation_generator = None
        self._setup_augmentation()
    
    def _setup_augmentation(self):
        """데이터 증강 설정"""
        self._augmentation_generator = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            fill_mode='nearest'
        )
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """이미지 전처리"""
        try:
            # 이미지 로드
            img = Image.open(image_path)
            img = img.convert('RGB')
            
            # 크기 조정
            img = img.resize(self.target_size)
            
            # numpy 배열로 변환 및 정규화
            img_array = np.array(img) / 255.0
            
            # 배치 차원 추가
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise ValueError(f"이미지 전처리 중 오류 발생: {str(e)}")
    
    def preprocess_image_from_array(self, image_array: np.ndarray) -> np.ndarray:
        """numpy 배열로부터 이미지 전처리"""
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        
        # 크기 조정
        if image_array.shape[1:3] != self.target_size:
            # PIL Image로 변환 후 크기 조정
            img = Image.fromarray((image_array[0] * 255).astype(np.uint8))
            img = img.resize(self.target_size)
            image_array = np.array(img) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    
    def augment_data(self, data: Any) -> Any:
        """데이터 증강"""
        if self._augmentation_generator is None:
            self._setup_augmentation()
        
        return self._augmentation_generator.flow_from_directory(
            data,
            target_size=self.target_size,
            batch_size=32,
            class_mode='categorical',
            shuffle=True
        )
    
    def create_training_generator(self, data_dir: str, validation_split: float = 0.2):
        """훈련 데이터 생성기 생성"""
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            validation_split=validation_split
        )
        
        train_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=self.target_size,
            batch_size=32,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        validation_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=self.target_size,
            batch_size=32,
            class_mode='categorical',
            subset='validation',
            shuffle=True
        )
        
        return train_generator, validation_generator


class ImageValidator:
    """이미지 검증기"""
    
    @staticmethod
    def validate_image_file(image_path: str) -> bool:
        """이미지 파일 검증"""
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_image_format(image_path: str, allowed_formats: List[str] = None) -> bool:
        """이미지 형식 검증"""
        if allowed_formats is None:
            allowed_formats = ['JPEG', 'PNG', 'BMP', 'TIFF']
        
        try:
            with Image.open(image_path) as img:
                return img.format in allowed_formats
        except Exception:
            return False
    
    @staticmethod
    def validate_image_size(image_path: str, min_size: Tuple[int, int] = (32, 32)) -> bool:
        """이미지 크기 검증"""
        try:
            with Image.open(image_path) as img:
                return img.size[0] >= min_size[0] and img.size[1] >= min_size[1]
        except Exception:
            return False


class DataQualityChecker:
    """데이터 품질 검사기"""
    
    def __init__(self, data_processor: DataProcessor):
        self.data_processor = data_processor
        self.validator = ImageValidator()
    
    def check_dataset_quality(self, data_dir: str) -> dict:
        """데이터셋 품질 검사"""
        import os
        
        quality_report = {
            'total_images': 0,
            'valid_images': 0,
            'invalid_images': 0,
            'class_distribution': {},
            'size_distribution': {},
            'format_distribution': {}
        }
        
        for class_name in os.listdir(data_dir):
            class_path = os.path.join(data_dir, class_name)
            if not os.path.isdir(class_path):
                continue
            
            class_images = []
            for filename in os.listdir(class_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                    image_path = os.path.join(class_path, filename)
                    
                    quality_report['total_images'] += 1
                    
                    if self.validator.validate_image_file(image_path):
                        quality_report['valid_images'] += 1
                        class_images.append(image_path)
                    else:
                        quality_report['invalid_images'] += 1
            
            quality_report['class_distribution'][class_name] = len(class_images)
        
        return quality_report
