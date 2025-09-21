# Arm Twin — Python ↔ Unity3D (Live JSON Control)

A **digital twin** demo for robotic arms using **Python** and **Unity3D**.

- **Python side**: Writes live-changing JSON files with joint/link angles.
- **Unity side**: Reads these JSON files and rotates link GameObjects in real-time.
- Works with **sensors, OpenCV tracking, or simulated input**.

---

## 🚀 Features
- Modular JSON per-link (`link1.json` … `link6.json`) or single JSON.
- Smooth interpolation of angles in Unity.
- Atomic JSON writing (no half-written files).
- Easy to extend with OpenCV, IMU sensors, or Bluetooth.

---

## 📂 Structure
