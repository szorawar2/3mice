# 3mice - Remote Mouse Control 🞡

Control your computer's mouse remotely using your smartphone!

## Features ✨

- 📱 Web-based remote control interface
- 🖥️ Windows compatibility
- ↔️ Real-time mouse movement & clicks
- 🔊 Volume control integration

## Installation 💻

1. **Download the latest release**:
   - [v1.1](/v1.1) (Or Latest)
2. **Run the executable** (`3mice.exe`):
   - Allow private network access when prompted by Windows Firewall

## Usage 📲

1. **Find your computer's local IP**:

   ```cmd
   ipconfig
   ```

   Look for "IPv4 Address" under your active connection.

2. **Open your phone's browser**:

   ```
   http://[computer-ip]:5125
   ```

   Example: `http://192.168.1.101:5125`

3. **Start controlling!**
   - Touch area for mouse movement
   - On-screen buttons for left/right clicks
   - Volume controls available

## Development Setup 🫠

### Prerequisites

- Python 3.10+
- Node.js 18+
- Windows OS

### Backend (Python)

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend (React)

```bash
cd frontend
npm install
npm run start
```

## Building from Source 🌿

### Build React frontend:

```bash
cd frontend
npm i
npm run build
```

### Copy build files:

```bash
cp -r frontend/build server/react
```

### Package with PyInstaller:

```bash
pyinstaller 3mice.spec --noconfirm --clean --distpath ../dev
```

## Troubleshooting 💑

### Connection Issues

- Ensure both devices are on the same network
- Verify Windows Firewall allows private network access
- Check if port 5125 is open

## Important Note 🔐

Always use on trusted networks. For public networks, consider adding authentication.
