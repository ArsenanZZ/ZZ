create extension if not exists pgcrypto;

create table if not exists public.story_comments (
  id uuid primary key default gen_random_uuid(),
  page_id text not null,
  page_url text not null,
  page_title text not null,
  name text not null,
  body text not null,
  created_at timestamptz not null default now(),
  is_hidden boolean not null default false,
  constraint story_comments_page_id_len check (char_length(page_id) between 1 and 160),
  constraint story_comments_page_url_len check (char_length(page_url) between 1 and 500),
  constraint story_comments_page_title_len check (char_length(page_title) between 1 and 240),
  constraint story_comments_name_len check (char_length(trim(name)) between 1 and 80),
  constraint story_comments_body_len check (char_length(trim(body)) between 1 and 1200),
  constraint story_comments_page_whitelist check (
    page_id in (
      'run50-xiangyang-marathon-facebook-en',
      'run50-xiangyang-marathon-en',
      'run50-xiangyang-marathon-zh',
      'run50-cleveland-marathon-facebook-en',
      'run50-cleveland-marathon-en',
      'run50-cleveland-marathon-zh',
      'run50-louisville-marathon-facebook-en',
      'run50-louisville-marathon-en',
      'run50-louisville-marathon-zh',
      'run50-chicago-marathon-facebook-en',
      'run50-chicago-marathon-en',
      'run50-chicago-marathon-zh',
      'run50-guilin-marathon-facebook-en',
      'run50-guilin-marathon-en',
      'run50-guilin-marathon-zh',
      'run50-hong-kong-marathon-facebook-en',
      'run50-hong-kong-marathon-en',
      'run50-hong-kong-marathon-zh',
      'run50-pisa-marathon-facebook-en',
      'run50-pisa-marathon-en',
      'run50-pisa-marathon-zh',
      'run50-mexico-marathon-facebook-en',
      'run50-mexico-marathon-en',
      'run50-mexico-marathon-zh',
      'run50-miami-marathon-fb',
      'run50-miami-marathon-en',
      'run50-miami-marathon-zh',
      'run50-little-rock-marathon-facebook-en',
      'run50-little-rock-marathon-en',
      'run50-little-rock-marathon-zh',
      'run50-south-carolina-marathon-facebook-en',
      'run50-south-carolina-marathon-en',
      'run50-south-carolina-marathon-zh',
      'run50-san-antonio-marathon-facebook-en',
      'run50-san-antonio-marathon-en',
      'run50-san-antonio-marathon-zh',
      'run50-west-virginia-marathon-facebook-en',
      'run50-west-virginia-marathon-en',
      'run50-west-virginia-marathon-zh',
      'run50-nashville-marathon-facebook-en',
      'run50-nashville-marathon-en',
      'run50-nashville-marathon-zh'
    )
  )
);

alter table public.story_comments enable row level security;

alter table public.story_comments
drop constraint if exists story_comments_page_whitelist;

alter table public.story_comments
add constraint story_comments_page_whitelist check (
  page_id in (
    'run50-xiangyang-marathon-facebook-en',
    'run50-xiangyang-marathon-en',
    'run50-xiangyang-marathon-zh',
    'run50-cleveland-marathon-facebook-en',
    'run50-cleveland-marathon-en',
    'run50-cleveland-marathon-zh',
    'run50-louisville-marathon-facebook-en',
    'run50-louisville-marathon-en',
    'run50-louisville-marathon-zh',
    'run50-chicago-marathon-facebook-en',
    'run50-chicago-marathon-en',
    'run50-chicago-marathon-zh',
    'run50-guilin-marathon-facebook-en',
    'run50-guilin-marathon-en',
    'run50-guilin-marathon-zh',
    'run50-hong-kong-marathon-facebook-en',
    'run50-hong-kong-marathon-en',
    'run50-hong-kong-marathon-zh',
    'run50-pisa-marathon-facebook-en',
    'run50-pisa-marathon-en',
    'run50-pisa-marathon-zh',
    'run50-mexico-marathon-facebook-en',
    'run50-mexico-marathon-en',
    'run50-mexico-marathon-zh',
    'run50-miami-marathon-fb',
    'run50-miami-marathon-en',
    'run50-miami-marathon-zh',
    'run50-little-rock-marathon-facebook-en',
    'run50-little-rock-marathon-en',
    'run50-little-rock-marathon-zh',
    'run50-south-carolina-marathon-facebook-en',
    'run50-south-carolina-marathon-en',
    'run50-south-carolina-marathon-zh',
      'run50-san-antonio-marathon-facebook-en',
      'run50-san-antonio-marathon-en',
      'run50-san-antonio-marathon-zh',
    'run50-west-virginia-marathon-facebook-en',
    'run50-west-virginia-marathon-en',
    'run50-west-virginia-marathon-zh',
    'run50-nashville-marathon-facebook-en',
    'run50-nashville-marathon-en',
    'run50-nashville-marathon-zh'
  )
);

grant usage on schema public to anon;
revoke update, delete on public.story_comments from anon;
grant select, insert on public.story_comments to anon;

drop policy if exists "Public can read visible story comments" on public.story_comments;
create policy "Public can read visible story comments"
on public.story_comments
for select
to anon
using (is_hidden = false);

drop policy if exists "Public can add story comments" on public.story_comments;
create policy "Public can add story comments"
on public.story_comments
for insert
to anon
with check (
  is_hidden = false
  and page_id in (
    'run50-xiangyang-marathon-facebook-en',
    'run50-xiangyang-marathon-en',
    'run50-xiangyang-marathon-zh',
    'run50-cleveland-marathon-facebook-en',
    'run50-cleveland-marathon-en',
    'run50-cleveland-marathon-zh',
    'run50-louisville-marathon-facebook-en',
    'run50-louisville-marathon-en',
    'run50-louisville-marathon-zh',
    'run50-chicago-marathon-facebook-en',
    'run50-chicago-marathon-en',
    'run50-chicago-marathon-zh',
    'run50-guilin-marathon-facebook-en',
    'run50-guilin-marathon-en',
    'run50-guilin-marathon-zh',
    'run50-hong-kong-marathon-facebook-en',
    'run50-hong-kong-marathon-en',
    'run50-hong-kong-marathon-zh',
    'run50-pisa-marathon-facebook-en',
    'run50-pisa-marathon-en',
    'run50-pisa-marathon-zh',
    'run50-mexico-marathon-facebook-en',
    'run50-mexico-marathon-en',
    'run50-mexico-marathon-zh',
    'run50-miami-marathon-fb',
    'run50-miami-marathon-en',
    'run50-miami-marathon-zh',
    'run50-little-rock-marathon-facebook-en',
    'run50-little-rock-marathon-en',
    'run50-little-rock-marathon-zh',
    'run50-south-carolina-marathon-facebook-en',
    'run50-south-carolina-marathon-en',
    'run50-south-carolina-marathon-zh',
      'run50-san-antonio-marathon-facebook-en',
      'run50-san-antonio-marathon-en',
      'run50-san-antonio-marathon-zh',
    'run50-west-virginia-marathon-facebook-en',
    'run50-west-virginia-marathon-en',
    'run50-west-virginia-marathon-zh',
    'run50-nashville-marathon-facebook-en',
    'run50-nashville-marathon-en',
    'run50-nashville-marathon-zh'
  )
  and char_length(trim(name)) between 1 and 80
  and char_length(trim(body)) between 1 and 1200
);
