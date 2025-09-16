"""
Gemini API 서비스
"""
import google.generativeai as genai
from django.conf import settings
import logging
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.vision_model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        텍스트 생성
        """
        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'text': response.text,
                'model': 'gemini-1.5-pro'
            }
        except Exception as e:
            logger.error(f"Gemini 텍스트 생성 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': 'gemini-1.5-pro'
            }
    
    def analyze_image(self, image_data: bytes, prompt: str = "이 이미지를 분석해주세요.") -> Dict[str, Any]:
        """
        이미지 분석
        """
        try:
            from PIL import Image
            import io
            
            # 이미지 데이터를 PIL Image로 변환
            image = Image.open(io.BytesIO(image_data))
            
            response = self.vision_model.generate_content([prompt, image])
            return {
                'success': True,
                'text': response.text,
                'model': 'gemini-1.5-pro'
            }
        except Exception as e:
            logger.error(f"Gemini 이미지 분석 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': 'gemini-1.5-pro'
            }
    
    def generate_quiz_question(self) -> Dict[str, Any]:
        """
        퀴즈 문제 생성
        """
        try:
            prompt = f"""
            환경 보호와 관련된 퀴즈를 다음 JSON 형식으로 생성해주세요.
            반드시 아래 형식을 정확히 지켜서 JSON만 응답해주세요:
            
            다음 형식으로 JSON 형태로 응답해주세요:
            {{
                "question": "문제 내용",
                "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
                "correct_answer": 0,
                "explanation": "정답에 대한 자세한 설명"
            }}
            
            주제는 다음 중 하나를 선택해서 작성해주세요:
                1. 기후변화와 지구온난화
                2. 재활용과 자원순환
                3. 친환경 생활습관
                4. 탄소중립과 신재생에너지
                
            난이도는 일반인이 이해할 수 있는 수준으로 작성하고,
            설명은 교육적이고 실용적인 내용으로 작성해주세요.
            """
            
            response = self.model.generate_content(prompt)
            
            # JSON 파싱 시도
            try:
                result = json.loads(response.text)
                return {
                    'success': True,
                    'quiz': result,
                    'model': 'gemini-1.5-pro'
                }
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 텍스트 그대로 반환
                return {
                    'success': True,
                    'quiz_text': response.text,
                    'model': 'gemini-1.5-pro'
                }
                
        except Exception as e:
            logger.error(f"Gemini 퀴즈 생성 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': 'gemini-1.5-pro'
            }
