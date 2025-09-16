"""
AI 서비스 뷰
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

from .services.gemini_service import GeminiService
from .services.gpt_service import GPTService

logger = logging.getLogger(__name__)

@api_view(['GET'])
def health_check(request):
    """AI 서버 상태 확인"""
    return JsonResponse({
        'status': 'UP',
        'service': 'ai-server',
        'version': '1.0.0',
        'available_services': ['gemini', 'gpt']
    })

@api_view(['POST'])
@parser_classes([JSONParser])
def generate_text(request):
    """텍스트 생성 (Gemini 또는 GPT)"""
    try:
        data = request.data
        prompt = data.get('prompt')
        model = data.get('model', 'gemini')  # 'gemini' 또는 'gpt'
        
        if not prompt:
            return Response({
                'success': False,
                'error': 'prompt는 필수입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if model == 'gemini':
            service = GeminiService()
            result = service.generate_text(prompt)
        elif model == 'gpt':
            service = GPTService()
            result = service.generate_text(prompt)
        else:
            return Response({
                'success': False,
                'error': '지원하지 않는 모델입니다. (gemini, gpt)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result)
        
    except Exception as e:
        logger.error(f"텍스트 생성 오류: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def analyze_image(request):
    """이미지 분석 (Gemini 또는 GPT)"""
    try:
        model = request.data.get('model', 'gemini')
        prompt = request.data.get('prompt', '이 이미지를 분석해주세요.')
        
        if 'image' not in request.FILES:
            return Response({
                'success': False,
                'error': '이미지 파일이 필요합니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        image_data = image_file.read()
        
        if model == 'gemini':
            service = GeminiService()
            result = service.analyze_image(image_data, prompt)
        elif model == 'gpt':
            service = GPTService()
            result = service.analyze_image(image_data, prompt)
        else:
            return Response({
                'success': False,
                'error': '지원하지 않는 모델입니다. (gemini, gpt)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result)
        
    except Exception as e:
        logger.error(f"이미지 분석 오류: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@parser_classes([JSONParser])
@csrf_exempt
def generate_quiz_question(request):
    """퀴즈 문제 생성 (Gemini)"""
    try:
        data = request.data
        
        service = GeminiService()
        result = service.generate_quiz_question()
        
        return Response(result)
        
    except Exception as e:
        logger.error(f"퀴즈 생성 오류: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)