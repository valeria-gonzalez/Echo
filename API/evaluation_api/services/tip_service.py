from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Dict, Any, List
from schemas.evaluation_schema import PraatAnalysisResponse, FeedbackResponse, TipsResponse

class FeedbackService:
    def __init__(self):
        self.model_name = "google/flan-t5-xxl"
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.generator = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=512,
                max_new_tokens=256,
                temperature=0.3,
                top_k=40,
                top_p=0.8,
                num_beams=3,
                do_sample=False,
                repetition_penalty=1.2,
                early_stopping=True
            )
            print(f"Model {self.model_name} loaded successfully.")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            self.generator = None
    
    def _analyze_audio_parameters(self, 
                                praat_data: Dict[str, Any]) -> Dict[str, str]:
        
        interpretations = {}
        
        if praat_data.get("pitch_mean_hz"):
            pitch = praat_data["pitch_mean_hz"]
            if pitch < 80:
                interpretations["pitch"] = (
                    "Very low pitch, may sound monotone or unclear"
                )
            elif pitch < 120:
                interpretations["pitch"] = (
                    "Low pitch, good for authority and clarity"
                )
            elif pitch < 180:
                interpretations["pitch"] = "Normal pitch range, very natural"
            elif pitch < 250:
                interpretations["pitch"] = "Higher pitch, expressive and clear"
            else:
                interpretations["pitch"] = (
                    "Very high pitch, may sound strained"
                )
                
        if praat_data.get("intensity_mean_db"):
            intensity = praat_data["intensity_mean_db"]
            if intensity < 55:
                interpretations["intensity"] = (
                    "Very quiet, difficult to hear clearly"
                )
            elif intensity < 63:
                interpretations["intensity"] = (
                    "Low volume, intimate speaking level"
                )
            elif intensity < 75:
                interpretations["intensity"] = (
                    "Good volume range, clear and natural"
                )
            elif intensity < 85:
                interpretations["intensity"] = (
                    "Loud volume, energetic and projected"
                )
            else:
                interpretations["intensity"] = (
                    "Very loud, may sound aggressive"
                )
        
        if praat_data.get("jitter_local_percent"):
            jitter = praat_data["jitter_local_percent"]
            if jitter < 0.5:
                interpretations["jitter"] = (
                    "Excellent pitch stability, very smooth"
                )
            elif jitter < 1.04:
                interpretations["jitter"] = (
                    "Good pitch stability, within normal range"
                )
            elif jitter < 2.0:
                interpretations["jitter"] = (
                    "Moderate pitch variation, slightly rough"
                )
            elif jitter < 4.0:
                interpretations["jitter"] = (
                    "Noticeable pitch instability, needs improvement"
                )
            else:
                interpretations["jitter"] = (
                    "Significant pitch problems, requires attention"
                )

        if praat_data.get("shimmer_local_db"):
            shimmer = praat_data["shimmer_local_db"]
            if shimmer < 0.5:
                interpretations["shimmer"] = (
                    "Excellent volume control, very steady"
                )
            elif shimmer < 1.0:
                interpretations["shimmer"] = (
                    "Good volume stability, smooth delivery"
                )
            elif shimmer < 2.0:
                interpretations["shimmer"] = (
                    "Moderate volume variation, acceptable"
                )
            elif shimmer < 3.81:
                interpretations["shimmer"] = "Noticeable volume instability"
            else:
                interpretations["shimmer"] = "Significant volume control issues"
        
        if praat_data.get("f1_mid_hz") and praat_data.get("f2_mid_hz"):
            f1, f2 = praat_data["f1_mid_hz"], praat_data["f2_mid_hz"]
            
            if f1 < 400 and f2 > 1500:
                interpretations["vowels"] = (
                    "Clear high vowels (like 'ee', 'oo')"
                )
            elif f1 > 600 and f2 < 1200:
                interpretations["vowels"] = (
                    "Clear low back vowels (like 'ah', 'aw')"
                )
            elif 400 <= f1 <= 600 and 1200 <= f2 <= 1500:
                interpretations["vowels"] = "Balanced vowel production"
            else:
                interpretations["vowels"] = "Mixed vowel characteristics"
        
        return interpretations
    
    def _calculate_overall_score(self, praat_data: Dict[str, Any]) -> float:
        
        score = 10
        
        if praat_data.get("jitter_local_percent"):
            jitter = praat_data["jitter_local_percent"]
            if jitter > 1.04:
                penalty = min(3.0, (jitter - 1.04) * 1.5)
                score -= penalty
                
        if praat_data.get("shimmer_local_db"):
            shimmer = praat_data["shimmer_local_db"]
            if shimmer > 1.0:
                penalty = min(2.5, (shimmer - 1.0) * 1.2)
                score -= penalty
                
        if praat_data.get("intensity_mean_db"):
            intensity = praat_data["intensity_mean_db"]
            if intensity < 55:
                score -= 2.0
            elif intensity < 63:
                score -= 1.0
            elif intensity > 85:
                score -= 1.5
            elif intensity > 75:
                score -= 0.5
                
        if praat_data.get("pitch_mean_hz"):
            pitch = praat_data["pitch_mean_hz"]
            if pitch < 70 or pitch > 300:
                score -= 1.5
            elif pitch < 85 or pitch > 250:
                score -= 0.5
                
        return max(0.0, min(10.0, score))
    
    def _generate_ai_feedback(self, interpretations: Dict[str, str],
                            score: float, praat_data: Dict[str, Any]) -> str:
        
        prompt = f"""Analyze this English speech voice and provide
        professional feedback:
        
        Voice Characteristics:
        - Pitch: {interpretations.get('pitch', 'N/A')}
        - Volume: {interpretations.get('intensity', 'N/A')}
        - Pitch Stability: {interpretations.get('jitter', 'N/A')}
        - Volume Control: {interpretations.get('shimmer', 'N/A')}
        - Vowel Quality: {interpretations.get('vowels', 'N/A')}
        
        Overall Score: {score}/10
        Speech Duration: {praat_data.get('duration_s', 0):.1f} seconds
        
        Provide constructive and professional feedback for English
        pronunciation based on these characteristics."""
        
        try:
            response = self.generator(prompt, max_length=200,
                                    num_return_sequences=1)
            return response[0]['generated_text'].strip()
        except Exception as e:
            print(f"Error generating AI feedback: {e}")
            return str(e)  # Fixed: return str(e) instead of just e
        
    def _generate_ai_recommendations(self, praat_data: Dict[str, Any],
                        interpretations: Dict[str, str]) -> List[str]:
        
        issues = []
        if praat_data.get("jitter_local_percent", 0) > 1.04:
            issues.append(
                f"pitch instability (jitter: "
                f"{praat_data['jitter_local_percent']:.2f}%)"
            )
            
        if praat_data.get("shimmer_local_db", 0) > 1.5:
            issues.append(
                f"volume instability (shimmer: "
                f"{praat_data['shimmer_local_db']:.2f} dB)"
            )  # Fixed: removed extra closing parenthesis
            
        if praat_data.get("intensity_mean_db", 0) < 63:
            issues.append(
                f"low volume (intensity: "
                f"{praat_data['intensity_mean_db']:.1f} dB)"
            )  # Fixed: removed extra closing parenthesis
            
        elif praat_data.get("intensity_mean_db", 0) > 75:
            issues.append(
                f"high volume (intensity: "
                f"{praat_data['intensity_mean_db']:.1f} dB)"
            )
            
        if praat_data.get("pitch_mean_hz", 0) < 85:
            issues.append(
                f"low pitch (pitch: "
                f"{praat_data['pitch_mean_hz']:.1f} Hz)"
            )
            
        elif praat_data.get("pitch_mean_hz", 0) > 250:
            issues.append(
                f"high pitch (pitch: "
                f"{praat_data['pitch_mean_hz']:.1f} Hz)"
            )
            
        prompt = f"""Generate 4-5 specific, actionable recommendations for
        improving English pronunciation based on these voice analysis
        results:
        
        Voice Issues Detected: {', '.join(issues) if issues else 
        'Minor improvements needed'}
        
        Voice Characteristics:
        {chr(10).join([f"- {k.title()}: {v}" 
        for k, v in interpretations.items()])}  # Fixed: added missing colon
        
        Duration: {praat_data.get('duration_s', 0):.1f} seconds
        
        Provide practical, specific recommendations for English language
        learners to improve their pronunciation.
        Focus on exercises and techniques they can practice daily:"""
        
        try: 
            response = self.generator(prompt, max_length=250,
                                    num_return_sequences=1)
            recommendations_text = response[0]['generated_text'].strip()
            
            recommendations = []
            for line in recommendations_text.split('\n'):
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•')
                            or line.startswith('1.') or line.startswith('2.')
                            or line.startswith('3.') or line.startswith('4.')
                            or line.startswith('5.')):
                    clean_line = line.lstrip('-•123456789. ').strip()
                    if clean_line:
                        recommendations.append(clean_line)
                elif line and not any(x in line.lower() 
                                    for x in ['recommendation', 'suggestion',
                                            'tip']):
                    recommendations.append(line)
            return recommendations[:5]  
        
        except Exception as e:
            print(f"Error generating AI tips: {e}")
            return []  # Fixed: return empty list instead of None
            
    def _generate_ai_tips(self, praat_data: Dict[str, Any]) -> Dict[str, Any]:
        
        score = self._calculate_overall_score(praat_data) 
        
        issues = []        
        strengths = []
        
        if praat_data.get("jitter_local_percent", 0) > 1.04:
            issues.append(
                f"pitch instability (jitter: "
                f"{praat_data['jitter_local_percent']:.2f}%)"
            )
        else:
            strengths.append("good pitch stability")
            
        if praat_data.get("shimmer_local_db", 0) > 1.5:
            issues.append(
                f"volume control (shimmer: "
                f"{praat_data['shimmer_local_db']:.2f} dB)"
            )
        else:
            strengths.append("good volume control")
            
        if praat_data.get("intensity_mean_db", 0) < 63:
            issues.append(
                f"voice projection (intensity: "
                f"{praat_data['intensity_mean_db']:.1f} dB too low)"
            )
        elif praat_data.get("intensity_mean_db", 0) > 75:
            issues.append(
                f"voice modulation (intensity: "
                f"{praat_data['intensity_mean_db']:.1f} dB too high)"
            )
        else:
            strengths.append("appropriate volume level")
            
        if praat_data.get("pitch_mean_hz", 0) < 85:
            issues.append(
                f"pitch variation (pitch: "
                f"{praat_data['pitch_mean_hz']:.1f} "
                f"Hz may be monotone)"
            )
        elif praat_data.get("pitch_mean_hz", 0) > 250:
            issues.append(
                f"pitch modulation (pitch: "
                f"{praat_data['pitch_mean_hz']:.1f} "
                f"Hz may be too high)"
            )
        else:
            strengths.append("natural pitch range")           
            
        tips_prompt = f"""Generate 5-6 personalized tips for improving English 
        pronunciation based on this voice analysis:

        Voice Strengths: {', '.join(strengths) if strengths 
        else 'Basic foundation present'}
        Areas for Improvement: {', '.join(issues) if issues 
        else 'Minor refinements needed'}
        Overall Score: {score:.1f}/10
        Speech Duration: {praat_data.get('duration_s', 0):.1f} seconds

        Provide specific, actionable daily practice tips for English language 
        learners:"""

        exercises_prompt = f"""Generate 4-5 specific practice exercises for 
        English pronunciation improvement based on these vocal characteristics:

        Issues to Address: {', '.join(issues) if issues 
        else 'General improvement'}
        Vocal Strengths: {', '.join(strengths) if strengths 
        else 'Building foundation'}

        Create practical exercises that can be done at home for 10-15 
        minutes daily:"""
        
        try:
            tips_response = self.generator(tips_prompt,  
                                                max_length=200, 
                                                num_return_sequences=1)
            tips_text = tips_response[0]['generated_text'].strip()
            
            exercises_response = self.generator(exercises_prompt,  
                                                    max_length=150, 
                                                    num_return_sequences=1)
            exercises_text = exercises_response[0]['generated_text'].strip()
            
            tips = self._parse_ai_response(tips_text)
            exercises = self._parse_ai_response(exercises_text)
            
            focus_areas = []
            if any("pitch" in issue for issue in issues):
                focus_areas.append("Pitch control")
            if any("volume" in issue for issue in issues):
                focus_areas.append("Volume stability")
            if any("projection" in issue for issue in issues):
                focus_areas.append("Voice projection")
            if any("modulation" in issue for issue in issues):
                focus_areas.append("Voice modulation")
            
            if not focus_areas:
                focus_areas = ["General refinement"]
            
            if score >= 8:
                difficulty = "Advanced - Fine-tuning"
            elif score >= 6:
                difficulty = "Intermediate - Skill building"
            elif score >= 4:
                difficulty = "Beginner - Foundation work"
            else:
                difficulty = "Basic - Essential development"
            
            return {
                "tips": tips[:6],
                "exercises": exercises[:5],
                "focus_areas": focus_areas,
                "difficulty": difficulty
            }
            
        except Exception as e:
            print(f"Error generating AI tips: {e}")
            return {  
                "tips": [],
                "exercises": [],
                "focus_areas": ["General improvement"],
                "difficulty": "Basic - Essential development"
            }
    
    def _parse_ai_response(self, text: str) -> List[str]:
        
        items = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or 
                        line.startswith(tuple('123456789')) or 
                        (len(line) > 20 and not line.startswith(('Generate', 
                                                                'Create', 
                                                                'Provide')))):
                clean_line = line.lstrip('-•123456789. ').strip()
                if clean_line and len(clean_line) > 10:
                    items.append(clean_line)
        if not items and text:
            sentences = [s.strip() 
                        for s in text.split('.') 
                        if s.strip() 
                        and len(s.strip()) > 15]
            items = sentences[:6]   
            
        return items
    
    async def generate_feedback(self, praat_data: 
        Dict[str, Any]) -> FeedbackResponse:
        
        interpretations = self._analyze_audio_parameters(praat_data)
        
        score = self._calculate_overall_score(praat_data)
        
        detailed_feedback = self._generate_ai_feedback(
            interpretations, score, praat_data)
        
        recommendations = self._generate_ai_recommendations(
            praat_data, interpretations)
        
        praat_response = PraatAnalysisResponse(**praat_data)
        
        return FeedbackResponse(
            overall_score=round(score, 1),
            detailed_feedback=detailed_feedback,
            vocal_characteristics=interpretations,
            recommendations=recommendations,
            praat_data=praat_response
        )
        
    async def generate_tips(self, praat_data: Dict[str, Any]) -> TipsResponse:
        """
        Generates personalized English pronunciation tips
        """
        tips_data = self._generate_ai_tips(praat_data)
        praat_response = PraatAnalysisResponse(**praat_data)
        
        return TipsResponse(
            personalized_tips=tips_data["tips"],
            exercises=tips_data["exercises"],
            focus_areas=tips_data["focus_areas"],
            difficulty_level=tips_data["difficulty"],
            praat_data=praat_response
        )

def get_feedback_service():
    return FeedbackService()