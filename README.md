# AutoDash 📊

AutoDash is an innovative tool that automatically generates interactive Streamlit dashboards from tabular data using AI-powered code generation. With AutoDash, you can transform your CSV files into beautiful, functional dashboards with just a few clicks.

![AutoDash Demo](https://i.imgur.com/b79yiqV.png)

## 🚀 Features

- **AI-Powered Dashboard Generation**: Utilizes advanced AI models (Claude and OpenAI) to create custom Streamlit dashboard code.
- **One-Click GitHub Integration**: Easily create a new GitHub repository with your dashboard code.
- **Download Option**: Download your dashboard as a structured project, ready to run.

## 🏗️ Project Structure

AutoDash is split into two repositories:

1. Backend (this repository): Contains the API and core logic for dashboard generation.
2. Frontend: Contains the user interface. [Link to Frontend Repository](https://github.com/luucaslfs/AutoDash-Front)

## 🛠️ Installation

### Backend Setup

1. Clone the backend repository:
   ```
   git clone https://github.com/luucaslfs/AutoDash.git
   cd AutoDash
   ```

2. Install dependencies:
   ```
   cd API
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_URL=your_database_url
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   CLAUDE_API_KEY=your_claude_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Frontend Setup

1. Clone the frontend repository:
   ```
   git clone https://github.com/your-username/AutoDash-Front.git
   cd AutoDash-Front
   ```

2. Install dependencies:
   ```
   cd autodash
   npm install
   ```

## 🖥️ Usage

1. Start the backend server:
   ```
   cd API
   uvicorn app.main:app --reload
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd AutoDash-Front/autodash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`.

4. Upload your CSV or Excel file, choose an AI model, and click "Generate Dashboard".

5. Review the generated code, make any necessary edits, and either download the project or create a GitHub repository.

## 🤝 Contributing

We welcome contributions to both the backend and frontend of AutoDash! 

## 📄 License

AutoDash is released under the MIT License. See the [LICENSE](link-to-license-file) file for more details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for making it easy to create beautiful data apps.
- [OpenAI](https://openai.com/) and [Anthropic](https://www.anthropic.com/) for their powerful AI models.

## 📞 Support

If you encounter any issues or have questions:
- For backend issues, please [open an issue](https://github.com/your-username/AutoDash/issues/new) on our backend GitHub repository.
- For frontend issues, please [open an issue](https://github.com/your-username/AutoDash-Front/issues/new) on our frontend GitHub repository.

## 🎥 Demo

Check out our video tutorial on how to use AutoDash:

[![AutoDash Tutorial](link-to-youtube-thumbnail)](link-to-youtube-video)

---

Made with ❤️ by [Lucas Florencio]