import parselmouth
from parselmouth.praat import call
from fastapi import UploadFile, HTTPException
import tempfile
import os
from typing import Dict, Any
class PraatService:
    async def analyze_audio(self, audio_file: UploadFile) -> Dict[str, Any]:
        tmp_audio_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, 
                                            suffix=".flac") as tmp_file:
                content = await audio_file.read()
                if not content:
                        os.remove(tmp_file.name)
                        raise HTTPException(status_code=400, 
                                            detail="Audio file is empty.")
                tmp_file.write(content)
                tmp_audio_file_path = tmp_file.name
                
            print(f"Attempting to load sound from: {tmp_audio_file_path}")
            sound = parselmouth.Sound(tmp_audio_file_path)
            duration_s = sound.duration
            print(f"Sound loaded. Duration: {duration_s}s") 

            pitch_floor = 75.0 
            pitch_ceiling = 600.0            
            
            print(f"Calling sound.to_pitch() with pitch_floor={pitch_floor}, "
                f"pitch_ceiling={pitch_ceiling}")
            
            pitch = sound.to_pitch(pitch_floor=pitch_floor,
                                    pitch_ceiling=pitch_ceiling)
            mean_pitch_fq = None
            if pitch.get_number_of_frames() > 0:
                mean_pitch_fq = call(pitch, "Get mean", 0, 0, "Hertz")
                
            intensity = sound.to_intensity()
            mean_intensity_db = None
            if intensity.get_number_of_frames() > 0:
                mean_intensity_db = call(intensity, "Get mean", 0, 0, "dB")
                
            jitter_local_percent = None
            shimmer_local_db = None
            if pitch.get_number_of_frames() > 0:
                point_process = call([sound, pitch], "To PointProcess (cc)")
                if call(point_process, "Get number of points") > 0:
                    jitter_raw = call(point_process, "Get jitter (local)",
                                    0, 0, 0.0001, 0.02, 1.3)
                    if jitter_raw is not None:
                        jitter_local_percent = jitter_raw * 100
                        
                    shimmer_raw_db = call([sound, point_process], 
                                        "Get shimmer (local_dB)", 
                                        0, 0, 0.0001, 0.02, 1.3, 1.6)
                    if shimmer_raw_db is not None:
                        shimmer_local_db = shimmer_raw_db
                else:
                    print("No points found in the point process.")
            else:
                print("No frames found in the pitch object.")
                
            f1_mid_hz = None
            f2_mid_hz = None
            
            try:
                formant = sound.to_formant_burg(time_step=0.01,
                max_number_of_formants=5, maximum_formant=5500,
                window_length=0.025, pre_emphasis_from=50)
                mid_time = duration_s / 2.0
                f1_mid_hz = call(formant, "Get value at time", 1, mid_time,
                                "Hertz", "Linear")
                f2_mid_hz = call(formant, "Get value at time", 2, mid_time,
                                "Hertz", "Linear")
            except parselmouth.PraatError as e:
                print(f"Cannot calculate formants: {e}")
            
            except Exception as e:
                print(f"Unexpected error calculating formants: {e}")
            
            
            results = {
                "pitch_mean_hz": round(mean_pitch_fq, 2) 
                if mean_pitch_fq is not None else None,
                "intensity_mean_db": round(mean_intensity_db, 2)
                if mean_intensity_db is not None else None,
                "jitter_local_percent": round(jitter_local_percent, 4)
                if jitter_local_percent is not None else None,
                "shimmer_local_db": round(shimmer_local_db, 4) 
                if shimmer_local_db is not None else None,
                "f1_mid_hz": round(f1_mid_hz, 2) 
                if f1_mid_hz is not None else None,
                "f2_mid_hz": round(f2_mid_hz, 2)
                if f2_mid_hz is not None else None,
                "duration_s": round(duration_s, 3) 
                if duration_s is not None else None,
                "message": "Audio analysis completed successfully."
            }
            return results
        
        except parselmouth.PraatError as e:
            print(f"Praat error: {e}")
            raise
        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        
        finally:
            if tmp_audio_file_path and os.path.exists(tmp_audio_file_path):
                try:
                    os.remove(tmp_audio_file_path)
                except Exception as e:
                    print(f"Error removing temporary file: {e}")
                    
def get_praat_service():
    return PraatService()