#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import requests
import yaml


GRAPHQL_URL = "https://api.github.com/graphql"
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class PostInfo:
    title: str
    url: str
    path: Path
    post_id: str | None


class GitHubDiscussionsClient:
    def __init__(
        self,
        token: str,
        repo_owner: str,
        repo_name: str,
        category_id: str | None,
        category_name: str | None,
    ) -> None:
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.category_id = category_id
        self.category_name = category_name
        self.repo_id: str | None = None
        self.mutation_delay_seconds = 0.35
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
            }
        )

    def graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        delay_seconds = 1.0
        for attempt in range(6):
            try:
                response = self.session.post(
                    GRAPHQL_URL,
                    json={"query": query, "variables": variables},
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
            except requests.RequestException:
                if attempt == 5:
                    raise
                time.sleep(delay_seconds)
                delay_seconds *= 2
                continue

            errors = payload.get("errors") or []
            if not errors:
                return payload["data"]

            retryable = any(
                "too quickly" in str(error.get("message", "")).lower()
                or "secondary rate limit" in str(error.get("message", "")).lower()
                for error in errors
            )
            if not retryable or attempt == 5:
                raise RuntimeError(json.dumps(errors, ensure_ascii=False, indent=2))

            time.sleep(delay_seconds)
            delay_seconds *= 2

        raise RuntimeError("Unexpected retry exhaustion in graphql()")

    def ensure_repository_context(self) -> None:
        if self.repo_id and self.category_id:
            return

        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
            discussionCategories(first: 100) {
              nodes {
                id
                name
              }
            }
          }
        }
        """
        data = self.graphql(
            query,
            {"owner": self.repo_owner, "name": self.repo_name},
        )
        repository = data["repository"]
        self.repo_id = repository["id"]

        if self.category_id:
            return

        if not self.category_name:
            raise RuntimeError("Either --category-id or --category-name must be provided.")

        for category in repository["discussionCategories"]["nodes"]:
            if category["name"] == self.category_name:
                self.category_id = category["id"]
                return

        raise RuntimeError(
            f"Discussion category '{self.category_name}' not found in {self.repo_owner}/{self.repo_name}."
        )

    def find_discussion_by_title(self, title: str) -> dict[str, Any] | None:
        query = """
        query($owner: String!, $name: String!, $after: String) {
          repository(owner: $owner, name: $name) {
            discussions(first: 100, after: $after) {
              nodes {
                id
                number
                title
                url
              }
              pageInfo {
                hasNextPage
                endCursor
              }
            }
          }
        }
        """

        after: str | None = None
        while True:
            data = self.graphql(
                query,
                {
                    "owner": self.repo_owner,
                    "name": self.repo_name,
                    "after": after,
                },
            )
            discussions = data["repository"]["discussions"]
            for discussion in discussions["nodes"]:
                if discussion["title"] == title:
                    return discussion

            if not discussions["pageInfo"]["hasNextPage"]:
                return None
            after = discussions["pageInfo"]["endCursor"]

    def create_discussion(self, title: str, body: str) -> dict[str, Any]:
        self.ensure_repository_context()
        mutation = """
        mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
          createDiscussion(
            input: {
              repositoryId: $repositoryId,
              categoryId: $categoryId,
              title: $title,
              body: $body
            }
          ) {
            discussion {
              id
              number
              title
              url
            }
          }
        }
        """
        data = self.graphql(
            mutation,
            {
                "repositoryId": self.repo_id,
                "categoryId": self.category_id,
                "title": title,
                "body": body,
            },
        )
        time.sleep(self.mutation_delay_seconds)
        return data["createDiscussion"]["discussion"]

    def add_comment(self, discussion_id: str, body: str, reply_to_id: str | None) -> str:
        mutation = """
        mutation($discussionId: ID!, $body: String!, $replyToId: ID) {
          addDiscussionComment(
            input: {
              discussionId: $discussionId,
              body: $body,
              replyToId: $replyToId
            }
          ) {
            comment {
              id
            }
          }
        }
        """
        data = self.graphql(
            mutation,
            {
                "discussionId": discussion_id,
                "body": body,
                "replyToId": reply_to_id,
            },
        )
        time.sleep(self.mutation_delay_seconds)
        return data["addDiscussionComment"]["comment"]["id"]


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    parser = argparse.ArgumentParser(
        description="Import WordPress comments from data/comments.yaml into GitHub Discussions."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Import comments for all posts and pages referenced in the comments export.",
    )
    parser.add_argument(
        "--post-url",
        dest="post_urls",
        action="append",
        help="Post URL to import, for example /2016/08/migrer-vers-spring-boot/",
    )
    parser.add_argument(
        "--repo",
        default="arey/javaetmoi",
        help="GitHub repository in owner/name form.",
    )
    parser.add_argument(
        "--category-id",
        default="DIC_kwDOSAqqoM4C6w9g",
        help="GitHub discussion category ID.",
    )
    parser.add_argument(
        "--category-name",
        default=None,
        help="GitHub discussion category name, used when --category-id is omitted.",
    )
    parser.add_argument(
        "--site-url",
        default="https://javaetmoi.com",
        help="Canonical site base URL used in created discussion bodies.",
    )
    parser.add_argument(
        "--comments-file",
        type=Path,
        default=repo_root / "data/comments.yaml",
        help="Path to the exported WordPress comments YAML file.",
    )
    parser.add_argument(
        "--content-root",
        type=Path,
        default=repo_root / "content",
        help="Path to the Hugo content directory.",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=script_dir / "import_state.json",
        help="Path to the JSON state file used for resumable imports.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub token. Defaults to the GITHUB_TOKEN environment variable.",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue with the next post if one import fails, then report all failures at the end.",
    )
    return parser.parse_args()


def normalize_url(url: str) -> str:
    normalized = url.strip()
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    if not normalized.endswith("/"):
        normalized = f"{normalized}/"
    return normalized


def read_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1)) or {}
    return data if isinstance(data, dict) else {}


def infer_bundle_url(path: Path, content_root: Path) -> str | None:
    relative = path.relative_to(content_root)
    parts = relative.parts
    if len(parts) == 3 and parts[0] == "pages" and parts[-1] == "index.md":
        return f"/{parts[1]}/"
    return None


def build_post_index(content_root: Path) -> dict[str, PostInfo]:
    index: dict[str, PostInfo] = {}
    for path in content_root.rglob("*.md"):
        front_matter = read_front_matter(path)
        title = front_matter.get("title")
        url = front_matter.get("url") or infer_bundle_url(path, content_root)
        if not title or not url:
            continue
        normalized_url = normalize_url(str(url))
        post_id = front_matter.get("post_id")
        index[normalized_url] = PostInfo(
            title=str(title),
            url=normalized_url,
            path=path,
            post_id=str(post_id) if post_id is not None else None,
        )
    return index


def load_comments(path: Path) -> list[dict[str, Any]]:
    comments = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(comments, list):
        raise RuntimeError(f"Unexpected comments format in {path}.")
    return [comment for comment in comments if isinstance(comment, dict)]


def collect_target_urls(args: argparse.Namespace, comments: list[dict[str, Any]]) -> list[str]:
    urls_from_args = [normalize_url(url) for url in (args.post_urls or [])]
    if args.all:
        urls_from_comments = sorted(
            {
                normalize_url(str(comment.get("post_url") or ""))
                for comment in comments
                if str(comment.get("post_url") or "").strip()
            }
        )
        if urls_from_args:
            seen = set(urls_from_comments)
            urls_from_comments.extend(url for url in urls_from_args if url not in seen)
        return urls_from_comments

    if not urls_from_args:
        raise RuntimeError("Use --all or provide at least one --post-url.")

    return urls_from_args


def load_state(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {"discussions": {}, "comments": {}}

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected state format in {path}.")

    discussions = data.get("discussions") or {}
    comments = data.get("comments") or {}
    if not isinstance(discussions, dict) or not isinstance(comments, dict):
        raise RuntimeError(f"Unexpected state format in {path}.")

    return {
        "discussions": {str(key): str(value) for key, value in discussions.items()},
        "comments": {str(key): str(value) for key, value in comments.items()},
    }


def save_state(path: Path, state: dict[str, dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def format_discussion_body(post: PostInfo, site_url: str) -> str:
    article_url = f"{site_url.rstrip('/')}{post.url}"
    return "\n".join(
        [
            f"Imported from the WordPress comments of [{post.title}]({article_url}).",
            "",
            "This discussion is used by Giscus for the article comments.",
        ]
    )


def format_comment_body(comment: dict[str, Any]) -> str:
    author_name = str(comment.get("author_name") or "Unknown author").strip()
    author_url = str(comment.get("author_url") or "").strip()
    published = str(comment.get("published") or "").strip()
    content = str(comment.get("content") or "").strip()

    author_label = f"[{author_name}]({author_url})" if author_url else author_name
    metadata = ["_Imported from WordPress._", "", f"Author: {author_label}"]
    if published:
        metadata.append(f"Published: {published}")

    return "\n".join(metadata + ["", content])


def sort_comments(comments: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        comments,
        key=lambda comment: (
            str(comment.get("published") or ""),
            int(str(comment.get("id") or "0")),
        ),
    )


def ensure_discussion(
    client: GitHubDiscussionsClient,
    post: PostInfo,
    site_url: str,
    state: dict[str, dict[str, str]],
    state_file: Path,
) -> tuple[str, dict[str, Any], bool]:
    discussion_id = state["discussions"].get(post.url)
    if discussion_id:
        discussion = client.find_discussion_by_title(post.title)
        if discussion and discussion["id"] == discussion_id:
            return discussion_id, discussion, False

    discussion = client.find_discussion_by_title(post.title)
    if discussion:
        state["discussions"][post.url] = discussion["id"]
        save_state(state_file, state)
        return discussion["id"], discussion, False

    discussion = client.create_discussion(post.title, format_discussion_body(post, site_url))
    state["discussions"][post.url] = discussion["id"]
    save_state(state_file, state)
    return discussion["id"], discussion, True


def import_post_comments(
    client: GitHubDiscussionsClient,
    post: PostInfo,
    comments: list[dict[str, Any]],
    state: dict[str, dict[str, str]],
    state_file: Path,
    site_url: str,
) -> tuple[dict[str, Any], int, int]:
    discussion_id, discussion, discussion_created = ensure_discussion(
        client, post, site_url, state, state_file
    )

    children_by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    comment_ids = {str(comment.get("id") or "") for comment in comments}
    for comment in comments:
        parent_id = str(comment.get("parent_id") or "0")
        if parent_id != "0" and parent_id not in comment_ids:
            parent_id = "0"
        children_by_parent[parent_id].append(comment)

    imported_comments = 0

    def import_children(
        parent_wordpress_id: str,
        parent_discussion_comment_id: str | None,
        thread_root_discussion_comment_id: str | None,
    ) -> None:
        nonlocal imported_comments
        for comment in sort_comments(children_by_parent.get(parent_wordpress_id, [])):
            comment_id = str(comment.get("id") or "")
            discussion_comment_id = state["comments"].get(comment_id)
            reply_to_id = (
                None
                if parent_wordpress_id == "0"
                else thread_root_discussion_comment_id or parent_discussion_comment_id
            )
            if not discussion_comment_id:
                discussion_comment_id = client.add_comment(
                    discussion_id,
                    format_comment_body(comment),
                    reply_to_id,
                )
                state["comments"][comment_id] = discussion_comment_id
                save_state(state_file, state)
                imported_comments += 1

            next_thread_root_discussion_comment_id = (
                discussion_comment_id
                if parent_wordpress_id == "0"
                else thread_root_discussion_comment_id or parent_discussion_comment_id
            )
            import_children(
                comment_id,
                discussion_comment_id,
                next_thread_root_discussion_comment_id,
            )

    import_children("0", None, None)
    return discussion, imported_comments, 1 if discussion_created else 0


def main() -> int:
    args = parse_args()
    if not args.token:
        print("GitHub token missing. Use --token or set GITHUB_TOKEN.", file=sys.stderr)
        return 1

    if "/" not in args.repo:
        print("--repo must be in owner/name form.", file=sys.stderr)
        return 1

    repo_owner, repo_name = args.repo.split("/", 1)
    post_index = build_post_index(args.content_root)
    comments = load_comments(args.comments_file)
    state = load_state(args.state_file)
    target_urls = collect_target_urls(args, comments)

    client = GitHubDiscussionsClient(
        token=args.token,
        repo_owner=repo_owner,
        repo_name=repo_name,
        category_id=args.category_id,
        category_name=args.category_name,
    )

    total_discussions_created = 0
    total_comments_imported = 0
    total_posts_processed = 0
    failures: list[tuple[str, str]] = []

    for post_url in target_urls:
        post = post_index.get(post_url)
        if not post:
            message = f"Post not found for URL: {post_url}"
            if not args.keep_going:
                print(message, file=sys.stderr)
                return 1
            failures.append((post_url, message))
            print(f"{post_url}: FAILED - {message}", file=sys.stderr)
            continue

        post_comments = [
            comment
            for comment in comments
            if normalize_url(str(comment.get("post_url") or "")) == post_url
        ]
        if not post_comments:
            print(f"{post_url}: no comments to import")
            continue

        try:
            discussion, imported_comments, created_discussions = import_post_comments(
                client,
                post,
                post_comments,
                state,
                args.state_file,
                args.site_url,
            )
        except Exception as exc:
            message = str(exc)
            if not args.keep_going:
                raise
            failures.append((post_url, message))
            print(f"{post_url}: FAILED - {message}", file=sys.stderr)
            continue

        total_posts_processed += 1
        total_discussions_created += created_discussions
        total_comments_imported += imported_comments

        print(f"{post.url} -> {post.title}")
        print(f"  discussion: #{discussion['number']} {discussion['url']}")
        print(f"  comments processed: {len(post_comments)}")
        print(f"  comments imported now: {imported_comments}")

    print("Summary")
    print(f"  targets requested: {len(target_urls)}")
    print(f"  posts processed: {total_posts_processed}")
    print(f"  discussions created: {total_discussions_created}")
    print(f"  comments imported: {total_comments_imported}")
    print(f"  failures: {len(failures)}")
    if failures:
        for post_url, message in failures:
            print(f"  - {post_url}: {message}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())