./manage.py dumpdata blog --natural-foreign --indent 2 \
    -e contenttypes -e auth.permission \
    -e wagtailcore.groupcollectionpermission \
    -e wagtailcore.grouppagepermission \
    -e wagtailimages.rendition \
    -e wagtailcore.pagerevision \
    -e sessions >./fixtures/data.json
