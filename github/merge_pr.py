"""
PR 머지 스크립트

단독 실행:
    python merge_pr.py --pr 1
    python merge_pr.py --pr 1 --method squash

모듈 사용:
    from github.merge_pr import merge_pr
    merge_pr(token, owner, repo, pr_number, method)
"""
import argparse

import requests

from auth import get_owner_repo, get_token, make_headers


def merge_pr(token, owner, repo, pr_number, method="merge"):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
    res = requests.put(url, headers=make_headers(token), json={"merge_method": method})
    res.raise_for_status()
    result = res.json()
    print(f"PR 머지 완료: #{pr_number} (sha: {result['sha'][:7]})")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub PR 머지")
    parser.add_argument("--pr", required=True, type=int, help="PR 번호")
    parser.add_argument(
        "--method", default="merge", choices=["merge", "squash", "rebase"], help="머지 방식 (기본값: merge)"
    )
    args = parser.parse_args()

    owner, repo = get_owner_repo()
    token = get_token()
    merge_pr(token, owner, repo, args.pr, args.method)
