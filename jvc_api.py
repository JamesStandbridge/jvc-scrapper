from requests_html import HTMLSession, HTML

class Topic:

    def __init__(self, title: str, author: str, url: str, base_url: str, session: HTMLSession):
        self.title = title
        self.author = author
        self.url = url
        self.base_url = base_url
        self.session = session

    def setPage(self, page: int) -> None:
        url_list = self.url.split("-")
        url_list[3] = str(page)
        self.url = "-".join(url_list)

    def getMessages(self, page: int) -> list:
        self.setPage(page)
        content = self.session.get(self.base_url + self.url).html

        messages = []
        for bloc_message in content.find(".bloc-message-forum"):
            bloc_message_html = HTML(html=bloc_message.html)

            for bloc_pseudo in bloc_message_html.find(".bloc-pseudo-msg"):
                author = bloc_pseudo.text

            for bloc_contenu in bloc_message_html.find(".bloc-contenu"):
                content = bloc_contenu.text

            for bloc_date in bloc_message_html.find(".bloc-date-msg"):
                date = bloc_date.text

            messages.append(Message(author, content, date))

        return messages

    def sendMessage(self, message: str):
        url = self.base_url + self.url
        content = self.session.get(url).html
        form_html = HTML(html=content.find(".js-form-session-data", first=True).html)
        inputTags = form_html.find("input")
        headers = {
            "fs_session": inputTags[0].attrs["value"],
            "fs_timestamp":  inputTags[1].attrs["value"],
            "fs_version":  inputTags[2].attrs["value"],
            inputTags[3].attrs["name"]: inputTags[3].attrs["value"],
            "g_recaptcha_response": "",
            "form_alias_rang": "1",

            "message_topic": message
        }

        post = self.session.post(url, data=headers).text
        post_html = HTML(html=post)

        if post_html.find(".alert", first=True):
                return False

        return True

    def getPages(self) -> int:
        content = self.session.get(self.base_url + self.url).html.find(".bloc-liste-num-page", first=True).text
        try:
            return int(content.split(" ")[1].replace("»", "").replace(".", ""))
        except IndexError:
            return 1

    def getOnlines(self) -> int:
        content = self.session.get(self.base_url + self.url).html.find(".nb-connect-fofo", first=True).text
        return content.split(" ")[0]

class Message:

    def __init__(self, author: str, message: str, date: str):
        self.author = author
        self.message = message
        self.date = date

class JVC:
    BASE_URL = 0
    BASE_URL_FORUM = 1
    BASE_URL_FORUM_SEARCH = 8

    BASE_URLS = {
        BASE_URL: "https://www.jeuxvideo.com",
        BASE_URL_FORUM: "https://www.jeuxvideo.com/forums",
        BASE_URL_FORUM_SEARCH: "https://www.jeuxvideo.com/recherche/forums",
    }

    def __init__(self, cookie: str, forum: str):
        self.cookie = cookie
        self.base_url = self.BASE_URLS[self.BASE_URL_FORUM] + forum
        self.search_url = self.BASE_URLS[self.BASE_URL_FORUM_SEARCH] + forum

        self.session = HTMLSession()
        self.session.cookies.update({
            "coniunctio": self.cookie
        })
        self.lastTopicMessage = None

    def getLastTopic(self, page: int, search: str=None) -> list:
        if(search):
            url_list = self.search_url.split("-")
            url_list[5] = str((page-1)*25 + 1)
            url = "-".join(url_list)
            url += "?search_in_forum={}&type_search_in_forum=titre_topic".format(search)
        else:
            url_list = self.base_url.split("-")
            url_list[5] = str((page-1)*25 + 1)
            url = "-".join(url_list)

        first_topic_found = False
        while not first_topic_found: 
            for element in self.session.get(url).html.find("li"):
                if "data-id" in element.attrs:
                    element_html = HTML(html=element.html)
                    title_element = element_html.find(".topic-title", first=True)
                    if(title_element != None):
                        title = title_element.text
                        author = element_html.find(".topic-author", first=True).text
                        url = next(iter(element_html.find(".lien-jv", first=True).links))
                        self.lastTopicMessage = Topic(title, author, self.BASE_URLS[self.BASE_URL] + url, self.BASE_URLS[self.BASE_URL], self.session)
                        first_topic_found = True
                        break

        return self.lastTopicMessage