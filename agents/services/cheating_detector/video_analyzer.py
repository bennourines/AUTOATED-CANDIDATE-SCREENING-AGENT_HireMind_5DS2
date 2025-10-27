"""
Video Analysis for Cheating Detection.

Analyzes:
- Eye gaze patterns (reading, looking away)
- Head pose (looking at secondary screen)
- Facial consistency (same person throughout)
- Attention focus and engagement
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, List, Optional, Tuple
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class VideoAnalyzer:
    """
    Advanced video analysis for behavioral cheating detection.
    
    Detects:
    1. Reading patterns (horizontal eye movements)
    2. Looking away from camera (poor focus)
    3. Head pose anomalies (looking at secondary screen)
    4. Face changes (impersonation)
    """
    
    def __init__(self):
        """Initialize video analyzer with MediaPipe."""
        logger.info("Initializing Video Analyzer...")
        
        # MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # MediaPipe Face Detection (for consistency check)
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.5
        )
        
        # Eye landmarks (MediaPipe Face Mesh indices)
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        # Head pose landmarks
        self.NOSE_TIP = 1
        self.CHIN = 152
        self.LEFT_EYE_CORNER = 263
        self.RIGHT_EYE_CORNER = 33
        
        logger.info("✅ Video Analyzer initialized")
    
    def analyze_gaze_behavior(
        self,
        video_path: str,
        sample_rate: int = 15
    ) -> Dict:
        """
        Comprehensive gaze behavior analysis.
        
        Args:
            video_path: Path to video file
            sample_rate: Analyze every Nth frame
            
        Returns:
            Gaze analysis with cheating indicators
        """
        logger.info(f"Analyzing gaze behavior: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Failed to open video: {video_path}")
            return self._get_default_gaze_result()
        
        # Analysis accumulators
        gaze_directions = []
        camera_focus_frames = 0
        total_frames = 0
        reading_pattern_count = 0
        erratic_movement_count = 0
        
        # Gaze history for pattern detection
        gaze_history = []
        
        frame_count = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                frame_count += 1
                
                # Sample frames
                if frame_count % sample_rate != 0:
                    continue
                
                total_frames += 1
                
                # Analyze frame
                result = self._analyze_frame_gaze(frame)
                
                if result:
                    gaze_directions.append(result['direction'])
                    
                    if result['looking_at_camera']:
                        camera_focus_frames += 1
                    
                    # Store gaze ratio for pattern detection
                    gaze_history.append(result['gaze_ratio'])
                    
                    # Detect reading pattern (horizontal eye movement)
                    if len(gaze_history) >= 5:
                        if self._is_reading_pattern(gaze_history[-5:]):
                            reading_pattern_count += 1
                    
                    # Detect erratic movements
                    if len(gaze_history) >= 3:
                        if self._is_erratic_movement(gaze_history[-3:]):
                            erratic_movement_count += 1
        
        finally:
            cap.release()
        
        logger.info(f"Analyzed {total_frames} frames")
        
        # Calculate metrics
        camera_focus_ratio = camera_focus_frames / total_frames if total_frames > 0 else 0
        reading_pattern_ratio = reading_pattern_count / total_frames if total_frames > 0 else 0
        erratic_ratio = erratic_movement_count / total_frames if total_frames > 0 else 0
        
        # Direction distribution
        direction_counts = defaultdict(int)
        for direction in gaze_directions:
            direction_counts[direction] += 1
        
        return {
            'camera_focus_ratio': round(camera_focus_ratio, 3),
            'reading_pattern_detected': reading_pattern_ratio > 0.2,  # 20% threshold
            'reading_pattern_ratio': round(reading_pattern_ratio, 3),
            'erratic_gaze': erratic_ratio > 0.3,  # 30% threshold
            'erratic_ratio': round(erratic_ratio, 3),
            'direction_distribution': dict(direction_counts),
            'total_frames_analyzed': total_frames,
            'gaze_timeline': gaze_history[:100]  # Sample for visualization
        }
    
    def _analyze_frame_gaze(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Analyze gaze in single frame.
        
        Args:
            frame: Video frame (BGR)
            
        Returns:
            Gaze analysis results or None
        """
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect face
            results = self.face_mesh.process(rgb_frame)
            
            if not results.multi_face_landmarks:
                return None
            
            landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape
            
            # Extract iris positions
            left_iris_points = [
                (landmarks.landmark[idx].x * w, landmarks.landmark[idx].y * h)
                for idx in self.LEFT_IRIS
            ]
            right_iris_points = [
                (landmarks.landmark[idx].x * w, landmarks.landmark[idx].y * h)
                for idx in self.RIGHT_IRIS
            ]
            
            left_iris_center = np.mean(left_iris_points, axis=0)
            right_iris_center = np.mean(right_iris_points, axis=0)
            
            # Extract eye corners
            left_eye_corners = [
                (landmarks.landmark[263].x * w, landmarks.landmark[263].y * h),  # Left
                (landmarks.landmark[362].x * w, landmarks.landmark[362].y * h)   # Right
            ]
            right_eye_corners = [
                (landmarks.landmark[133].x * w, landmarks.landmark[133].y * h),  # Left
                (landmarks.landmark[33].x * w, landmarks.landmark[33].y * h)     # Right
            ]
            
            # Calculate gaze ratios
            left_ratio = self._calculate_gaze_ratio(
                left_iris_center, left_eye_corners[0], left_eye_corners[1]
            )
            right_ratio = self._calculate_gaze_ratio(
                right_iris_center, right_eye_corners[0], right_eye_corners[1]
            )
            
            avg_ratio = (left_ratio + right_ratio) / 2
            
            # Determine direction
            if avg_ratio < 0.3:
                direction = "right"
                looking_at_camera = False
            elif avg_ratio > 0.7:
                direction = "left"
                looking_at_camera = False
            else:
                direction = "center"
                looking_at_camera = True
            
            return {
                'direction': direction,
                'looking_at_camera': looking_at_camera,
                'gaze_ratio': avg_ratio,
                'left_ratio': left_ratio,
                'right_ratio': right_ratio
            }
            
        except Exception as e:
            logger.debug(f"Frame gaze analysis failed: {e}")
            return None
    
    def _calculate_gaze_ratio(
        self,
        iris_center: Tuple[float, float],
        eye_left: Tuple[float, float],
        eye_right: Tuple[float, float]
    ) -> float:
        """
        Calculate gaze ratio (0=far right, 0.5=center, 1=far left).
        """
        eye_width = abs(eye_right[0] - eye_left[0])
        
        if eye_width == 0:
            return 0.5
        
        iris_distance_from_right = abs(iris_center[0] - eye_right[0])
        ratio = iris_distance_from_right / eye_width
        
        return np.clip(ratio, 0, 1)
    
    def _is_reading_pattern(self, gaze_ratios: List[float]) -> bool:
        """
        Detect reading pattern (left-to-right horizontal eye movement).
        
        Reading pattern: smooth left→right or right→left movement
        
        Args:
            gaze_ratios: Last N gaze ratios (0-1)
            
        Returns:
            True if reading pattern detected
        """
        if len(gaze_ratios) < 3:
            return False
        
        # Check for monotonic increase or decrease
        diffs = np.diff(gaze_ratios)
        
        # Consistent left movement (increasing ratios)
        left_movement = all(d > 0.05 for d in diffs)
        
        # Consistent right movement (decreasing ratios)
        right_movement = all(d < -0.05 for d in diffs)
        
        # Reading involves large horizontal sweeps
        movement_range = max(gaze_ratios) - min(gaze_ratios)
        large_sweep = movement_range > 0.4
        
        return (left_movement or right_movement) and large_sweep
    
    def _is_erratic_movement(self, gaze_ratios: List[float]) -> bool:
        """
        Detect erratic eye movements (rapid, non-natural changes).
        
        Args:
            gaze_ratios: Last N gaze ratios
            
        Returns:
            True if erratic movement detected
        """
        if len(gaze_ratios) < 3:
            return False
        
        # Calculate changes
        diffs = np.diff(gaze_ratios)
        
        # Rapid changes (> 0.3 change between frames)
        rapid_changes = sum(abs(d) > 0.3 for d in diffs)
        
        # Erratic = multiple rapid changes
        return rapid_changes >= 2
    
    def analyze_head_pose(
        self,
        video_path: str,
        sample_rate: int = 30
    ) -> Dict:
        """
        Analyze head pose for suspicious angles.
        
        Detects:
        - Head turned to secondary screen
        - Unusual head angles
        
        Args:
            video_path: Path to video
            sample_rate: Analyze every Nth frame
            
        Returns:
            Head pose analysis
        """
        logger.info(f"Analyzing head pose: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Failed to open video: {video_path}")
            return {'error': 'Failed to open video'}
        
        # Analysis accumulators
        yaw_angles = []  # Left-right rotation
        pitch_angles = []  # Up-down rotation
        suspicious_pose_count = 0
        total_frames = 0
        
        frame_count = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                frame_count += 1
                
                if frame_count % sample_rate != 0:
                    continue
                
                total_frames += 1
                
                # Analyze head pose
                result = self._estimate_head_pose(frame)
                
                if result:
                    yaw_angles.append(result['yaw'])
                    pitch_angles.append(result['pitch'])
                    
                    # Check for suspicious angles
                    if abs(result['yaw']) > 30 or abs(result['pitch']) > 25:
                        suspicious_pose_count += 1
        
        finally:
            cap.release()
        
        suspicious_pose_ratio = suspicious_pose_count / total_frames if total_frames > 0 else 0
        
        return {
            'avg_yaw': round(float(np.mean(yaw_angles)), 2) if yaw_angles else 0,
            'avg_pitch': round(float(np.mean(pitch_angles)), 2) if pitch_angles else 0,
            'suspicious_pose_ratio': round(suspicious_pose_ratio, 3),
            'looking_at_secondary_screen': suspicious_pose_ratio > 0.3,
            'total_frames_analyzed': total_frames
        }
    
    def _estimate_head_pose(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Estimate head pose angles from facial landmarks.
        
        Returns:
            Dict with yaw (left-right), pitch (up-down), roll angles
        """
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if not results.multi_face_landmarks:
                return None
            
            landmarks = results.multi_face_landmarks[0]
            h, w, _ = frame.shape
            
            # Key landmarks for pose estimation
            nose = np.array([
                landmarks.landmark[self.NOSE_TIP].x * w,
                landmarks.landmark[self.NOSE_TIP].y * h
            ])
            
            chin = np.array([
                landmarks.landmark[self.CHIN].x * w,
                landmarks.landmark[self.CHIN].y * h
            ])
            
            left_eye = np.array([
                landmarks.landmark[self.LEFT_EYE_CORNER].x * w,
                landmarks.landmark[self.LEFT_EYE_CORNER].y * h
            ])
            
            right_eye = np.array([
                landmarks.landmark[self.RIGHT_EYE_CORNER].x * w,
                landmarks.landmark[self.RIGHT_EYE_CORNER].y * h
            ])
            
            # Calculate yaw (left-right rotation)
            eye_center = (left_eye + right_eye) / 2
            horizontal_diff = nose[0] - eye_center[0]
            eye_distance = np.linalg.norm(right_eye - left_eye)
            
            yaw = np.degrees(np.arctan2(horizontal_diff, eye_distance)) * 2
            
            # Calculate pitch (up-down rotation)
            vertical_diff = nose[1] - eye_center[1]
            pitch = np.degrees(np.arctan2(vertical_diff, eye_distance)) * 2
            
            return {
                'yaw': float(yaw),
                'pitch': float(pitch),
                'roll': 0.0  # Simplified
            }
            
        except Exception as e:
            logger.debug(f"Head pose estimation failed: {e}")
            return None
    
    def detect_face_consistency(
        self,
        video_path: str,
        sample_rate: int = 60
    ) -> Dict:
        """
        Verify same person throughout video (detect impersonation).
        
        Args:
            video_path: Path to video
            sample_rate: Analyze every Nth frame
            
        Returns:
            Face consistency analysis
        """
        logger.info(f"Checking face consistency: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Failed to open video: {video_path}")
            return {'error': 'Failed to open video'}
        
        # Store face embeddings
        face_embeddings = []
        
        frame_count = 0
        analyzed_count = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                frame_count += 1
                
                if frame_count % sample_rate != 0:
                    continue
                
                # Extract face embedding (simplified - use face recognition in production)
                embedding = self._extract_face_embedding(frame)
                
                if embedding is not None:
                    face_embeddings.append(embedding)
                    analyzed_count += 1
        
        finally:
            cap.release()
        
        # Check consistency
        if len(face_embeddings) < 2:
            return {
                'consistent': True,
                'confidence': 0.5,
                'warning': 'Insufficient frames for consistency check'
            }
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(face_embeddings) - 1):
            sim = self._cosine_similarity(face_embeddings[i], face_embeddings[i+1])
            similarities.append(sim)
        
        avg_similarity = float(np.mean(similarities))
        min_similarity = float(np.min(similarities))
        
        # Consistent if high average similarity
        is_consistent = avg_similarity > 0.8 and min_similarity > 0.6
        
        return {
            'consistent': is_consistent,
            'avg_similarity': round(avg_similarity, 3),
            'min_similarity': round(min_similarity, 3),
            'frames_analyzed': analyzed_count,
            'warning': None if is_consistent else 'Face inconsistency detected - possible impersonation'
        }
    
    def _extract_face_embedding(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract face embedding (simplified placeholder).
        
        In production, use DeepFace or face_recognition library.
        """
        try:
            # Simplified: use pixel histogram as embedding
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_region = gray[100:300, 100:300]  # Approximate face region
            
            hist = cv2.calcHist([face_region], [0], None, [64], [0, 256])
            embedding = hist.flatten()
            embedding = embedding / np.linalg.norm(embedding)  # Normalize
            
            return embedding
            
        except Exception as e:
            logger.debug(f"Face embedding failed: {e}")
            return None
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def _get_default_gaze_result(self) -> Dict:
        """Return default gaze result when analysis fails."""
        return {
            'camera_focus_ratio': 0.0,
            'reading_pattern_detected': False,
            'reading_pattern_ratio': 0.0,
            'erratic_gaze': False,
            'erratic_ratio': 0.0,
            'direction_distribution': {},
            'total_frames_analyzed': 0,
            'gaze_timeline': []
        }

# Global instance
video_analyzer = VideoAnalyzer()