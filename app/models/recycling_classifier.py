"""
분리수거 품목 분류를 위한 EfficientNetV2 모델
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from PIL import Image
import os
from typing import List, Tuple, Dict
import json


class RecyclingClassifier:
    """분리수거 품목 분류 모델 클래스"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.class_names = [
            'glass',              # 유리
            'paper',             # 종이
            'plastic',            # 플라스틱
            'metal',             # 금속
            'trash'              # 일반 쓰레기
        ]
        self.num_classes = len(self.class_names)
        self.input_size = (224, 224, 3)
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def create_base_model(self) -> keras.Model:
        """EfficientNetV2 기반 모델 생성"""
        # EfficientNetV2-S 모델 로드 (사전 훈련된 가중치 사용)
        base_model = keras.applications.EfficientNetV2S(
            weights='imagenet',
            include_top=False,
            input_shape=self.input_size
        )
        
        # 사전 훈련된 모델의 가중치 고정 (처음 몇 개 레이어만)
        base_model.trainable = False
        
        # 분류 헤드 추가
        inputs = keras.Input(shape=self.input_size)
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        model = keras.Model(inputs, outputs)
        return model
    
    def prepare_data(self, data_dir: str, validation_split: float = 0.2) -> Tuple[tf.data.Dataset, tf.data.Dataset]:
        """데이터셋 준비"""
        # 데이터 증강 설정
        train_datagen = keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            validation_split=validation_split
        )
        
        # 훈련 데이터
        train_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        # 검증 데이터
        validation_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            subset='validation',
            shuffle=True
        )
        
        return train_generator, validation_generator
    
    def fine_tune(self, data_dir: str, epochs: int = 10, save_path: str = "models/recycling_classifier.h5"):
        """모델 파인튜닝"""
        # 모델 생성
        self.model = self.create_base_model()
        
        # 컴파일
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # 데이터 준비
        train_gen, val_gen = self.prepare_data(data_dir)
        
        # 콜백 설정
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=3,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=2,
                min_lr=1e-7
            )
        ]
        
        # 훈련
        history = self.model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1
        )
        
        # 모델 저장
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.model.save(save_path)
        
        # 클래스 이름 저장
        class_info = {
            'class_names': self.class_names,
            'num_classes': self.num_classes
        }
        with open(f"{save_path.replace('.h5', '_classes.json')}", 'w', encoding='utf-8') as f:
            json.dump(class_info, f, ensure_ascii=False, indent=2)
        
        return history
    
    def load_model(self, model_path: str):
        """저장된 모델 로드"""
        self.model = keras.models.load_model(model_path)
        
        # 클래스 정보 로드
        class_file = model_path.replace('.h5', '_classes.json')
        if os.path.exists(class_file):
            with open(class_file, 'r', encoding='utf-8') as f:
                class_info = json.load(f)
                self.class_names = class_info['class_names']
                self.num_classes = class_info['num_classes']
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """이미지 전처리"""
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def predict(self, image_path: str) -> Dict:
        """이미지 분류 예측"""
        if self.model is None:
            raise ValueError("모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요.")
        
        # 이미지 전처리
        processed_image = self.preprocess_image(image_path)
        
        # 예측
        predictions = self.model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        predicted_class = self.class_names[predicted_class_idx]
        
        # 모든 클래스에 대한 확률
        class_probabilities = {
            self.class_names[i]: float(predictions[0][i])
            for i in range(len(self.class_names))
        }
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'class_probabilities': class_probabilities,
            'is_recyclable': predicted_class in ['glass', 'paper', 'plastic', 'metal']
        }
    
    def predict_from_array(self, image_array: np.ndarray) -> Dict:
        """numpy 배열로부터 이미지 분류 예측"""
        if self.model is None:
            raise ValueError("모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요.")
        
        # 이미지 전처리
        if len(image_array.shape) == 3:
            image_array = np.expand_dims(image_array, axis=0)
        
        # 예측
        predictions = self.model.predict(image_array, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        predicted_class = self.class_names[predicted_class_idx]
        
        # 모든 클래스에 대한 확률
        class_probabilities = {
            self.class_names[i]: float(predictions[0][i])
            for i in range(len(self.class_names))
        }
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'class_probabilities': class_probabilities,
            'is_recyclable': predicted_class in ['glass', 'paper', 'plastic', 'metal']
        }
