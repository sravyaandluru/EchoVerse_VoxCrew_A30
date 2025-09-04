EchoVerse – PDF & Text to Audiobook

EchoVerse is a sleek Streamlit app that converts PDFs and text into audiobooks.
With customizable voice, narration speed, and light/dark themes, it’s the perfect tool for students, readers, and multitaskers.

Features

PDF to Audio – Upload any text-based PDF and instantly convert it
Preview & Edit – Extract text, select page ranges, and edit before converting
Custom Voices – Choose between male or female voice options
Adjustable Speed – Narration from 0.5x very slow to 2x turbo fast
Beautiful UI – Light & dark themes with gradient cards
Responsive Layout – Works seamlessly on desktop & mobile

Quick Setup

# 1. Clone & Navigate
git clone <your-repo-url>
cd EchoVerse

# 2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run the App
streamlit run app.py --server.port 8501


Then open http://localhost:8501
 in your browser.

What You’ll See
Upload Tab – Upload your PDF & pick page ranges
Preview Section – Edit extracted text before conversion
Voice & Speed Options – Customize narration style
Convert Buttons – Generate preview or full audiobook
Download Option – Save the result as an MP3 file


Troubleshooting
Text not extracted? The PDF might be scanned (image-only)
Voice missing? Depends on available system voices
Slow conversion? Large documents take more time
Port busy? Run on another port:
streamlit run app.py --server.port 8502


Tech Stack
Frontend: Streamlit + Custom CSS
Backend: Python + PyPDF2
TTS Engine: pyttsx3 (offline text-to-speech)
Design: Gradient themes + Light/Dark mode

Team Notes
Works completely offline – no internet or cloud costs
Outputs in MP3 format (playable anywhere)
Ideal for students, professionals, and audiobook lovers
