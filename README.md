# SpotMuzik

A desktop music player application built with Python and Tkinter that fetches trending tracks via the Spotify API, streams 30-second audio previews through the Deezer API, and lets users manage personal playlists within a dark-themed GUI.

---

## Key Features

- **User Authentication** — Register and log in with credentials stored securely in a local SQLite database; active sessions are tracked in memory using a singly linked list.
- **Trending Track Discovery** — Fetches the top 20 current tracks from the Spotify API and displays them in an interactive list ready for playback.
- **Audio Streaming** — Resolves each track through the Deezer public API and streams its 30-second preview directly via `pygame`, with full Play / Pause / Resume / Next / Previous controls.
- **Playlist Management** — Create, rename, and edit named playlists; add or remove individual tracks; browse your full library from a dedicated screen.
- **Playlist Customization** — Personalize playlists with custom names and manage track ordering from within the app.

---

## Prerequisites

- **Python** 3.10 or later
- **pip** (bundled with Python)
- **Spotify Developer credentials** — a `client_id` and `client_secret` from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

> The Deezer API is public and requires no credentials.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Duartedlourenco/spotmuzik.git
cd spotmuzik/Projeto

# 2. Install dependencies
pip install -r requirements.txt
```

### Configure Spotify credentials

Open `View.py` and replace the placeholder values in the `load_top_tracks` method:

```python
client_id     = 'YOUR_SPOTIFY_CLIENT_ID'
client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'
```

> **Security note:** For production use, load these values from environment variables or a `.env` file rather than hard-coding them.

---

## Usage

```bash
# From inside the Projeto/ directory
python Program.py
```

**Typical workflow:**

1. Register a new account or log in with existing credentials.
2. Click **Carregar Músicas** to fetch the current top 20 tracks from Spotify.
3. Select a track from the list and click **Play** to stream its Deezer preview.
4. Use the **Biblioteca** screen to create playlists, add tracks to them, and browse your saved collections.

---

## Project Structure

```
Projeto/
├── Program.py                  # Entry point — initialises Tk root and Controller
├── Controller.py               # MVC controller; wires root window to View
├── View.py                     # All UI frames, event handlers, and API calls
├── requirements.txt
└── Model/
    ├── DataBase.py             # SQLite wrapper (user persistence)
    ├── Utilizador.py           # User domain model
    ├── UtilizadorLinkedList.py # Singly linked list for in-memory user sessions
    └── List/
        ├── List.py             # Abstract base class for list ADT
        └── Nodes.py            # SingleListNode and DoubleListNode implementations
```

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `customtkinter` | ≥ 5.2.0 | Modern-styled Tkinter widgets |
| `pygame` | ≥ 2.5.0 | Audio playback engine |
| `requests` | ≥ 2.31.0 | HTTP calls to Deezer API |
| `spotipy` | ≥ 2.23.0 | Spotify Web API client |

---

## Contributing

1. Fork the repository and create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes. Keep commits focused and messages descriptive.
3. Ensure the application runs without errors before opening a pull request.
4. Open a pull request against `main` with a clear description of what was changed and why.

For significant changes, open an issue first to discuss the proposed approach.

---

## License

This project was developed for educational purposes.
