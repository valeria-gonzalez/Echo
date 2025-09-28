from parselmouth.praat import run_file
import numpy as np
from scipy.stats import ks_2samp, ttest_ind
import os

class SpeechAnalyzer:
    """Class for the analysis of voice without the need of a transcription."""

    def _analyze_audio(self, audio_filename: str, audio_dir: str):
        """Internal helper to run Praat analysis and extract result array.
        
        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.
        """
        full_audio_path = os.path.join(audio_dir, audio_filename)
        
        # Get the path to this script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Build absolute path to myspsolution.praat in analysis/
        praat_script_path = os.path.join(base_path, "myspsolution.praat")
        
        textgrid_path = f"{audio_dir}/{audio_filename}.TextGrid"  # Expected output from Praat

        try:
            result = run_file(
                praat_script_path, -20, 2, 0.3, "yes",
                full_audio_path, audio_dir + "/", 80, 400, 0.01, capture_output=True
            )
            
            parsed_textgrid = str(result[1]).strip().split()
            
            # Clean up: delete the .TextGrid file if it exists
            if os.path.isfile(textgrid_path):
                os.remove(textgrid_path)

            return parsed_textgrid
        except Exception as e:
            print(f"Error for PRAAT analyzing audio, check analyzer : {e}")
            return None

    def get_syllable_count(self, audio_filename: str, audio_dir: str) -> int:
        """Detect and count number of syllables.

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            int: Number of syllables.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        return int(data[0]) if data else None

    def get_pauses_count(self, audio_filename: str, audio_dir: str) -> int:
        """Detect and count number of pauses and fillers.

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            int: Number of pauses and fillers.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        return int(data[1]) if data else None

    def get_rate_of_speech(self, audio_filename: str, audio_dir: str) -> int:
        """Measure the total number of syllables spoken per second (including 
        pauses and fillers).

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            int: Number of syllables spoken per second.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        return int(data[2]) if data else None

    def get_articulation_rate(self, audio_filename: str, audio_dir: str) -> int:
        """Measure the total number of syllables spoken per second 
        (excluding pauses and fillers).

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            int: Number of syllables articulated per second.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        return int(data[3]) if data else None

    def get_speaking_time(self, audio_filename: str, audio_dir: str) -> float:
        """Measure speaking time (excluding fillers and pauses).

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            float: Number of seconds of only speaking duration without pauses.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        return float(data[4]) if data else None

    def get_total_speaking_time(self, audio_filename: str, audio_dir: str) -> float:
        """Measure speaking time (including fillers and pauses).

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            float: Number of seconds of only speaking duration with pauses.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        return float(data[5]) if data else None

    def get_speaking_to_total_time_ratio(self, audio_filename: str, audio_dir: str) -> float:
        """Measure ratio between speaking duration and total speaking duration.

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            float: Ratio (speaking duration)/(original duration).
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        return float(data[6]) if data else None

    def get_overview(self, audio_filename: str, audio_dir: str) -> dict:
        """Get total overview of audio properties. Includes number of syllables,
        number of pauses, rate of speech, articulation rate, speaking duration,
        original duration and ratio.

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            dict: Overview of audio properties.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        if not data:
            print("Getting PRAAT analysis failed ;(")
            return None
        
        print("Getting PRAAT analysis success!")
        return {
            "number_of_syllables": int(data[0]),
            "number_of_pauses": int(data[1]),
            "speech_rate": float(data[2]),
            "articulation_rate": float(data[3]),
            "speaking_duration": float(data[4]),
            "total_duration": float(data[5]),
            "ratio": float(data[6])
        }

    def get_gender_and_mood(self, audio_filename: str, audio_dir: str) -> dict:
        """Recognize gender and mood of speech.

        Args:
            audio_filename (str): Filename with extension.
            audio_dir (str): Filepath where the audio is.

        Returns:
            dict: Gender and mood of speech.
        """
        data = self._analyze_audio(audio_filename, audio_dir)
        if not data:
            return None

        f0_mean = float(data[8])
        f0_median = float(data[7])

        # Gender/mood classification threshold
        if f0_median <= 114:
            g, j = 101, 3.4
        elif f0_median <= 135:
            g, j = 128, 4.35
        elif f0_median <= 163:
            g, j = 142, 4.85
        elif f0_median <= 197:
            g, j = 182, 2.7
        elif f0_median <= 226:
            g, j = 213, 4.5
        elif f0_median > 226:
            g, j = 239, 5.3
        else:
            print("Voice not recognized")
            return None

        def compare_distributions(a, b, c, d):
            d1 = np.random.wald(a, 1, 1000)
            d2 = np.random.wald(b, 1, 1000)
            ks = ks_2samp(d1, d2)
            c1 = np.random.normal(a, c, 1000)
            c2 = np.random.normal(b, d, 1000)
            t_stat = ttest_ind(c1, c2)
            return [ks[0], ks[1], abs(t_stat[0]), t_stat[1]]

        # Repeated statistical testing
        attempts = 0
        result = compare_distributions(g, j, f0_median, f0_mean)
        while (result[3] > 0.05 and result[0] > 0.04) or attempts < 5:
            result = compare_distributions(g, j, f0_median, f0_mean)
            attempts += 1

        gender, mood = None, None
        if 97 < f0_median <= 114:
            gender, mood = "Male", "Showing no emotion, normal"
        elif f0_median <= 135:
            gender, mood = "Male", "Reading"
        elif f0_median <= 163:
            gender, mood = "Male", "Speaking passionately"
        elif f0_median <= 197:
            gender, mood = "Female", "Showing no emotion, normal"
        elif f0_median <= 226:
            gender, mood = "Female", "Reading"
        elif f0_median <= 245:
            gender, mood = "Male", "Speaking passionately"
        else:
            print("Voice not recognized")
            return None

        return {
            "gender": gender,
            "mood": mood
        }