import requests, time, platform
from typing import Dict, List, Optional, Any

NANOSECONDS = 1_000_000_000

class RequestManager:
    
    _instance = None
    def __new__(cls, *args, **kwargs):
      if not cls._instance:
        cls._instance = super(RequestManager, cls).__new__(cls)
      return cls._instance

    def __init__(self, user_agent: str = f"{platform.system()}/RedditOfflineApp/0.1"):
      if hasattr(self, 'session'):
          return

      self.session = requests.Session()
      self.session.headers.update({'User-Agent': user_agent})
      
      self.window_size = 600  # 10 min
      self.remaining: float = 600.0
      self.used: Optional[int] = None
      self.min_request_interval = 1.0 
      self.last_request_time = 0.0

    # --- Rate Limiting ---

    def _delay(self) -> None:
        now = time.time()
        
        time_since_last = now - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_duration = self.min_request_interval - time_since_last
            print(f" [Pacing] Sleeping {sleep_duration:.2f}s")
            time.sleep(sleep_duration)
            return

        # If we have very few requests left, wait for the reset.
        if self.remaining is not None and self.remaining < 10.0:
            wait_time = max(0, self.reset_timestamp - now)
            if wait_time > 0:
                print(f" [Rate Limit Hit] Remaining: {self.remaining}. Waiting {wait_time:.2f}s for reset.")
                time.sleep(wait_time + 2) # +2 safety buffer

    def _update_rate_limit(self, headers: Dict[str, Any]) -> None:
        if "x-ratelimit-remaining" not in headers:
            return

        self.remaining = float(headers["x-ratelimit-remaining"])
        self.used = int(headers.get("x-ratelimit-used", 0))
        seconds_to_reset = int(headers.get("x-ratelimit-reset", 0))
        
        self.reset_timestamp = time.time() + seconds_to_reset
        
        print(f"--- [API Headers] Remaining: {self.remaining} | Used: {self.used} | Resets in: {seconds_to_reset}s")

    # --- Request Methods ---

    def make_request(self, url: str) -> Dict:

        self._delay()
        try:
            print(f" -> GET {url}")
            response = self.session.get(url)

            self.last_request_time = time.time()

            response = self.session.get(url)

            self._update_rate_limit(response.headers)
            
            if response.status_code == 429:
                print("Hit 429 Too Many Requests. Backing off...")
                time.sleep(15)
                return self.make_request(url) # Retry
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request Error ({url}): {e}")
            time.sleep(2)
            raise


    def download_media(self, url: str) -> bytes:
        # Media that sits on external domains (i.redd.it) don't consume API limit
        try:
            resp = requests.get(url, headers={'User-Agent': self.session.headers['User-Agent']})
            resp.raise_for_status()
            return resp.content
        except Exception as e:
            print(f"[ERROR] Error downloading media: {e}")
            raise


    # --- Responses parsing ---

    def get_posts(self, params: Dict) -> Dict:

        results = {}
        subreddit_failures = []
        
        for subreddit, sub_params in params.items():
            print(f"Fetching {subreddit}...")
            
            num_posts = min(100, sub_params.get("num_posts", 10))
            flairs = sub_params.get("flairs", {"filter": False})
            order_by = sub_params.get("order_by", "hot")
            
            if not flairs.get("filter"):
                url = f'https://reddit.com/r/{subreddit}/{order_by}.json'
            else:
                flairs_list = flairs.get("wanted_flairs", [])
                if not flairs_list:
                    print(f"Flair filter applied, but no flairs specified for {subreddit}, skipping.")
                    continue
                
                url = f'https://reddit.com/r/{subreddit}/search/.json?q=flair%3A"{flairs_list[0]}'
                for flair in flairs_list[1:]:
                  url += f'+OR+flair%3A"{flair}"'
                url += f'&type=posts&sort={order_by}&limit={num_posts}&restrict_sr=on'

            try:
                listing_json = self.make_request(url)
                if listing_json:
                    results[subreddit] = self._process_subreddit_listing(listing_json, sub_params)
                else:
                    subreddit_failures.append(subreddit)
            except Exception as e:
                print(f"[ERROR] Failed to fetch {subreddit}: {e}")
                subreddit_failures.append(subreddit)
                continue
        
        if subreddit_failures:
            print(f"[WARN] Failed to fetch: {", ".join(subreddit_failures)}")
        return results


    def _process_subreddit_listing(self, listing_json: Dict, params: Dict) -> List[Dict]:

        valid_posts = []
        
        try:
            min_comments = params.get("ignore_if_fewer_comments_than", 0)
            children = listing_json.get('data', {}).get('children', [])
            
            for item in children:
                if len(valid_posts) >= params['num_posts']:
                    break
                
                post_data = item['data']
                
                if params.get("ignore_stickied_posts") and post_data.get("stickied"):
                    continue
                
                if post_data.get("num_comments", 0) < min_comments:
                    continue

                permalink = post_data['permalink']
                full_url = f'https://reddit.com{permalink}.json'
                
                try:
                    print(f"--- Fetching details: {post_data.get('title')[:30]}...")
                    post_details = self.make_request(full_url)
                    valid_posts.append(post_details)
                except Exception as e:
                    print(f"[ERROR] Error fetching details for {permalink}: {e}")
                    
        except Exception as e:
            print(f"[ERROR] Error processing listing: {e}")
            
        return valid_posts

 