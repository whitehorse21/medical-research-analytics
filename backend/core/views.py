from django.db.models import Avg, Count, Max, Min, Q
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import LiteratureArticle, Participant, Study
from .serializers import (
    LiteratureArticleSerializer,
    ParticipantSerializer,
    StudySerializer,
)


class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all().order_by("-created_at")
    serializer_class = StudySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "condition", "status"]
    ordering_fields = ["created_at", "start_date", "end_date", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get("status", None)
        condition_filter = self.request.query_params.get("condition", None)

        if status_filter:
            queryset = queryset.filter(status__icontains=status_filter)
        if condition_filter:
            queryset = queryset.filter(condition__icontains=condition_filter)

        return queryset

    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        """Get all participants for a specific study"""
        study = self.get_object()
        participants = study.participants.all().order_by("-enrolled_on")
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def stats(self, request):
        """Get statistics about studies"""
        from django.utils import timezone
        from datetime import timedelta
        
        total_studies = Study.objects.count()
        by_status = {}
        for status_val in ["planning", "recruiting", "active", "completed", "cancelled"]:
            by_status[status_val] = Study.objects.filter(status=status_val).count()
        
        # Additional metrics
        active_studies = Study.objects.filter(status="active").count()
        completed_studies = Study.objects.filter(status="completed").count()
        completion_rate = (completed_studies / total_studies * 100) if total_studies > 0 else 0
        
        # Recent studies (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_studies = Study.objects.filter(created_at__gte=thirty_days_ago).count()
        
        # Studies with dates
        studies_with_dates = Study.objects.exclude(start_date__isnull=True).count()
        ongoing_studies = Study.objects.filter(
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).count()

        return Response({
            "total_studies": total_studies,
            "by_status": by_status,
            "active_studies": active_studies,
            "completed_studies": completed_studies,
            "completion_rate": round(completion_rate, 1),
            "recent_studies": recent_studies,
            "studies_with_dates": studies_with_dates,
            "ongoing_studies": ongoing_studies,
        })


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all().order_by("-enrolled_on")
    serializer_class = ParticipantSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["code", "study__title"]
    ordering_fields = ["enrolled_on", "age", "code"]
    ordering = ["-enrolled_on"]

    def get_queryset(self):
        queryset = super().get_queryset()
        study_id = self.request.query_params.get("study", None)
        sex_filter = self.request.query_params.get("sex", None)
        min_age = self.request.query_params.get("min_age", None)
        max_age = self.request.query_params.get("max_age", None)

        if study_id:
            queryset = queryset.filter(study_id=study_id)
        if sex_filter:
            queryset = queryset.filter(sex__icontains=sex_filter)
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        if max_age:
            queryset = queryset.filter(age__lte=max_age)

        return queryset

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def stats(self, request):
        """Get statistics about participants"""
        from django.utils import timezone
        from datetime import timedelta
        
        total_participants = Participant.objects.count()
        by_sex = {}
        for sex_val in ["M", "F", "Male", "Female", "Other"]:
            count = Participant.objects.filter(sex__icontains=sex_val).count()
            if count > 0:
                by_sex[sex_val] = count

        avg_age = Participant.objects.aggregate(
            avg_age=Avg("age")
        )["avg_age"] or 0
        
        # Additional metrics
        min_age = Participant.objects.aggregate(min_age=Min("age"))["min_age"] or 0
        max_age = Participant.objects.aggregate(max_age=Max("age"))["max_age"] or 0
        
        # Participants by age groups
        age_groups = {
            "0-18": Participant.objects.filter(age__lte=18).count(),
            "19-35": Participant.objects.filter(age__gte=19, age__lte=35).count(),
            "36-50": Participant.objects.filter(age__gte=36, age__lte=50).count(),
            "51-65": Participant.objects.filter(age__gte=51, age__lte=65).count(),
            "65+": Participant.objects.filter(age__gt=65).count(),
        }
        
        # Recent enrollments (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_enrollments = Participant.objects.filter(enrolled_on__gte=thirty_days_ago.date()).count()
        
        # Average participants per study
        from django.db.models import Count
        studies_with_participants = Study.objects.annotate(
            participant_count=Count("participants")
        ).exclude(participant_count=0)
        avg_per_study = (
            studies_with_participants.aggregate(avg=Avg("participant_count"))["avg"] or 0
        )

        return Response({
            "total_participants": total_participants,
            "by_sex": by_sex,
            "average_age": round(avg_age, 2) if avg_age else 0,
            "min_age": min_age,
            "max_age": max_age,
            "age_groups": age_groups,
            "recent_enrollments": recent_enrollments,
            "average_per_study": round(avg_per_study, 1) if avg_per_study else 0,
        })


class LiteratureArticleViewSet(viewsets.ModelViewSet):
    queryset = LiteratureArticle.objects.all().order_by("-created_at")
    serializer_class = LiteratureArticleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "authors", "journal", "abstract"]
    ordering_fields = ["year", "created_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        year_filter = self.request.query_params.get("year", None)
        journal_filter = self.request.query_params.get("journal", None)
        author_filter = self.request.query_params.get("author", None)

        if year_filter:
            queryset = queryset.filter(year=year_filter)
        if journal_filter:
            queryset = queryset.filter(journal__icontains=journal_filter)
        if author_filter:
            queryset = queryset.filter(authors__icontains=author_filter)

        return queryset

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def stats(self, request):
        """Get statistics about literature articles"""
        from django.utils import timezone
        from datetime import timedelta
        
        total_articles = LiteratureArticle.objects.count()
        by_year = dict(
            LiteratureArticle.objects.values("year")
            .annotate(count=Count("id"))
            .order_by("-year")
            .values_list("year", "count")[:10]
        )

        journals = (
            LiteratureArticle.objects.values("journal")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        
        # Additional metrics
        current_year = timezone.now().year
        current_year_articles = LiteratureArticle.objects.filter(year=current_year).count()
        last_year_articles = LiteratureArticle.objects.filter(year=current_year - 1).count()
        
        # Articles with DOI
        articles_with_doi = LiteratureArticle.objects.exclude(doi__isnull=True).exclude(doi="").count()
        doi_coverage = (articles_with_doi / total_articles * 100) if total_articles > 0 else 0
        
        # Recent articles (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_articles = LiteratureArticle.objects.filter(created_at__gte=thirty_days_ago).count()
        
        # Year range
        year_range = LiteratureArticle.objects.aggregate(
            min_year=Min("year"),
            max_year=Max("year")
        )

        return Response({
            "total_articles": total_articles,
            "top_years": by_year,
            "top_journals": list(journals),
            "current_year_articles": current_year_articles,
            "last_year_articles": last_year_articles,
            "articles_with_doi": articles_with_doi,
            "doi_coverage": round(doi_coverage, 1),
            "recent_articles": recent_articles,
            "year_range": year_range,
        })