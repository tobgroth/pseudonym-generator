# 🔐 Pseudonym Generator



A secure, local-only tool to generate reproducible pseudonyms for research participants.



> ✅ No data is sent online. All processing happens on your machine.  

> ✅ GDPR/IRB-compliant for pseudonymizing sensitive data.



## 📌 Features



- Generate pseudonyms from name, DOB, and place of birth 

- Alternatively: Use existing pseudonym / base code

- Password-protected, reproducible pseudonyms

- Verification code to prevent typos in password

- Copy-paste ready output



## 🧩 How to Use



1. Install Python 3.7+ (or see below for Windows executable)

2. Run: `python pseudonym_generator.py`

3. Enter participant data to create a base code or enter existing 1st layer pseudonym / base code

4. Set a study password

5. Click "Generate Pseudonym(s)"

6. Copy output to clipboard



### 📦 Download (Windows)



You can run the tool without installing Python:



- ✅ **`pseudonymGenerator.exe`** – Windows executable (built from source).

- 📁 Location: `releases/PseudonymGenerator_v1.0`

- Unzip and use `.exe` within its folder



> ⚠️ **Important Security Note**:  

> This `.exe` was built from the open-source code in this repository.  

> You can verify its integrity by:

> 1. Downloading the source code.

> 2. Building it yourself using `pyinstaller` (see below).



> 🔐 **Always run executables from trusted sources.**  

> This tool does not connect to the internet — it runs entirely locally.



---



### 🛠️ Build from Source (Optional)



If you want to build the `.exe` yourself (recommended for security):



1. Install Python 3.7+.

2. Install `pyinstaller`:

&#x20;  ```bash

&#x20;  pip install pyinstaller

3. ```bash
   pyinstaller --onedir --windowed --name "PseudonymGenerator" --clean pseudonym_generator.py



## 🛡️ Security



- All hashing is done locally using PBKDF2 and SHA-256

- No PII is stored or transmitted

- Ambiguous characters (0/O) are replaced with # and +



### 🛡️ GDPR & IRB Compliance



This tool is designed to support GDPR and IRB-compliant research by:

- Performing all processing locally (no data sent online).

- Using pseudonymization to protect personal data.

- Requiring a password to regenerate pseudonyms.



⚠️ **Important**:  

This tool alone does not guarantee compliance.  

You must:

- Store the password securely (e.g., in a password manager).

- Delete raw data after pseudonymization.

- Document the process in your IRB application.

- Limit access to authorized personnel.



For full compliance, use this tool as part of a secure, documented research workflow.



## 📄 License



MIT License – see `LICENSE` file.



## 📚 Citing This Work



If you use this tool in your research, please cite it as:



> Tobias Grothe (2026). *PseudonymGenerator: A Secure Tool for Generating Reproducible Pseudonyms in Research*. GitHub. https://github.com/yourusername/pseudonym-generator



Or in BibTeX:

```bibtex

@misc{grothe2025pseudonymgenerator,
author = {Grothe, Tobias},
title = {PseudonymGenerator: A Secure Tool for Generating Reproducible Pseudonyms in Research},
year = {2026},
howpublished = {url{https://github.com/tobgroth/pseudonym-generator}}
}
```


## 📬 Support



For bugs or suggestions:  

👉 [GitHub Issues](https://github.com/tobgroth/pseudonym-generator/issues)



---



## 📝 Author



Tobias Grothe  

Researcher & Developer  

https://github.com/tobgroth

