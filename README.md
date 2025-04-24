# Drawed

Drawed is a unique group chat web application where users portray their current state of mind through random fine art "stickers" rather than traditional text messages. Use this app to portrait how high you are, sending a random art piece that will show other users the state you are in. When a user presses the "I'm Drawed" button, the system selects a random artwork from a curated collection and displays it in the chat for everyone to see. The app creates a fun, visual communication experience that lets friends express their emotional or altered states through art history's diverse expressions.

## 🎨 Features

- **Simple, focused interface** with a prominent "I'm Drawed" button
- **Real-time chat** with instant art delivery to all participants
- **Curated art collection** from various periods and styles to match any vibe
- **Metadata display** for each artwork (title, artist, period)
- **Visual communication** through fine art that expresses your current state
- **No explanation needed** - let the art speak for your mood or state

## 🛠️ Technology Stack

- **Backend:** Flask (Python) with Flask-SocketIO for real-time communication
- **Database:** MongoDB for storing users, messages and artwork data
- **Frontend:** HTML/CSS/JavaScript with WebSocket integration
- **Deployment:** Initially on Raspberry Pi, potentially moving to cloud hosting later
- **Web Server:** Nginx as reverse proxy

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB
- Node.js and npm (for frontend development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/drawed.git
   cd drawed
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (create a .env file):
   ```
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   MONGO_URI=mongodb://localhost:27017/drawed_dev
   ```

5. Run the application:
   ```bash
   python run.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
drawed/
├── app/                    # Main application package
│   ├── __init__.py         # Package initializer
│   ├── config.py           # Configuration settings
│   ├── core.py             # Application factory
│   ├── models/             # Database models
│   ├── routes/             # Web routes and views
│   ├── sockets/            # WebSocket event handlers
│   ├── static/             # Static files (CSS, JS)
│   └── templates/          # HTML templates
├── artworks/               # Storage for artwork files
├── tests/                  # Test suite
├── .env                    # Environment variables (not in repo)
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
└── run.py                  # Application entry point
```

## 🌟 Roadmap

- [x] Initial project setup
- [x] Basic Flask application with "Hello World"
- [x] Chat interface design
- [ ] MongoDB integration and data models
- [ ] WebSocket implementation for real-time updates
- [ ] Random artwork selection and display
- [ ] User authentication and profiles
- [ ] Multiple chat rooms
- [ ] Art filtering and preferences
- [ ] Mobile responsiveness enhancements
- [ ] Deployment to cloud hosting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 👏 Acknowledgements

- All the amazing artists whose work will be shared through this application
- The Flask and MongoDB communities for excellent documentation
- Everyone who contributes to this project

---

Made with ❤️ and 🎨