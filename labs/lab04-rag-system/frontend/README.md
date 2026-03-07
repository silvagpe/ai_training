# RAG System Frontend

A Next.js-based frontend for indexing and querying source code files using RAG (Retrieval Augmented Generation).

## Features

- **Index Files**: Upload or manually add up to 2 source code files for indexing
- **Query Interface**: Chat-based interface to ask questions about indexed files
- **Sources & Context**: View detailed sources and context used to generate answers
- **Responsive Design**: Mobile-friendly interface
- **Modern UI**: Built with shadcn/ui components and Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

### Indexing Files

1. Navigate to the home page (Index Files)
2. Add up to 2 source code files using either:
   - **Manual entry**: Enter filename and paste code content
   - **File upload**: Click "Upload File" button and select a file (max 100KB)
3. Click "Index Files" to submit
4. View the indexing results showing chunks indexed and file names

### Querying Files

1. Navigate to the Query page
2. Type your question about the indexed files in the text area
3. Press Enter or click "Send" to submit
4. View the answer in the chat interface
5. Click "View Sources" to see which code sections were used
6. Click "View Context" to see the full code context

## Tech Stack

- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **Icons**: lucide-react

## API Endpoints

The application connects to:
- **Index**: `POST https://lab4rag-production.up.railway.app/index/files`
- **Query**: `POST https://lab4rag-production.up.railway.app/query`

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with navbar
│   ├── page.tsx            # Index/upload page
│   ├── query/
│   │   └── page.tsx        # Query page with chat interface
│   └── globals.css         # Global styles and theme
├── components/
│   ├── navbar.tsx          # Navigation component
│   └── ui/                 # shadcn/ui components
├── lib/
│   ├── api.ts              # API client functions
│   ├── types.ts            # TypeScript type definitions
│   └── utils.ts            # Utility functions
└── public/                 # Static assets
```

## Color Scheme

The application uses a custom color palette:
- Primary (Cyan): `#049DBF`
- Secondary (Brown): `#8C4F04`
- Accent (Tan): `#D99036`
- Brown Light: `#8C6542`
- Dark: `#0D0D0D`

## Development

### Build for Production

```bash
npm run build
```

### Start Production Server

```bash
npm start
```

### Lint Code

```bash
npm run lint
```

## Features Details

### File Size Limits
- Maximum file size: 100KB per file
- Maximum files: 2 files can be indexed at once

### Supported File Types
`.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.java`, `.cpp`, `.c`, `.go`, `.rs`, `.rb`, `.php`, `.html`, `.css`, `.json`, `.yaml`, `.yml`, `.txt`

### Chat Features
- Message history maintained during session
- Keyboard shortcuts: Enter to send, Shift+Enter for new line
- Loading states while processing queries
- Error handling for API failures

## License

MIT

