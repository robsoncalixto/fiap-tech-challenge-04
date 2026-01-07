"""
Summary report generation module
"""

from dataclasses import dataclass
from typing import List, Dict
from collections import Counter

from src.utils import get_logger

logger = get_logger(__name__)


@dataclass
class AnalysisSummary:
    """Represents complete analysis summary"""

    video_filename: str
    total_frames: int
    duration: float
    fps: float
    total_faces_detected: int
    emotion_distribution: Dict[str, int]
    activity_distribution: Dict[str, int]
    processing_time: float


def create_summary(
    video_filename: str,
    total_frames: int,
    duration: float,
    fps: float,
    frames_data: List[Dict],
    processing_time: float,
) -> AnalysisSummary:
    """
    Create analysis summary from collected frame data

    Args:
        video_filename: Name of the video file
        total_frames: Total number of frames processed
        duration: Video duration in seconds
        fps: Frames per second
        frames_data: List of dictionaries with frame analysis data
        processing_time: Total processing time in seconds

    Returns:
        AnalysisSummary object
    """
    # Count total faces
    total_faces = sum(frame.get("num_faces", 0) for frame in frames_data)

    # Aggregate emotion statistics
    emotion_counts = Counter()
    for frame in frames_data:
        emotions = frame.get("emotions", [])
        for emotion in emotions:
            if hasattr(emotion, "emotion_label"):
                emotion_counts[emotion.emotion_label.value] += 1

    # Aggregate activity statistics
    activity_counts = Counter()
    for frame in frames_data:
        activity = frame.get("activity", None)
        if activity:
            activity_counts[activity] += 1

    summary = AnalysisSummary(
        video_filename=video_filename,
        total_frames=total_frames,
        duration=duration,
        fps=fps,
        total_faces_detected=total_faces,
        emotion_distribution=dict(emotion_counts),
        activity_distribution=dict(activity_counts),
        processing_time=processing_time,
    )

    logger.info("Analysis summary created successfully")
    return summary


def generate_text_report(summary: AnalysisSummary, output_path: str) -> None:
    """
    Generate formatted text report and save to file

    Args:
        summary: AnalysisSummary object
        output_path: Path to save the report file
    """
    lines = []

    # Header
    lines.append("=" * 60)
    lines.append("RELATÓRIO DE ANÁLISE DE VÍDEO")
    lines.append("=" * 60)
    lines.append("")

    # Video information
    lines.append(f"Arquivo: {summary.video_filename}")
    lines.append(f"Total de Frames: {summary.total_frames}")
    lines.append(f"Duração: {summary.duration:.2f} segundos")
    lines.append(f"FPS: {summary.fps:.2f}")
    lines.append("")

    # Face detection statistics
    lines.append("--- DETECÇÃO FACIAL ---")
    lines.append(f"Total de Rostos Detectados: {summary.total_faces_detected}")
    lines.append("")

    # Emotion analysis statistics
    if summary.emotion_distribution:
        lines.append("--- ANÁLISE DE EMOÇÕES ---")
        total_emotions = sum(summary.emotion_distribution.values())

        for emotion, count in sorted(
            summary.emotion_distribution.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_emotions * 100) if total_emotions > 0 else 0
            lines.append(f"{emotion}: {count} ({percentage:.1f}%)")
        lines.append("")

    # Activity detection statistics
    if summary.activity_distribution:
        lines.append("--- DETECÇÃO DE ATIVIDADES ---")
        total_activities = sum(summary.activity_distribution.values())

        for activity, count in sorted(
            summary.activity_distribution.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_activities * 100) if total_activities > 0 else 0
            lines.append(f"{activity}: {count} frames ({percentage:.1f}%)")
        lines.append("")

    # Processing information
    lines.append(f"Tempo de Processamento: {summary.processing_time:.1f} segundos")
    lines.append("")
    lines.append("=" * 60)

    # Write to file
    report_text = "\n".join(lines)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        logger.info(f"Relatório salvo em: {output_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar relatório: {e}")


def format_timestamp(seconds: float) -> str:
    """
    Format seconds to MM:SS.s format

    Args:
        seconds: Time in seconds

    Returns:
        Formatted timestamp string
    """
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes:02d}:{secs:04.1f}"
