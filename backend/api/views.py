from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Assignment, Submission, User
from .serializers import AssignmentSerializer, SubmissionSerializer, UserSerializer
from ai_engine.utils import check_plagiarism, generate_feedback

from rest_framework.decorators import action
from django.contrib.auth import authenticate

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({
                "id": user.id,
                "username": user.username,
                "role": user.role
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        submission = serializer.save()
        
        # Extract text from PDF if uploaded
        if submission.file_upload and not submission.text_content:
            try:
                from pdfminer.high_level import extract_text
                submission.text_content = extract_text(submission.file_upload.path)
                submission.save()
            except Exception as e:
                print(f"Error extracting PDF: {e}")
        
        # Trigger AI Evaluation
        existing_submissions = Submission.objects.filter(assignment=submission.assignment).exclude(id=submission.id)
        existing_texts = [s.text_content for s in existing_submissions if s.text_content]
        
        if submission.text_content:
            score = check_plagiarism(submission.text_content, existing_texts)
            text_len = len(submission.text_content.split())
            feedback = generate_feedback(score, text_len)
            
            # Simple grading logic: 100 - (plagiarism_score) + bonus for length
            grade = max(0, min(100, 100 - int(score) + (min(20, text_len // 10))))
            
            submission.plagiarism_score = score
            submission.feedback = feedback
            submission.grade = grade
            submission.is_evaluated = True
            submission.save()
