import os
import gradio as gr
import google.generativeai as genai
from prompts import TEACHER_PROMPT

# ==========================================
# 1. GEMINI AI CONFIGURATION
# ==========================================
# Aapki generate ki hui API Key yahan set ho gayi hai
GEMINI_API_KEY = "AQ.Ab8RN6JS4yBatnoFHNV3CtNQbGtn-JC-hydhMeBtayzpzQ0zCQ"
genai.configure(api_key=GEMINI_API_KEY)

# Aapki screen ke hisab se exact model name set kiya hai
model = genai.GenerativeModel('gemini-3-flash-preview')

# ==========================================
# 2. CORE LOGIC (Voice Command Processing)
# ==========================================
def process_classroom_command(audio_path):
    if not audio_path:
        return "🎙️ Teacher Sahab, pehle Mic par click karke kuch boliye, fir send kijiye!"

    try:
        # Step A: Microphone se record ki hui audio file ko read karna
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        # Step B: Gemini 3 Flash Preview ko data bhejna
        response = model.generate_content([
            TEACHER_PROMPT,
            {
                "mime_type": "audio/mp3", 
                "data": audio_bytes
            },
            "Is audio command ko dhyan se suniye aur upar diye gaye TEACHER_PROMPT ke rules ke hisab se smart board ke liye Hinglish me output generate kijiye."
        ])
        
        # Step C: AI ka response text wapas screen par dikhana
        return response.text

    except Exception as e:
        return f"⚠️ Ek error aaya hai: {str(e)}\n\nKripya check karein ki aapka internet chal raha hai ya nahi."

# ==========================================
# 3. SMART BOARD UI DESIGN (GRADIO)
# ==========================================
# Custom CSS taaki Smart Board par text bada aur clear dikhe (UX Empathy)
custom_css = """
.smart-board-text textarea {
    font-size: 28px !important; 
    line-height: 1.6 !important;
    font-family: 'Arial', sans-serif !important;
    font-weight: bold !important;
    color: #0f172a !important;
    background-color: #f8fafc !important;
}
"""

with gr.Blocks(css=custom_css, title="CDF AI Classroom Assistant") as demo:
    gr.Markdown("# 🏫 Connecting Dreams Foundation - AI Classroom Co-Pilot")
    gr.Markdown("### Option A: Voice-Enabled AI Teaching Assistant for Government Schools")
    gr.HTML("<hr>")
    
    with gr.Row():
        # LEFT SIDE: Teacher Controls
        with gr.Column(scale=1):
            gr.Markdown("### 🎙️ Teacher Controls")
            audio_input = gr.Audio(
                sources=["microphone"], 
                type="filepath", 
                label="Mic On karke boliye (e.g., 'Explain Photosynthesis' ya 'Take a Quiz')"
            )
            submit_btn = gr.Button("🚀 Project to Smart Board", variant="primary")
            
        # RIGHT SIDE: Big Smart Board Display for Classroom
        with gr.Column(scale=2):
            gr.Markdown("### 📺 Smart Board Screen (For Students)")
            board_display = gr.Textbox(
                label="Live Content Display", 
                lines=12, 
                elem_classes=["smart-board-text"],
                interactive=False
            )

    # Connections
    submit_btn.click(
        fn=process_classroom_command, 
        inputs=audio_input, 
        outputs=board_display
    )

# Local Server par launch karne ke liye
if __name__ == "__main__":
    demo.launch()