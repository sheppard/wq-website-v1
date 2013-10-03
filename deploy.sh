#!/bin/sh
set -e

# Build javascript with wq.app
cd app;
wq build $1;

# Force important files through any unwanted server caching
cd ../;
sed -i "s/wqsite.js/wqsite.js?v="$1"/" htdocs-build/wqsite.appcache
sed -i "s/wqsite.css/wqsite.css?v="$1"/" htdocs-build/wqsite.appcache

# Preserve Django's static files (e.g. admin)
cp -a htdocs/static htdocs-build/static

# Replace existing htdocs with new version
rm -rf htdocs/;
mv -i htdocs-build/ htdocs;

# Restart Django
touch db/wqsite/wsgi.py
