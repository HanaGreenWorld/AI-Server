"""
OpenAI GPT API 서비스
"""
import openai
from django.conf import settings
import logging
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class GPTService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_text(self, prompt: str, model: str = "gpt-3.5-turbo", **kwargs) -> Dict[str, Any]:
        """
        텍스트 생성
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "당신은 친환경 활동을 도와주는 AI 어시스턴트입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            return {
                'success': True,
                'text': response.choices[0].message.content,
                'model': model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"GPT 텍스트 생성 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': model
            }
    
    def analyze_image(self, image_data: bytes, prompt: str = "이 이미지를 분석해주세요.") -> Dict[str, Any]:
        """
        이미지 분석 (GPT-4 Vision)
        """
        try:
            import base64
            
            # 이미지를 base64로 인코딩
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            return {
                'success': True,
                'text': response.choices[0].message.content,
                'model': 'gpt-4-vision-preview',
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"GPT 이미지 분석 오류: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': 'gpt-4-vision-preview'
            }