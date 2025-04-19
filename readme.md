# 🚀 Reddit Upvote & Comment Bot
An automated Reddit bot that **upvotes** and **comments** on new posts in a chosen subreddit. This bot uses [PRAW](https://praw.readthedocs.io/en/latest/) (Python Reddit API Wrapper) to interact with Reddit's API while handling **rate limits** and **spam detection** intelligently.

## 🔥 Features
✅ **Upvotes posts automatically**  
✅ **Posts randomized comments** from a predefined list  
✅ **Handles Reddit’s rate limits** (avoids excessive commenting)  
✅ **Uses randomized delays** to prevent spam detection  
✅ **Tracks replied posts** to prevent duplicates  
✅ **Auto-restarts on errors** for stability  

## ⚡ Installation
### 1️⃣ **Clone this Repository**
```sh
git clone https://github.com/testert353/reddit-karma-farmer.git
cd reddit-karma-bot
```

### 2️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 3️⃣ **Set Up Reddit API Credentials**
1. Visit [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click **Create App** → Choose **Script**
3. Note down **client ID**, **client secret**, **username**, **password**
4. Edit `praw.ini`:
```py
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
USERNAME = "your_reddit_username"
PASSWORD = "your_reddit_password"
USER_AGENT = "Epic Bot"
SUBREDDIT = "pics"  # Change to target subreddit
```

### 4️⃣ **Run the Bot**
```sh
python main.py
```

## 📜 Configuration
Modify `randomposts.txt` to change the comment pool:
```txt
Upvoted! Keep posting awesome content | Your post stood out—had to upvote | Take my upvote—go forth and post more greatness | Boosted your post—hope it gets more love | Dropped an upvote, hope this gets more visibility | Had to upvote—this was worth it
```

## 🛠 How It Works
1. The bot connects to Reddit using PRAW.
2. It streams new posts from a **target subreddit**.
3. For each post:
   - ✅ **Upvotes the post** so the comment will be more believable.
   - ✅ **Posts a random comment** from `randomposts.txt`
   - ✅ **Logs the post ID** to prevent duplicate interactions
4. If **rate-limited**, it waits until Reddit allows more actions.

## 🚨 Handling Rate Limits
Reddit enforces **rate limits** when posting too fast. The bot automatically **detects rate limits** and waits before continuing.

```py
except praw.exceptions.APIException as e:
    if "RATELIMIT" in str(e):
        wait_time = int(str(e).split("Take a break for ")[1].split(" ")[0])
        print(f"⏳ Rate limited! Waiting {wait_time} minutes...")
        time.sleep(wait_time * 60)
```

## ❌ Troubleshooting
| Problem | Solution |
|---------|----------|
| Bot does nothing after launch | Ensure correct API credentials in `config.py` |
| Rate limit errors | Reduce the bot’s activity or increase delay time |
| Empty comments | Ensure `randomposts.txt` contains valid text |
| 404 error on subreddit | The subreddit may be **banned** or **private** |

## 🎯 Future Enhancements
- [ ] Add **AI-generated replies** using GPT API  
- [ ] Implement **post filtering** (e.g., avoid NSFW content)  
- [ ] Create a **web-based dashboard** for bot stats  

## 💡 Credits & License
- Created by **Testert353**
- Powered by **Python & PRAW**
- Open-source under **MIT License**

🔥 **Ready to boost your Reddit karma? Run the bot and let it roll!** 🚀
