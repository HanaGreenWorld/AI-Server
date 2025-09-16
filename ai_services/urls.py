"""
AI 서비스 URL 설정
"""
from django.urls import path
from . import views

urlpatterns = [
    # 헬스체크
    path('health/', views.health_check, name='health_check'),
    
    # 기본 AI 서비스
    path('generate-text/', views.generate_text, name='generate_text'),
    path('analyze-image/', views.analyze_image, name='analyze_image'),
    
    # 친환경 관련 AI 서비스
    path('eco/quiz/', views.generate_quiz_question, name='generate_quiz'),
]
