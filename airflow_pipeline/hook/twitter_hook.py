from airflow.providers.http.hooks.http import HttpHook
import requests

class TwitterHook(HttpHook):

    def __init__(self, end_time, start_time, query, conn_id=None):
        self.query = query
        self.end_time = end_time
        self.start_time = start_time
        self.conn_id = conn_id or "twitter_default"
        super().__init__(http_conn_id=self.conn_id)


    def create_url(self):
        TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"

        end_time = self.end_time
        start_time = self.start_time
        query = self.query

        tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
        user_fields = "expansions=author_id&user.fields=id,name,username,created_at"

        url_raw = f"/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"

        return url_raw

    def connect_to_endpoint(self, url, session):
        request = requests.Request("GET", url)
        prep = session.prepare_request(request)
        self.log.info(f'URL: {url}')
        return self.run_and_check(session, prep, {})
