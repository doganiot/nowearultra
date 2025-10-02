from django.contrib import admin
from .models import Project, Model3D, ModelAnalysis, ProcessingStep, ProcessedModel


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'user__username')
    date_hierarchy = 'created_at'


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'file_format', 'file_size', 'is_processed', 'uploaded_at')
    list_filter = ('file_format', 'is_processed', 'uploaded_at')
    search_fields = ('name',)
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('file_format', 'file_size')


@admin.register(ModelAnalysis)
class ModelAnalysisAdmin(admin.ModelAdmin):
    list_display = ('model', 'vertices_count', 'faces_count', 'is_watertight', 'topology_status', 'analyzed_at')
    list_filter = ('is_watertight', 'topology_status', 'analyzed_at')
    search_fields = ('model__name',)
    date_hierarchy = 'analyzed_at'


@admin.register(ProcessingStep)
class ProcessingStepAdmin(admin.ModelAdmin):
    list_display = ('model', 'step_type', 'success', 'execution_time', 'created_at')
    list_filter = ('step_type', 'success', 'created_at')
    search_fields = ('model__name',)
    date_hierarchy = 'created_at'


@admin.register(ProcessedModel)
class ProcessedModelAdmin(admin.ModelAdmin):
    list_display = ('original_model', 'final_vertices_count', 'final_faces_count', 'quality_score', 'is_printable', 'created_at')
    list_filter = ('is_printable', 'created_at')
    search_fields = ('original_model__name',)
    date_hierarchy = 'created_at'
