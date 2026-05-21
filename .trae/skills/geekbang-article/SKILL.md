---
name: "geekbang-article"
description: "Extracts article content from GeekBang URLs and generates Markdown files. Invoke when user provides a GeekBang article URL like https://time.geekbang.org/column/article/xxxxx"
---

# GeekBang Article to Markdown

This skill extracts article content from GeekBang and converts it to a clean Markdown file.

## Usage

When user provides a GeekBang article URL (e.g., `https://time.geekbang.org/column/article/13067`), invoke this skill to:
1. Extract the article ID from the URL
2. Send a POST request to the GeekBang API
3. Extract the `article_content` field
4. Convert HTML to clean Markdown
5. Generate a `.md` file in the current directory

## GeekBang API Details

- **URL**: `https://time.geekbang.org/serv/v1/article`
- **Method**: POST
- **Content-Type**: application/json

### Request Body
```json
{"id": "<article_id>", "include_neighbors": true, "is_freelyread": true}
```

### Required Headers
- `Accept: application/json, text/plain, */*`
- `Content-Type: application/json`
- `Cookie: <user_cookie>` (User must provide their GeekBang cookie for authentication)
- `Origin: https://time.geekbang.org`
- `Referer: https://time.geekbang.org/column/article/<article_id>`
- `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36`
- `X-GEEK-REQ-ID: <request_id>@1@web`


## Error Handling

If the API returns a permission error:
1. Inform the user that the cookie may be expired or invalid
2. Ask user to provide a new cookie
3. Update the cookie in the script or re-run with new cookie

## Example

User provides: `https://time.geekbang.org/column/article/13067`

Extract article ID: `13067`

Generate request to: `https://time.geekbang.org/serv/v1/article`

Output file: `92 程序员面试攻略：面试前的准备.md` (based on article title)
