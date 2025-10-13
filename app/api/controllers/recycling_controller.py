"""
분리수거 품목 분류 컨트롤러
"""
from typing import Dict, Any, List, Optional
from fastapi import UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.api.base import BaseController, APIResponse, RequestValidator, ErrorHandler
from app.core.interfaces import IImageClassifier


class RecyclingController(BaseController):
    """분리수거 품목 분류 컨트롤러"""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.classifier = self.get_service('inference_service')
    
    def validate_request(self, request_data: Dict[str, Any]) -> bool:
        """요청 데이터 검증"""
        # 기본 검증 로직
        return True
    
    async def classify_image(self, file: UploadFile) -> APIResponse:
        """이미지 분류"""
        try:
            # 파일 검증
            if not RequestValidator.validate_image_file(file.content_type):
                return APIResponse.error("이미지 파일만 업로드 가능합니다.")
            
            # 파일 읽기 (비동기)
            contents = await file.read()
            
            # 이미지 분류
            result = self.classifier.classify_image_from_bytes(contents)
            
            if 'error' in result:
                return APIResponse.error(result['error'])
            
            return APIResponse.success({
                "filename": file.filename,
                "predicted_class": result['predicted_class'],
                "confidence": result['confidence'],
                "is_recyclable": result['is_recyclable'],
                "class_probabilities": result['class_probabilities']
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def classify_local_image(self, image_path: str) -> APIResponse:
        """로컬 이미지 분류"""
        try:
            import os
            if not os.path.exists(image_path):
                raise ErrorHandler.handle_not_found_error("이미지 파일")
            
            # 이미지 분류
            result = self.classifier.classify_image(image_path)
            
            if 'error' in result:
                return APIResponse.error(result['error'])
            
            return APIResponse.success({
                "image_path": image_path,
                "predicted_class": result['predicted_class'],
                "confidence": result['confidence'],
                "is_recyclable": result['is_recyclable'],
                "class_probabilities": result['class_probabilities']
            })
            
        except HTTPException:
            raise
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    async def batch_classify_images(self, files: List[UploadFile]) -> APIResponse:
        """배치 이미지 분류"""
        try:
            if len(files) > 10:
                return APIResponse.error("한 번에 최대 10개 파일까지만 처리 가능합니다.")
            
            results = []
            
            for file in files:
                try:
                    # 파일 검증
                    if not RequestValidator.validate_image_file(file.content_type):
                        results.append({
                            "filename": file.filename,
                            "error": "이미지 파일이 아닙니다."
                        })
                        continue
                    
                    # 파일 읽기 (비동기)
                    contents = await file.read()
                    
                    # 이미지 분류
                    result = self.classifier.classify_image_from_bytes(contents)
                    
                    if 'error' in result:
                        results.append({
                            "filename": file.filename,
                            "error": result['error']
                        })
                    else:
                        results.append({
                            "filename": file.filename,
                            "predicted_class": result['predicted_class'],
                            "confidence": result['confidence'],
                            "is_recyclable": result['is_recyclable']
                        })
                        
                except Exception as e:
                    results.append({
                        "filename": file.filename,
                        "error": f"처리 중 오류가 발생했습니다: {str(e)}"
                    })
            
            return APIResponse.success({
                "total_files": len(files),
                "results": results
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def get_class_info(self) -> APIResponse:
        """클래스 정보 조회"""
        try:
            class_info = self.classifier.get_class_info()
            
            if 'error' in class_info:
                return APIResponse.error(class_info['error'])
            
            return APIResponse.success(class_info)
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def health_check(self) -> APIResponse:
        """서비스 상태 확인"""
        try:
            is_model_loaded = hasattr(self.classifier, 'is_model_loaded') and self.classifier.is_model_loaded()
            
            return APIResponse.success({
                "status": "healthy",
                "model_loaded": is_model_loaded
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
