from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import json

# Function to shorten URL using TinyURL
def shorten_url_tinyurl(long_url):
    try:
        # Construct the TinyURL shortening API URL
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        return response.text
    except Exception as e:
        return long_url  # If an error occurs, return the original URL

# Function to handle /find command
async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        query = " ".join(context.args)  # Combine the search query
        api_key = "qwertyuiop"  # Replace with your API key
        cse_id = "82uidw9iw9si92"  # Replace with your Custom Search Engine ID

        try:
            # Make the API request
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"
            response = requests.get(url)
            data = response.json()

            # Extract the top result if available
            if "items" in data:
                top_result = data["items"][0]
                title = top_result["title"]
                snippet = top_result["snippet"]
                link = top_result["link"]
                pagemap = top_result.get("pagemap", {})
                article_body = pagemap.get("metatags", [{}])[0].get("og:description", "No description available.")

                # Correctly format the Google search link
                google_search_link = f"https://www.google.com/search?q={query}"

                # Shorten the Google search link using the TinyURL API
                short_google_search_link = shorten_url_tinyurl(google_search_link)

                # Truncate snippet and article to 50 lines (if long)
                snippet_lines = snippet.split('. ')
                snippet_excerpt = '. '.join(snippet_lines[:50]) + ('.' if len(snippet_lines) > 50 else '')

                article_lines = article_body.split('. ')
                article_excerpt = '. '.join(article_lines[:50]) + ('.' if len(article_lines) > 50 else '')

                # Send detailed information to the user
                response_message = (
                    f"ᴛɪᴛᴛʟᴇ : {title}\n\n"
                    f"ꜱɴɪᴘᴘᴇᴛ : {snippet_excerpt}\n\n"
                    f"ɢᴏᴏɢʟᴇ ʟɪɴᴋ : {short_google_search_link}\n"
                )

                await update.message.reply_text(response_message)
            else:
                await update.message.reply_text(f"No results found for '{query}'.")
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")
    else:
        await update.message.reply_text("Usage: /find <search query>")

# Main function to start the bot
def main():
    bot_token = "7787965675643:nhfnorihroeuhhirioi"  # Replace with your bot's token

    # Create the Application
    application = Application.builder().token(bot_token).build()

    # Add handler for the /find command
    application.add_handler(CommandHandler("find", find_command))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
