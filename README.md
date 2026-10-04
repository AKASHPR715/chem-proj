# ⚗️ Periodic Table Quiz



![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧪 **30 curated questions** | Element symbols, names, atomic numbers, groups & classifications |
| 🎨 **Rich UI** | Gradient hero banner, glassmorphism cards, micro-animations |
| 💡 **Hints & explanations** | Collapsible hint before answering; detailed explanation after |
| 📊 **Live score dashboard** | Score, attempts, accuracy % with animated progress bar |
| 🔄 **Session state** | Score persists across questions; restart anytime |
| 🎉 **Completion screen** | Balloons + final stats when all questions are finished |

---

## 📁 Project Structure

```
project/
├── app.py              # Main Streamlit application
├── questions.csv       # Question bank (30 questions)
├── requirements.txt    # Python dependencies
└── README.md           # You are here
```

---

## 🚀 Absolute Beginner's Guide: How to Run This Quiz

If you have never touched a computer program before, don't worry! Follow these exact steps to get this quiz running on your machine:

**Step 1: Install a Code Editor (IDE)**
First, you need a program to open and view the code. We recommend Visual Studio Code (VS Code). Go to [code.visualstudio.com](https://code.visualstudio.com/), download the installer for your operating system (Windows or Mac), and run it. Just keep clicking "Next" until it is installed.

**Step 2: Install Python**
Python is the language this quiz is written in. Go to [python.org/downloads](https://www.python.org/downloads/) and click the big yellow button to download the latest version. **CRITICAL STEP:** When you open the Python installer, look at the very bottom of the first screen and **check the box that says "Add python.exe to PATH"**. If you miss this, nothing else will work! After checking the box, click "Install Now".

**Step 3: Open the Project in VS Code**
Download this quiz project folder to your computer and remember where you saved it. Open VS Code, click on **File > Open Folder...**, and select the project folder you just downloaded. You should now see files like `app.py` and `README.md` on the left side of your screen.

**Step 4: Open a Terminal**
Inside VS Code, look at the top menu bar. Click on **Terminal > New Terminal**. A small text window will open at the bottom of your screen. This is where you will type commands to make the app work.

**Step 5: Create and Activate a Virtual Environment**
A virtual environment is like a secure bubble for this specific project. In the terminal you just opened, type the following command and press Enter:
`python -m venv venv`

Wait a few seconds. A new folder named "venv" will appear on the left. Now, you need to activate this bubble. 
- If you are on **Windows**, type: `venv\Scripts\activate` and press Enter.
- If you are on **Mac/Linux**, type: `source venv/bin/activate` and press Enter.

You will know it worked if you see `(venv)` appear at the start of the line in your terminal.

**Step 6: Install the Required Tools**
Our quiz uses special tools called Streamlit and Pandas. To download them into your bubble, type this command and press Enter:
`pip install -r requirements.txt`

You will see a bunch of text scrolling by as it downloads. Wait until it finishes and stops moving.

**Step 7: Run the Quiz!**
You are finally ready! In the terminal, type this final command and press Enter:
`streamlit run app.py`

A browser window should automatically pop open showing the Periodic Table Quiz! If it doesn't pop open, look in the terminal for a link that looks like `http://localhost:8501` and `Ctrl-Click` it. To stop the quiz later, click on the terminal and press `Ctrl + C`.

---

## 📝 Adding / Editing Questions

Open `questions.csv` in any spreadsheet editor or text editor. Each row needs:

| Column | Description |
|---|---|
| `id` | Unique integer ID |
| `question` | The question text |
| `option_a` – `option_d` | Four answer choices |
| `correct_option` | Letter of the correct option (`A`, `B`, `C`, or `D`) |
| `hint` | A short hint shown before answering |
| `explanation` | Detailed explanation shown after answering |

Save the file and refresh the Streamlit app — new questions appear instantly.

---

## 🛠️ Tech Stack

- **Streamlit** — interactive web UI
- **Pandas** — CSV data loading & manipulation
- **Python** — core logic & session-state management

---

## 📄 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
