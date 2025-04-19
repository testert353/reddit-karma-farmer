from keep_alive import keep_alive
import slack
from datetime import datetime
import random
import os
import praw
import time

sendSlackAlerts = False

mybot = praw.ini

# ✅ Ensure Reddit connection works before proceeding
try:
    subreddit = mybot.subreddit("pics")  # Use a real subreddit
    print("✅ Successfully connected to Reddit!")
except Exception as e:
    print(f"❌ Reddit connection failed: {e}")
    exit()

# ✅ Ensure tracking file exists
if not os.path.isfile("posts_replied_to.txt"):
    open("posts_replied_to.txt", 'w').write('')

def docomment():
    print("\n🚀 Bot started - Commenting & upvoting posts")

    # ✅ Load random comments safely
    try:
        randomposts = open("randomposts.txt", encoding="utf-8", errors="replace").read().split('|')
    except Exception as e:
        print(f"❌ Failed to load random posts: {e}")
        return

    # ✅ Start processing posts
    for submission in subreddit.stream.submissions():
        done = open("posts_replied_to.txt", 'r', encoding="utf-8").read().split(',')

        if submission.id not in done:
            rand = random.randint(0, len(randomposts) - 1)
            randompost = randomposts[rand]

            post_url = f"https://www.reddit.com/r/{submission.subreddit}/comments/{submission.id}"
            print(f"\n⚡️ New post detected: {submission.title}")
            print(f"🔗 Post URL: {post_url}")

            # ✅ UPVOTE the post
            submission.upvote()
            print("⬆️ Post upvoted!")

            # ✅ Prevent empty comments
            if not randompost.strip():
                print("⚠️ Skipped empty comment—no valid text found!")
                continue

            print(f"✍️ Commenting: {randompost}")

            try:
                submission.reply(randompost)
                print("✅ Comment successfully posted!")

                with open("posts_replied_to.txt", "a", encoding="utf-8") as posts_replied_to:
                    posts_replied_to.write(submission.id + ",")

                # ✅ Random delay between posts (avoids spam detection)
                delay = random.randint(5, 20)
                print(f"⏳ Waiting {delay} seconds before next post...")
                time.sleep(delay)

            except praw.exceptions.APIException as e:
                if "RATELIMIT" in str(e):
                    wait_time = int(str(e).split("Take a break for ")[1].split(" ")[0])
                    print(f"⏳ Rate limited! Waiting {wait_time} minutes...")
                    time.sleep(wait_time * 60)
                else:
                    print(f"❌ ERROR COMMENTING: {e}")

def go():
    while True:
        try:
            docomment()
        except KeyboardInterrupt:
            print("\n👋 Bot stopped manually")
            exit(0)
        except Exception as error:
            now = datetime.now()
            date = now.strftime("%m/%d/%Y %H:%M:%S")

            print(f"\n⚠️ ERROR OCCURRED AT {date}: {error}")

            with open("logs.txt", 'a', encoding="utf-8") as file:
                file.write(f"\n{date}\n{error}")

            if sendSlackAlerts:
                slacktoken = open("slacktoken.txt").read()
                client = slack.WebClient(token=slacktoken)
                client.chat_postMessage(channel='alerts', text=f"🚨 Error occurred:\n{error}")

            print("🔄 Restarting bot after error...")
            time.sleep(5)

keep_alive()
go()
