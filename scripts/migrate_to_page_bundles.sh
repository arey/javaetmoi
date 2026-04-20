#!/bin/bash
# Migrate a flat Hugo post (.md) to a page bundle (index.md + co-located images)
# Uses git mv to preserve history. Idempotent: skips already-migrated posts.
#
# Usage: ./scripts/migrate_to_page_bundles.sh content/posts/2026/decouverte-de-spring-modulith.md
#    or: ./scripts/migrate_to_page_bundles.sh content/posts/2026/decouverte-de-spring-modulith.md content/posts/2025/some-post.md ...

set -euo pipefail

HUGO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HUGO_ROOT"

migrate_post() {
  local md_file="$1"

  # Validate input
  if [[ ! -f "$md_file" ]]; then
    echo "SKIP: $md_file does not exist (already migrated?)"
    return 0
  fi

  local slug
  slug="$(basename "$md_file" .md)"
  local dir
  dir="$(dirname "$md_file")"
  local bundle_dir="$dir/$slug"

  # Skip if already a page bundle
  if [[ -f "$bundle_dir/index.md" ]]; then
    echo "SKIP: $bundle_dir/index.md already exists"
    return 0
  fi

  echo "=== Migrating: $md_file ==="

  # 1. Create the bundle directory
  mkdir -p "$bundle_dir"

  # 2. Move .md → index.md using git mv
  git mv "$md_file" "$bundle_dir/index.md"

  # 3. Extract all wp-content file references from the post
  #    Matches patterns like: wp-content/uploads/YYYY/MM/filename.ext
  #    Also handles full URLs: https://javaetmoi.com/wp-content/uploads/...
  #    Excludes _xmlsf_image_featured.loc metadata line (line starting with "  loc:")
  local wp_refs
  wp_refs=$(grep -v '  loc: https://' "$bundle_dir/index.md" \
    | grep -oE 'wp-content/uploads/[^"*)\ ]+' \
    | sort -u) || true

  if [[ -z "$wp_refs" ]]; then
    echo "  No wp-content references found (no images to move)"
    # Still add usePageBundles: true
    sed -i '' '/^featureImage:/a\
usePageBundles: true
' "$bundle_dir/index.md" 2>/dev/null || true
    return 0
  fi

  # 4. For each referenced file, copy from static/ to the bundle, then update references
  local ref basename_file static_path decoded_path decoded_basename
  for ref in $wp_refs; do
    static_path="static/$ref"
    basename_file="$(basename "$ref")"

    # Decode URL-encoded characters (e.g., %5F → _)
    decoded_path=$(printf '%b' "$(echo "$static_path" | sed 's/%\([0-9A-Fa-f][0-9A-Fa-f]\)/\\x\1/g')")
    decoded_basename=$(printf '%b' "$(echo "$basename_file" | sed 's/%\([0-9A-Fa-f][0-9A-Fa-f]\)/\\x\1/g')")

    if [[ -f "$decoded_path" ]]; then
      # Copy image to bundle directory using decoded filename
      cp "$decoded_path" "$bundle_dir/$decoded_basename"
      git add "$bundle_dir/$decoded_basename"
      echo "  Copied: $decoded_basename"
    elif [[ -f "$static_path" ]]; then
      cp "$static_path" "$bundle_dir/$basename_file"
      git add "$bundle_dir/$basename_file"
      echo "  Copied: $basename_file"
    else
      echo "  WARNING: $static_path not found!"
    fi

    # 5. Replace all occurrences of the wp-content path with just the (decoded) filename
    #    Handle both relative and full URL references
    #    Use | as sed delimiter since paths contain /
    # First replace full URLs: https://javaetmoi.com/wp-content/... → filename
    sed -i '' "s|https://javaetmoi.com/$ref|$decoded_basename|g" "$bundle_dir/index.md"
    # Then replace relative paths: wp-content/... → filename
    sed -i '' "s|$ref|$decoded_basename|g" "$bundle_dir/index.md"
  done

  # 6. Fix images in summary: prefix bare filenames with post URL (for homepage rendering)
  local post_url
  post_url=$(grep '^url:' "$bundle_dir/index.md" | sed 's/url: *//;s/"//g;s/ *$//')
  if [[ -n "$post_url" ]]; then
    perl -i -pe '
      BEGIN { $url = "'"$post_url"'"; $in_fm = 0; $in_summary = 0; $fm_count = 0; }
      if (/^---/) { $fm_count++; if ($fm_count == 2) { $in_fm = 0; $in_summary = 0; } else { $in_fm = 1; } next; }
      if ($in_fm && /^summary:/) { $in_summary = 1; next; }
      if ($in_fm && $in_summary && /^\S/) { $in_summary = 0; }
      if ($in_summary) {
        s/!\[([^\]]*)\]\(([^\/)(][^)]*\.(?:png|jpg|jpeg|gif|svg|webp|avif|jpe?g))\)/![$1](${url}$2)/g;
      }
    ' "$bundle_dir/index.md"
  fi

  # 7. Add usePageBundles: true to front matter (after featureImage line, or after thumbnail)
  if grep -q '^featureImage:' "$bundle_dir/index.md"; then
    # Insert after featureImageAlt if present, else after featureImage
    if grep -q '^featureImageAlt:' "$bundle_dir/index.md"; then
      sed -i '' '/^featureImageAlt:/a\
usePageBundles: true
' "$bundle_dir/index.md"
    else
      sed -i '' '/^featureImage:/a\
usePageBundles: true
' "$bundle_dir/index.md"
    fi
  elif grep -q '^thumbnail:' "$bundle_dir/index.md"; then
    sed -i '' '/^thumbnail:/a\
usePageBundles: true
' "$bundle_dir/index.md"
  else
    # Fallback: add before the closing ---
    sed -i '' '0,/^---$/!{/^---$/i\
usePageBundles: true
}' "$bundle_dir/index.md"
  fi

  # 8. Verify no wp-content refs remain (except in _xmlsf URLs and guid)
  local remaining
  remaining=$(grep -n "wp-content" "$bundle_dir/index.md" | grep -v "loc: https://" | grep -v "guid: https://" || true)
  if [[ -n "$remaining" ]]; then
    echo "  WARNING: Remaining wp-content references:"
    echo "$remaining"
  else
    echo "  All wp-content references updated successfully"
  fi

  echo "  Done: $bundle_dir/index.md ($(ls "$bundle_dir" | wc -l | tr -d ' ') files)"
}

# Process each argument
for post in "$@"; do
  migrate_post "$post"
done
