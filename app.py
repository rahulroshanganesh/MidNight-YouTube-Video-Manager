from flask import *
from datetime import datetime
import validators

app = Flask(__name__)



@app.route("/", methods=["GET"])
def home():
    return """
        <h1 style="text-align:center;">MidNight YouTube Video Manager</h1>
        <h2>Enter the contents below</h2>
        <form method="POST" action="/go">
            <h2>Title:- <input type="text" name="title"></h2>
            <h2>URL:- <input type="text" name="url"></h2>
            <input type="submit">
            </form>
        <form methd="GET" action="/list">
            <input type="submit" value="See List" >
        </form>

        <div style="text-align:center;">
            <h1> ABOUT </h1>
            <h3>If Youtube Watch Later and Liked videos Playlist is filled and messed up use my app. I built this literally on midnight.</h3>
        </div>
    """

@app.route("/go", methods=["POST"])
def go():
    # if request.method == "POST":
    url = request.form.get("url")
    title = request.form.get("title")

    with open("db.txt", 'a') as file:
        file.write(title + "-------" + url + "-------" + str(datetime.now()) +"\n")
    return f"""
            <h1>Added {title}</h1>
            <button><h3><a href="/list"> See lists </a></h3></button>
    """ 

@app.route("/list", methods=["GET"])
def list():
    ListOfUrls = []
    template = ""
    # component = ""
    with open("db.txt", "r") as file:
        ListOfUrls = file.readlines()

    for item in ListOfUrls:
        title, url, time= item.split("-------")
        if "youtube" in url: 
            domain, id = url.split("=")
            videoId = f"https://img.youtube.com/vi/{id}/0.jpg"
        else:
            videoId = "https://support.vevo.com/hc/article_attachments/16164505898395"
        if not validators.url(url):
            component = f"""
                <h3 style="font-size:24px;">{url}</h3>
            """
        else:
            component = f"""
            <img src={videoId} width="120" style="margin-left:10px;"/>
                <button>
                    <a href={url} target="_blank">
                        {title}
                    </a>
                </button> 
            """
        template += f"""
                <li style="list-style:none; margin:5px 0;">
                    {component}
                    <span style="margin-left:10px; font-size:14px; color:gray;">
                        at {time}
                    </span>
                    <form method="post" action="/remove"> 
                        <input type="hidden" name="id" value="{id}">
                        <input type="submit" value="DELETE" style="color:red; font-size:20px;">
                    </form>
                </li>
            """

    return f"""
        <h1 style="text-align:center;">List of Useful Links</h1>
        <ul style="padding:0;">
            {template}
        </ul>
        <form method="GET" action="/">
            <input type="submit" value="Add more">
        </form>
    """

@app.route("/remove", methods=["POSt"])
def remove():
    id = request.form.get("id")
    with open("db.txt", "r") as file:
        lt = file.readlines()

    for item in lt:
        if id in item:
            dele = item
            lt.remove(item)

    with open("db.txt", "w") as file:
        file.write("\n".join(lt))

    return f"""
    <h1>Deleted {dele.split("-------")[0]}</h1>
    <p>You will be redirected to Home in 3 seconds...</p>
    <script>
        setTimeout(function(){{
            window.location.href = "/";
        }}, 3000);
    </script>
    """

if __name__ == "__main__":
    app.run(debug=True)
