"""
Main entry point for Video Facial Analysis System
"""

import sys
import argparse
import cv2

from src import config
from src.utils import (
    setup_logging,
    get_logger,
    validate_file_exists,
    ensure_directory_exists,
)
from src.video_processor import load_video, get_video_info, extract_frames
from src.face_detector import initialize_detector, detect_faces
from src.emotion_analyzer import load_emotion_model, batch_analyze_emotions
from src.activity_detector import initialize_activity_detector, analyze_motion
from src.anomaly_detector import (
    train_anomaly_model,
    load_anomaly_model,
    save_anomaly_model,
    detect_anomaly,
    classify_anomaly_type,
    create_anomaly_record,
)
from src.summary_generator import create_summary, generate_text_report

# Setup logging
setup_logging()
logger = get_logger(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Sistema de Análise de Expressões Faciais em Vídeo"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=config.INPUT_VIDEO_PATH,
        help=f"Caminho do vídeo de entrada (padrão: {config.INPUT_VIDEO_PATH})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=config.OUTPUT_DIR,
        help=f"Diretório de saída (padrão: {config.OUTPUT_DIR})",
    )
    parser.add_argument(
        "--no-output-video",
        action="store_true",
        help="Não gerar vídeo de saída anotado",
    )

    return parser.parse_args()


def annotate_frame_with_faces(frame, faces, emotions, activity_info, frame_count):
    """Annotate frame with face detections, emotions, and activity"""
    for i, face in enumerate(faces):
        bbox = face.bounding_box
        x, y, w, h = bbox.x, bbox.y, bbox.width, bbox.height

        cv2.rectangle(frame, (x, y), (x + w, y + h), config.BOX_COLOR, 2)

        # Add emotion label if available
        if emotions and i < len(emotions):
            emotion = emotions[i]
            label = f"{emotion.emotion_label.value}: {emotion.confidence:.2f}"
        else:
            label = f"Face {face.face_id}"

        cv2.putText(
            frame,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            config.FONT_SCALE,
            config.TEXT_COLOR,
            config.FONT_THICKNESS,
        )

    # Display activity info in top-left corner
    if activity_info:
        activity_text = f"Activity: {activity_info}"
        cv2.putText(
            frame,
            activity_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

    # Display frame count and face count
    cv2.putText(
        frame,
        f"Frame: {frame_count} | Faces: {len(faces)}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    return frame


def main():
    """Main execution function"""
    args = parse_arguments()

    logger.info("=== Sistema de Análise de Expressões Faciais em Vídeo ===")
    logger.info("Iniciando processamento...")

    # Validate input video exists
    if not validate_file_exists(args.input):
        logger.error(f"Erro: Arquivo de vídeo não encontrado: {args.input}")
        logger.error(
            "Por favor, coloque um arquivo de vídeo MP4 no caminho especificado."
        )
        sys.exit(1)

    # Ensure output directory exists
    ensure_directory_exists(args.output)
    logger.info(f"Diretório de saída: {args.output}")

    try:
        # Load video
        logger.info(f"Carregando vídeo: {args.input}")
        video_capture = load_video(args.input)

        # Get video information
        video_info = get_video_info(video_capture)

        # Display video information
        logger.info("=" * 50)
        logger.info("INFORMAÇÕES DO VÍDEO:")
        logger.info(f"  Total de Frames: {video_info['total_frames']}")
        logger.info(f"  FPS: {video_info['fps']:.2f}")
        logger.info(f"  Resolução: {video_info['width']}x{video_info['height']}")
        logger.info(f"  Duração: {video_info['duration']:.2f} segundos")
        logger.info("=" * 50)

        # Initialize face detector
        logger.info("Inicializando detector de rostos...")
        face_cascade = initialize_detector()

        # Initialize emotion analyzer
        logger.info("Inicializando analisador de emoções...")
        emotion_model = load_emotion_model()

        # Initialize activity detector
        logger.info("Inicializando detector de atividades...")
        activity_config = initialize_activity_detector()

        # Setup video writer if output video is requested
        video_writer = None
        if not args.no_output_video:
            import os

            output_video_path = os.path.join(args.output, "output_video.mp4")
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(
                output_video_path,
                fourcc,
                video_info["fps"],
                (video_info["width"], video_info["height"]),
            )
            logger.info(f"Vídeo de saída será salvo em: {output_video_path}")

        # Extract and process frames
        logger.info("Processando frames do vídeo...")
        import time

        start_time = time.time()

        frame_count = 0
        total_faces_detected = 0
        prev_frame_data = None
        frames_data = []
        anomalies = []

        for frame in extract_frames(video_capture):
            frame_count += 1

            # Detect faces in frame
            faces = detect_faces(frame.image_data, face_cascade)
            total_faces_detected += len(faces)

            # Analyze emotions for detected faces
            emotions = []
            if faces:
                face_images = [face.face_image for face in faces]
                emotions = batch_analyze_emotions(face_images, emotion_model)

            # Analyze motion/activity
            avg_face_area = (
                sum(f.bounding_box.width * f.bounding_box.height for f in faces)
                / len(faces)
                if faces
                else 0.0
            )
            motion_analysis = analyze_motion(
                prev_frame_data,
                frame.image_data,
                num_faces=len(faces),
                avg_face_area=avg_face_area,
                detector_config=activity_config,
            )
            activity_info = motion_analysis.activity_type.value

            # Collect frame data for summary
            frames_data.append(
                {
                    "frame_number": frame_count,
                    "num_faces": len(faces),
                    "emotions": emotions,
                    "activity": activity_info,
                }
            )

            # Annotate frame with face detections, emotions, and activity
            annotated_frame = annotate_frame_with_faces(
                frame.image_data.copy(), faces, emotions, activity_info, frame_count
            )

            # Store current frame for next iteration
            prev_frame_data = frame.image_data.copy()

            # Write annotated frame to output video
            if video_writer is not None:
                video_writer.write(annotated_frame)

            # Log progress every N frames
            if frame_count % config.LOG_EVERY_N_FRAMES == 0:
                logger.info(
                    f"Processados {frame_count} frames, {len(faces)} rostos detectados neste frame"
                )

        # Release video writer
        if video_writer is not None:
            video_writer.release()
            logger.info("Vídeo de saída salvo com sucesso")

        # Calculate processing time
        processing_time = time.time() - start_time

        # Generate summary report
        logger.info("Gerando relatório resumido...")
        import os

        summary = create_summary(
            video_filename=os.path.basename(args.input),
            total_frames=frame_count,
            duration=video_info["duration"],
            fps=video_info["fps"],
            frames_data=frames_data,
            anomalies=anomalies,
            processing_time=processing_time,
        )

        report_path = os.path.join(args.output, "relatorio.txt")
        generate_text_report(summary, report_path)

        # Final summary
        logger.info("=" * 50)
        logger.info("PROCESSAMENTO CONCLUÍDO!")
        logger.info(f"Total de frames processados: {frame_count}")
        logger.info(f"Total de rostos detectados: {total_faces_detected}")
        logger.info(f"Tempo de processamento: {processing_time:.1f}s")
        logger.info(f"Relatório salvo em: {report_path}")
        logger.info("=" * 50)

        return 0

    except FileNotFoundError as e:
        logger.error(f"Erro: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Erro ao processar vídeo: {e}")
        logger.error("O arquivo pode estar corrompido ou em formato não suportado.")
        return 1
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
