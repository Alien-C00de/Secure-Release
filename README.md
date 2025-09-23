# 🔐 Secure Release – Empowering Safe and Reliable Applications

Secure Release is a unified security scanning solution that empowers developers and security teams to identify and mitigate vulnerabilities early in the development lifecycle.  
It integrates multiple scanning techniques under one umbrella to ensure code, dependencies, secrets, and APIs are thoroughly analyzed for hidden threats and misconfigurations.  

---

## 🌟 Key Highlights
- Empowers developers & security teams with **unified scanning capabilities**.  
- Provides **comprehensive analysis** across code, dependencies, secrets, and APIs.  
- Identifies **vulnerabilities, misconfigurations, and hidden threats** early.  
- Enhances security posture by offering **actionable insights and recommendations**.  
- Streamlines scanning processes under **one powerful, integrated solution**.  

---

## 🛠️ Features
- Developed in **Python**  
- **SAST & API Scan** under one umbrella  
- **Asynchronous execution** for faster scanning  
- Accurate **vulnerability detection** across layers  
- **User-friendly interface** with Streamlit  
- Generates **detailed HTML reports**  
- **Dependency Scanning** using OWASP Dependency-Check & Safety  
- **Code Scanning** with Semgrep (Java, .NET) & Bandit (Python)  
- **Secret Scanning** using detect-secrets (hardcoded secrets detection)  
- **API Security Testing** with OWASP ZAP v2 & custom fuzzing  

---

## ⚙️ Prerequisites

#### Before running the tool, ensure the following are installed on your machine:

- **OWASP Dependency-Check** (Add the Dependency-Check `bin` folder location in the `config.yaml` file.)

  Download: [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check)  

- **OWASP ZAP**

  Download: [OWASP ZAP](https://www.zaproxy.org/download/)  

🔹 The setup instructions below are for **Windows users**, but installation is almost the same for **Linux**.

---

## 📦 Installation

- #### Clone this repository and install all required dependencies:

```bash
git clone https://github.com/Alien-C00de/Secure-Release.git
pip install -r requirements.txt
```
- #### To enable API scanning, run the ZAP daemon from the `Secure Release` root directory:
```bash
start_zap.bat
```
- #### Run the tool with the following command:
```bash
streamlit run gui_app.py
```
##### This will launch the Secure Release GUI in your browser.

## 📂 File Structure

- `config.yaml` → Contains all configuration settings.
- `./Sample_code/`→ Includes intentionally vulnerable projects for testing.

## 📊 Reports

- HTML report files are located under the `./Reports/output` directory:

- Reports include detailed findings for code scans, dependency checks, secret scans, and API vulnerabilities.

## 🖼️ Screenshots
- **SAST Dashboard Preview**

<img width="1029" height="729" alt="localhost_8501_ (4)" src="https://github.com/user-attachments/assets/bdaf9b18-6c86-438b-b8d0-9bcdf788cdd7" />

- **SAST Report Preview**
<img width="1018" height="763" alt="SAST" src="https://github.com/user-attachments/assets/900ff52d-f94a-43dd-8749-5b8de293e76c" />

- **API Scanner Preview**
<img width="1045" height="765" alt="localhost_8501_ (7)" src="https://github.com/user-attachments/assets/fa1c6940-39b1-42b8-a884-628e8b9a6098" />

- **SAST Report Preview**
<img width="1001" height="771" alt="API" src="https://github.com/user-attachments/assets/d347ff38-eabd-4f16-847c-6e6c0cf087c6" />


## 🚀 Future Enhancements
- Enhancing Module Capabilities.
- AI-Powered Security Analysis.
- User Experience & Performance Optimization.
