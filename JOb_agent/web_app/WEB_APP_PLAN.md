# 🌌 JobTracker Premium Web App - Implementation Plan

## 🎯 Objective
Build a **high-end, production-ready web application** for JobTracker that feels premium, fluid, and "not AI generated".

## 🛠 Tech Stack
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Vanilla CSS Modules (for maximum control & performance)
- **Animations:** Framer Motion (critical for the "premium" feel)
- **Icons:** Lucide React
- **Backend:** Existing FastAPI (Python)

## 🎨 Design System: "Nebula"

### 1. Color Palette
- **Background:** `#0A0A0F` (Deep Void)
- **Surface:** `rgba(255, 255, 255, 0.03)` (Glass)
- **Border:** `rgba(255, 255, 255, 0.08)`
- **Primary:** `#00E5FF` (Cyan Neon) - for actions
- **Secondary:** `#7C4DFF` (Deep Purple) - for gradients
- **Text:** `#FFFFFF` (Primary), `#A1A1AA` (Secondary)

### 2. UI Components
- **Glass Cards:** Backdrop blur `12px`, thin borders, subtle inner shadow.
- **Glowing Gradients:** Radial gradients behind important elements.
- **Typography:** `Inter` (Google Fonts) - clean, readable, modern.

## 🚀 Features & Pages

### 1. Landing / Dashboard (`/`)
- **Hero Section:** "Find Your Next Mission" with animated gradient text.
- **Stats Row:** 3D-style cards showing "Jobs Applied", "Interviews", "Offers".
- **Recent Activity:** Timeline view of applications.

### 2. Job Search (`/jobs`)
- **Search Bar:** Floating, glowing search bar.
- **Job Cards:**
    - Logo (left)
    - Title & Company (bold)
    - Match Score (animated ring)
    - "Apply" button (hover effect: glow)
- **Filters:** Sidebar with glass effect.

### 3. Job Details (`/jobs/[id]`)
- **Split View:** Job details on left, AI analysis on right.
- **AI Match Analysis:** "Why you match" with animated checkmarks.

### 4. Applications Board (`/applications`)
- **Kanban Board:** Drag and drop columns (Applied, Interview, Offer).
- **Smooth transitions** when moving cards.

## 🔄 Backend Integration
We will use the existing FastAPI endpoints:
- `GET /api/v1/jobs/search`
- `GET /api/v1/jobs/recommendations`

## 📅 Step-by-Step Execution

1.  **Setup:** Install dependencies (`framer-motion`, `lucide-react`, `clsx`).
2.  **Styles:** Configure `globals.css` with CSS variables.
3.  **Components:** Build reusable `GlassCard`, `NeonButton`, `PageLayout`.
4.  **Pages:** Implement Dashboard and Job Search first.
5.  **Integration:** Connect to localhost:8000.
