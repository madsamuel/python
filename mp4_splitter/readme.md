# 🎥 Video Splitter Script

This **Python script** splits an **MP4 video file** into two equal parts using **FFmpeg**. The script handles video files with spaces in their names, checks for **FFmpeg** availability, and suppresses terminal output from FFmpeg.

---

## 📋 **Features**
- Split any MP4 video file into two equal parts.
- Automatically handle spaces in file names and paths.
- Suppress verbose FFmpeg output during processing.
- Check if **FFmpeg** is installed on the system before running.
- Accept both **relative file names** and **absolute file paths**.

---

## 🛠️ **Requirements**
- **Python 3.x**
- **FFmpeg** (must be installed and available in the system PATH)

---

## 📥 **Installation**

### **1. Clone the Repository:**
```bash
git clone https://github.com/yourusername/video-splitter.git
cd video-splitter
```

### **2. Install Dependencies:**
The script uses only built-in Python libraries. No additional dependencies are required.

### **3. Install FFmpeg:**
If FFmpeg is not installed, download it from [FFmpeg.org](https://ffmpeg.org/download.html) and add it to your **system PATH**.

---

## 🚀 **Usage**

### **Run the Script:**
```bash
python split_video.py
```

### **Enter the MP4 File Path:**
The script will prompt you to enter the file path of the MP4 video to be split.

#### **Example 1:** File in the same folder as the script
```
Enter the name of your MP4 file (or full file path): my_video.mp4
```

#### **Example 2:** Full file path with spaces
```
Enter the name of your MP4 file (or full file path): "C:\Users\John Doe\Videos\my video.mp4"
```

---

## 🧪 **Example Output**
For an input file named `my_video.mp4`, the script will generate two output files:
- **`my_video_part1.mp4`**
- **`my_video_part2.mp4`**

---

## ⚠️ **Error Handling**
- The script checks if **FFmpeg** is available on the system.
- If the video file is not found, an error message is displayed.

---

## 🛠️ **Troubleshooting**
If you encounter issues with **FFmpeg**, ensure that it is properly installed and added to your **system PATH**.

### **Verify FFmpeg Installation:**
Run the following command in your terminal:
```bash
ffmpeg -version
```

---

## 📄 **License**
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 **Contributing**
Pull requests are welcome (if needed 😀)
